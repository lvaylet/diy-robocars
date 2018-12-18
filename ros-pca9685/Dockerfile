ARG ROS_DISTRO_VERSION=melodic
ARG ROS_ARCHITECTURE=arm32v7

FROM ${ROS_ARCHITECTURE}/ros:${ROS_DISTRO_VERSION}-ros-base

# Build with:
# $ docker build -t ros-pca9685 .
#
# Run with:
# $ docker run -it --rm ros-pca9685
#
# Inspect with:
# $ docker run -it --rm ros-pca9685 bash
# root@217f8db31d8a:/#

WORKDIR /usr/catkin_ws

# Bundle source code
COPY src/ ./src/

# Bundle start script
COPY start.sh ./

CMD [ "bash", "start.sh"]
