ARG ROS_DISTRO_VERSION=melodic
ARG ROS_ARCHITECTURE=arm32v7

FROM ${ROS_ARCHITECTURE}/ros:${ROS_DISTRO_VERSION}-ros-base

# Test with:
# $ docker run -it --rm ros:melodic-ros-base bash
# root@217f8db31d8a:/#
#
# Build with:
# $ docker build -t ros-pca9685 .

# Setup ROS environment
# RUN source "/opt/ros/melodic/setup.bash"
# RUN source /opt/ros/${ROS_DISTRO_VERSION}/setup.bash
# RUN /bin/bash -c "source /opt/ros/melodic/setup.bash"
# RUN /bin/bash -c "source /opt/ros/melodic/setup.bash; catkin_init_workspace /home/ros/workspace/src'

# Create workspace
WORKDIR /usr/catkin_ws

# Bundle source code
COPY src/ ./

# Initialize workspace
# Inspired from: https://github.com/sigproc/docker/blob/master/ros-indigo/Dockerfile
# RUN mkdir -p /usr/catkin_ws/src \
#  && /bin/bash -c "source /opt/ros/melodic/setup.bash; catkin_init_workspace /usr/catkin_ws"
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash; catkin_init_workspace /usr/catkin_ws"

# Clone ros-pwm-msgs and ros-pca9685 packages locally in src/
# RUN cd /usr/catkin_ws/src \
#  && git clone https://github.com/cocasema/ros-pwm-msgs \
#  && git clone https://github.com/cocasema/ros-pca9685

# Clone submodules in ros-pca9685
# Edit ros-pca9685/.gitmodules and change git@github.com:cocasema/simple_io.git to https://github.com/cocasema/simple_io.git, so the next command does not require SSH
# RUN cd ros-pca9685 \
#  && sed -i -e 's/git@github.com:cocasema\/simple_io.git/https:\/\/github.com\/cocasema\/simple_io.git/g' .gitmodules \
#  && git submodule update --init

# Build package
# RUN cd /usr/catkin_ws \
#  && /bin/bash -c "source /opt/ros/melodic/setup.bash; catkin_make"
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash; catkin_make"

# Install package
# Note: why not `source install/setup.bash?`
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash; catkin_make_install" \
 && /bin/bash -c "source devel/setup.bash"

CMD [ "rosrun", "pca9685", "pca9685_node" ]
