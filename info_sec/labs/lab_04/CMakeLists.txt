cmake_minimum_required(VERSION 3.29)
project(lab_04)

set(CMAKE_CXX_STANDARD 20)

include_directories(inc)

add_executable(
        lab_04
        src/main.cpp
        src/RSA.cpp
        inc/RSA.h
        inc/SHA1.h
        src/SHA1.cpp
)

target_link_libraries(lab_04 -lgmp -lgmpxx)