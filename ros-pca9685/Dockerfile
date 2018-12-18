ARG ROS_DISTRO_VERSION=melodic
ARG ROS_ARCHITECTURE=arm32v7

FROM ${ROS_ARCHITECTURE}/ros:${ROS_DISTRO_VERSION}-ros-base

ARG ROS_DISTRO_VERSION

# Create workspace and set as working directory
WORKDIR /usr/catkin_ws

# Bundle source code
COPY src/ ./src/

# Build and install package
# Note : `source` does not work in Dockerfile because default shell is /bin/sh
# Use `.` instead, as described at https://stackoverflow.com/questions/20635472/using-the-run-instruction-in-a-dockerfile-with-source-does-not-work
RUN . /opt/ros/${ROS_DISTRO_VERSION}/setup.sh \
 && catkin_make \
 && catkin_make install

# Bundle start script
COPY start.sh ./

CMD [ "bash", "start.sh" ]
