cmake_minimum_required(VERSION 3.24)
project(lab_01)

set(CMAKE_CXX_STANDARD 20)

include_directories(inc)

add_executable(lab_01
        src/main.cpp
        inc/enigma.h
        src/enigma.cpp
        inc/encoder.h
        src/encoder.cpp)
