# YOLO-with-Raspi5
Hello

# laser_segmentation
![ROS2](https://img.shields.io/badge/ros2-humble-blue?logo=ros&logoColor=white)
![License](https://img.shields.io/github/license/ajtudela/laser_segmentation)
[![Build](https://github.com/ajtudela/laser_segmentation/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/ajtudela/laser_segmentation/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/ajtudela/laser_segmentation/graph/badge.svg?token=R48HZO62SQ)](https://codecov.io/gh/ajtudela/laser_segmentation)

## ROS package configuration
**Subscribed Topic**: 
  - Input image-stream ```sensor_msgs/msg/Image```<br>

**Published Topic**: 
  - Image-stream with bounding box around detected objects ```sensor_msgs/msg/Image```<br>
  - Bounding boxes (manually created message type) ```boundingboxes/msg/BoundingBoxes```



## Results


## References
* https://github.com/moksh-401-511/YOLOv5_ROS2-YOu-can-Leverage-On-ROS2
* http://www.yahboom.net/study/MicroROS-Pi5

## Developers
* Minje Kim (minje617@gmail.com)
