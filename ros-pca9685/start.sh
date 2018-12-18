#!/usr/bin/env bash

# Enter debug mode when a DEBUG variable is defined, no matter its actual value
if [[ -n "${DEBUG}" ]]; then

  echo "Entering infinite loop..."
  while true; do sleep 1; done

else

  echo "Setting up package..."
  source devel/setup.bash

  echo "Starting node..."
  rosrun pca9685 pca9685_node

fi
