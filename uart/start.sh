#!/usr/bin/env bash

if [[ -n "${DEBUG}" ]]; then
  echo "Entering infinite loop..."
  while true; do sleep 1; done
else
  echo "Starting application..."
  node main.js
fi
