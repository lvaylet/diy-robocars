ARG PYTHON_VERSION=3.6

FROM resin/raspberrypi3-python:${PYTHON_VERSION} as builder
# Use multi-stage build to reduce final image size from 330 MB down to 215 MB
# References:
# - https://www.merixstudio.com/blog/docker-multi-stage-builds-python-development/

ENV PYTHONUNBUFFERED 1

# Install GCC and Python libraries
RUN apt-get update && apt-get install -y \
      build-essential \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /wheels

COPY requirements.txt ./
# Collect or create wheels out of downloaded packages and saves them in workdir
RUN pip install --upgrade pip \
 && pip install --upgrade wheel \
 && pip wheel -r requirements.txt

# ---

FROM resin/raspberrypi3-python:${PYTHON_VERSION}-slim

LABEL maintainer="Laurent Vaylet <laurent.vaylet@gmail.com>"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
      python3-smbus \
      i2c-tools \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# This is where the magic of multi-stage builds kicks in. Contents of /wheels is
# copied from builder image by specifying --from param. Then pip install with
# additional -f flag is being run. This will force pip to use .whl archives in
# the specified directory. After that, both /wheels and /root/.cache/pip folders
# are removed, as you don’t need them anymore.
COPY --from=builder /wheels /wheels
RUN pip install --upgrade pip \
 && pip install -r /wheels/requirements.txt \
                --find-links /wheels \
 && rm -rf /wheels \
 && rm -rf /root/.cache/pip/*

WORKDIR /usr/src/app

# Bundle app code
COPY . ./

# Start application
CMD [ "bash", "start.sh" ]
