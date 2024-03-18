#!/bin/bash
export DISPLAY=localhost:0.0
xterm -e -hold roslaunch jetracer jetracer.launch 
roscore


