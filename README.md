# PBL2024
This repository contains our build system and code for Nvidia Jetracer platform. The code is written in Python and uses ROS for communication between different components. The main goal of this project is to create a system that allows the Jetracer to avoid obstacles using a Lidar sensor.

## General info
This project is a part of the PBL2024 course at the Warsaw University of Technology. The code is written in Python and uses ROS for communication between different components. The main goal of this project is to create a system that allows the Jetracer to avoid obstacles using a Lidar sensor.

To run this code, you must have a virtual machine configured, along with the Nvidia Jetracer ROS AI kit.

## Setup
1. scp launch.sh script to your Jetracer machine (eg. scp launch.sh jetson@10.44.25.xx:/home/jetson/Documents).
2. Connect via ssh to your Jetracer (eg. ssh jetson@10.44.25.xx).
3. cd to the directory where you copied launch.sh script.
4. ```chmod +x launch.sh```
5. ```./launch.sh```
6. After a few seconds, jetracer should be running, along with the lidar component
If you want to add more components, you can add them to the launch.sh script by adding the following line: ```roslaunch <package_name> <launch_file> --wait &```
7. Now you can close the ssh connection and connect to the Jetracer via ROS tools (eg. Rviz, Rqt, etc.)
8. To run the script allowing the Jetracer to avoid obstacles, run the following command: ```python avoid_obstacles.py```