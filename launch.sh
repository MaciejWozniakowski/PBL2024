#!/bin/bash
source /opt/ros/melodic/setup.bash
source /home/jetson/catkin_ws/devel/setup.bash
roscore  &
roslaunch jetracer jetracer.launch --wait &
roslaunch jetracer lidar.launch --wait &
