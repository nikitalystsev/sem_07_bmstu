cmake_minimum_required(VERSION 3.29)
project(lab_02)

set(CMAKE_CXX_STANDARD 20)

include_directories(inc)

add_executable(lab_02
        src/main.cpp
        src/DES.cpp
        inc/PCBC.h
        src/PCBC.cpp)
