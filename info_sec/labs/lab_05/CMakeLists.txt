cmake_minimum_required(VERSION 3.29)
project(lab_05)

set(CMAKE_CXX_STANDARD 20)

include_directories(inc)

add_executable(
        lab_05
        src/main.cpp
        inc/LZW.h
        src/LZW.cpp
        inc/TrieTree.h
        src/TrieTree.cpp
)
