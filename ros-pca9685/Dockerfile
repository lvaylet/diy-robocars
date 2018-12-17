FROM arm32v7/ros:melodic-ros-base

# Setup ROS environment
# RUN source "/opt/ros/$ROS_DISTRO/setup.bash" 

# Create workspace
# WORKDIR /usr/catkin_ws

# Initialize workspace
RUN mkdir -p /usr/catkin_ws/src \
 && cd /usr/catkin_ws \
 && catkin_make

# Clone ros-pwm-msgs and ros-pca9685 packages locally in src/
RUN cd src \
 && git clone https://github.com/cocasema/ros-pwm-msgs \
 && git clone --recurse-submodules https://github.com/cocasema/ros-pca9685

# Edit ros-pca9685/.gitmodules and change git@github.com:cocasema/simple_io.git to https://github.com/cocasema/simple_io.git

RUN cd ros-pca9685 \
 && git submodule update --init

# Build package 
RUN cd /usr/catkin_ws \
 && catkin_make

# Install package
RUN catkin_make install
