# Build with:
# $ docker build -t ros-pca9685 .
#
# Run with:
# $ docker run -it --rm ros-pca9685
#
# Inspect with:
# $ docker run -it --rm ros-pca9685 bash
# root@217f8db31d8a:/#

ARG ROS_DISTRO_VERSION=melodic
ARG ROS_ARCHITECTURE=arm32v7

FROM ${ROS_ARCHITECTURE}/ros:${ROS_DISTRO_VERSION}-ros-base

# Create workspace and set as working directory
WORKDIR /usr/catkin_ws

# Bundle source code
COPY src/ ./src/

# Bundle start script
COPY start.sh ./

# Build and install package
# Note : `source` does not work in Dockerfile because default shell is /bin/sh
# Use `.` instead, as described at https://stackoverflow.com/questions/20635472/using-the-run-instruction-in-a-dockerfile-with-source-does-not-work
RUN . /opt/ros/melodic/setup.sh \
 && catkin_make \
 && catkin_make install

CMD [ "bash", "start.sh"]
