FROM resin/raspberrypi3-python:3.6-slim

LABEL maintainer="Laurent Vaylet <laurent.vaylet@gmail.com>"

WORKDIR /usr/src/app

# Disable "running on RPi" detection during installation of picamera below
# Reference: https://github.com/resin-io-projects/resin-rpi-python-picamera/issues/8
ENV READTHEDOCS True

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Bundle app code
COPY . ./

# Start application
CMD [ "bash", "start.sh" ]
