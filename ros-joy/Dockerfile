FROM arm32v7/ros:melodic-ros-base

RUN apt-get update && apt-get install -y \
      ros-melodic-joy \
 && rm -rf /var/lib/apt/lists/

WORKDIR /usr/src/app

# Bundle app code
COPY . ./

# Start application
CMD bash start.sh
