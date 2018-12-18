ARG ROS_DISTRO_VERSION=melodic
ARG ROS_ARCHITECTURE=arm32v7

FROM ${ROS_ARCHITECTURE}/ros:${ROS_DISTRO_VERSION}-ros-base

ARG ROS_DISTRO_VERSION

RUN apt-get update && apt-get install -y \
      ros-${ROS_DISTRO_VERSION}-ros-tutorials \
      ros-${ROS_DISTRO_VERSION}-common-tutorials \
 && rm -rf /var/lib/apt/lists/
