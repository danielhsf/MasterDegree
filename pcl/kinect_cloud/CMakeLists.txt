cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(kinect_cloud)

find_package(PCL 1.8 REQUIRED)

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_executable (kinect_cloud kinect_cloud.cpp)
target_link_libraries (kinect_cloud ${PCL_LIBRARIES}) 
