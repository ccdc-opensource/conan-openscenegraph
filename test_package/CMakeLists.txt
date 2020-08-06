cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(${PROJECT_NAME}
    test_package.cpp
    ${CONAN_USER_OPENSCENEGRAPH_openscenegraph_freetype_plugin_source}/FreeTypeFont.cpp
    ${CONAN_USER_OPENSCENEGRAPH_openscenegraph_freetype_plugin_source}/FreeTypeFont.h
    ${CONAN_USER_OPENSCENEGRAPH_openscenegraph_freetype_plugin_source}/FreeTypeLibrary.cpp
    ${CONAN_USER_OPENSCENEGRAPH_openscenegraph_freetype_plugin_source}/FreeTypeLibrary.h
)

target_include_directories(${PROJECT_NAME}
    PRIVATE ${CONAN_USER_OPENSCENEGRAPH_openscenegraph_freetype_plugin_source})
target_link_libraries(${PROJECT_NAME} CONAN_PKG::openscenegraph)
