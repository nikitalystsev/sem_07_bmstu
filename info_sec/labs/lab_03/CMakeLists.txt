cmake_minimum_required(VERSION 3.29)
project(lab_03)

set(CMAKE_CXX_STANDARD 20)

include_directories(inc)

add_executable(lab_03
        src/main.cpp
        inc/AES.h
        src/AES.cpp
        inc/CFB.h
        src/CFB.cpp
)
