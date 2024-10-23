cmake_minimum_required(VERSION 2.8.4)
project(hideme)


set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp  mi_water.cpp mi_memfile.cpp mi2_memfile.cpp  mi2_water.cpp )
add_executable(hideme ${SOURCE_FILES})
TARGET_LINK_LIBRARIES( hideme ${Boost_LIBRARIES} )