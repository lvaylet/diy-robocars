#!/usr/bin/env bash

if [[ -n "${DEBUG}" ]]; then
  echo "Entering infinite loop..."
  while true; do sleep 1; done
else
  # echo "Initializing workspace..."
  # catkin_init_workspace

  echo "Building package..."
  catkin_make

  echo "Installing package..."
  catkin_make install
  # Note: why not `source install/setup.bash?`
  source devel/setup.bash

  echo "Starting node..."
  rosrun pca9685 pca9685_node
fi
