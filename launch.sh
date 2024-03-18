#!/bin/bash
nohup roscore &

nohup roslaunch jetracer jetracer.launch &

roscore_pid=$!
jetracer_pid=$!

echo "PID roscore: $roscore_pid"
echo "PID jetracer: $jetracer_pid"

