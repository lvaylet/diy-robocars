#!/usr/bin/env bash

if [[ -n "${DEBUG}" ]]; then
  echo "Entering infinite loop..."
  echo 'Start a minicom session with: minicom -b 57600 -o -D "/dev/ttyACM0"'
  while true; do sleep 1; done
else
  echo "Starting application..."
  node main.js
fi
