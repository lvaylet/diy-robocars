cmake_minimum_required(VERSION 2.8.3)
project(pwm_msgs)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  std_msgs
)

# include_directories(include)

add_message_files(
  DIRECTORY msg
  FILES
  DutyCyclePercent.msg
  DutyCycleValue.msg
  DutyCycle.msg
  SinglePinDutyCycle.msg
  MultiPinDutyCycle.msg
)

add_service_files(
  DIRECTORY srv
  FILES
  SetDutyCycle.srv
  SetMultiPinDutyCycle.srv
  SetSinglePinDutyCycle.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  # INCLUDE_DIRS include
  CATKIN_DEPENDS message_runtime std_msgs
)

install(
  DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  FILES_MATCHING PATTERN "*.h"
)

# if (CATKIN_ENABLE_TESTING)
#   add_subdirectory(test)
# endif()
