#!/usr/bin/env python3
import rclpy
import cv2
import os
import onnxruntime as ort
import numpy as np
from .utils import xywh2xyxy, draw_detections, multiclass_nms
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ament_index_python.packages import get_package_share_directory

class DetectionNode(Node): 
    def __init__(self):
        super().__init__("YOLO_v8") 
        
        self.declare_parameter('subscribed_topic', '/cam0/image_raw')
        self.declare_parameter('published_topic', '/Detected_image')
        self.declare_parameter('conf_threshold', 0.3)
        self.declare_parameter('iou_threshold', 0.5)
        self.declare_parameter('model_file', 'yolov8m.onnx')


        self.subscribed_topic = self.get_parameter('subscribed_topic').value
        self.published_topic = self.get_parameter('published_topic').value
        self.conf_threshold= self.get_parameter('conf_threshold').value
        self.iou_threshold= self.get_parameter('iou_threshold').value
        self.model_file = self.get_parameter('model_file').value

        self.subscriber = self.create_subscription(Image, self.subscribed_topic, self.subscriber_callback, 10)
        self.publisher = self.create_publisher(Image, self.published_topic, 10)
        
        self.bridge = CvBridge()
        
        package_share_directory = get_package_share_directory('yolo_v8')
        model_path = os.path.join(package_share_directory, 'resource', self.model_file)
        self.ort_session = ort.InferenceSession(model_path)

        model_inputs = self.ort_session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]

        self.input_shape = model_inputs[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]
        
        self.prev_time = cv2.getTickCount()

    def subscriber_callback(self, msg):
        input_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        detections = self.run_inference(input_image)
        self.boxes, self.scores, self.class_ids = self.process_output(detections)

        output_image = draw_detections(input_image, self.boxes, self.scores, self.class_ids, mask_alpha=0.4)
        
        current_time = cv2.getTickCount()
        time_difference = (current_time - self.prev_time) / cv2.getTickFrequency()
        fps = 1.0 / time_difference
        self.prev_time = current_time
        
        fps_text = f"FPS: {fps:.2f}"
        cv2.putText(output_image, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        
        self.publisher.publish(self.bridge.cv2_to_imgmsg(output_image, "bgr8"))

    def process_output(self, output):
        predictions = np.squeeze(output[0]).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > self.conf_threshold, :]
        scores = scores[scores > self.conf_threshold]

        if len(scores) == 0:
            return [], [], []

        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Get bounding boxes for each object
        boxes = self.extract_boxes(predictions)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        # indices = nms(boxes, scores, self.iou_threshold)
        indices = multiclass_nms(boxes, scores, class_ids, self.iou_threshold)

        return boxes[indices], scores[indices], class_ids[indices]

    def extract_boxes(self, predictions):
        # Extract boxes from predictions
        boxes = predictions[:, :4]

        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes)

        # Convert boxes to xyxy format
        boxes = xywh2xyxy(boxes)

        return boxes
    
    def rescale_boxes(self, boxes):
        # Rescale boxes to original image dimensions
        input_shape = np.array([self.input_width, self.input_height, self.input_width, self.input_height])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([self.img_width, self.img_height, self.img_width, self.img_height])
        return boxes

    def preprocess(self, image):
        self.img_height, self.img_width = image.shape[:2]
        
        resized = cv2.resize(image, (640, 480))
        normalized = resized / 255.0
        transposed = np.transpose(normalized, (2, 0, 1))
        input_data = np.expand_dims(transposed, axis=0).astype(np.float32)
        return input_data

    def run_inference(self, input_image):
        input_data = self.preprocess(input_image)
        ort_inputs = {self.ort_session.get_inputs()[0].name: input_data}
        ort_outs = self.ort_session.run(None, ort_inputs)
        return ort_outs
        
    def draw_detections(self, image, detections):
        for detection in detections[0]:
            x1, y1, x2, y2, conf, cls = detection
            if conf > 0.5:
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                label = f"Class: {int(cls)}, Conf: {conf:.2f}"
                cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return image

def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode() 
    rclpy.spin(node)
    DetectionNode.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
