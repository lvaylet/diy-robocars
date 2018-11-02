#!/usr/bin/env bash

echo "Enabling I2C..."
# Reference: https://www.balena.io/docs/learn/develop/hardware/i2c-and-spi/#i2c
modprobe i2c-dev

echo "Scanning I2C bus for devices..."
i2cdetect -y 1

if [[ -z "${DEBUG}" ]]; then
  echo "Entering infinite loop..."
  while true; do sleep 1; done
else
  echo "Starting application..."
  python app.py
fi
