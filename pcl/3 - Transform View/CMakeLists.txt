cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(transform_from_viewpoint)

find_package(PCL 1.2 REQUIRED)

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_executable (transform_from_viewpoint transform_from_viewpoint.cpp)
target_link_libraries (transform_from_viewpoint ${PCL_LIBRARIES})
