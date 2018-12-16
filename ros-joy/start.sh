#!/usr/bin/env bash

if [[ -n "${DEBUG}" ]]; then
  echo "Entering infinite loop..."
  while true; do sleep 1; done
else
  echo "Starting application..."
  rosparam set joy_node/dev "/dev/input/js0"
  rosrun joy joy_node
fi
