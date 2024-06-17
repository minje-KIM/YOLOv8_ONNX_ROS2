# YOLOv8_ONNX_ROS2
![ROS2](https://img.shields.io/badge/ros2-humble-blue?logo=ros&logoColor=white)
![Ubuntu](https://img.shields.io/badge/ubuntu-22.04-blue)
![Python](https://img.shields.io/badge/python-3.8-blue)

This repository is a ROS2 package that performs object detection using YOLOv8 with ONNX.

![euroc2](https://github.com/minje-KIM/YOLO-with-Raspi5/assets/61033374/b8e3675a-fe53-4567-9045-5493ef073690)


## ROS Package Configuration
**Subscribed Topic**: 
  - Image-stream : ```sensor_msgs/msg/Image```<br>

**Published Topic**: 
  - Image-stream with bounding box around detected objects : ```sensor_msgs/msg/Image```<br>
 
![image](rqt_graph.png)


## Results
* Actual video
TBD
* comparison table
TBD

## Experimental Setup
platform and experiment situation
we experimented with the MicroRos-Rp5 model at UNIST.

## References
* https://github.com/moksh-401-511/YOLOv5_ROS2-YOu-can-Leverage-On-ROS2
* http://www.yahboom.net/study/MicroROS-Pi5
* https://github.com/ConfusionTechnologies/ros-yolov5-node
  
## Developers
* Minje Kim (minje617@gmail.com)
