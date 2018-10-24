#!/usr/bin/env bash

echo "Probing camera module..."
# Requires `io.resin.features.kernel-modules` label in `docker-compose.yml`
# Reference: https://docs.resin.io/learn/develop/hardware/i2c-and-spi/#raspberry-pi-camera-module
modprobe bcm2835-v4l2

if [[ -z "${DEBUG}" ]]; then
  echo "Entering infinite loop..."
  while true; do sleep 1; done
else
  echo "Starting application..."
  python app.py
fi
