cmake_minimum_required(VERSION 3.27)
message("Using toolchain file ${CMAKE_TOOLCHAIN_FILE}.")

########################################################################################################################
## Define project
########################################################################################################################
project(
  PluginName
  VERSION 0.0.1
  LANGUAGES CXX
)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_DEBUG OFF)

include(GNUInstallDirs)

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cmake/version.rc.in
  ${CMAKE_CURRENT_BINARY_DIR}/version.rc
  @ONLY
)

set(PUBLIC_HEADER_DIR "${CMAKE_CURRENT_SOURCE_DIR}/include/${PROJECT_NAME}")

set(
  headers
    include/Utility.h
)

set(
  sources
    src/Main.cpp
    src/Settings.cpp
    src/Hooks.cpp

    ${CMAKE_CURRENT_BINARY_DIR}/version.rc
)

source_group(
  TREE ${CMAKE_CURRENT_SOURCE_DIR}
  FILES ${headers} ${sources}
)

########################################################################################################################
## Configure target DLL
########################################################################################################################
find_package(CommonLibSF CONFIG REQUIRED)

add_commonlibsf_plugin(
  ${PROJECT_NAME}
  AUTHOR AuthorName
  SOURCES ${headers} ${sources}
)

add_library("${PROJECT_NAME}::${PROJECT_NAME}" ALIAS "${PROJECT_NAME}")

find_path(SIMPLEINI_INCLUDE_DIRS "SimpleIni.h")

target_include_directories(
  ${PROJECT_NAME}
  PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/src>
    $<INSTALL_INTERFACE:src>
    ${SIMPLEINI_INCLUDE_DIRS}
)

target_include_directories(
  ${PROJECT_NAME}
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)

target_precompile_headers(
  ${PROJECT_NAME}
  PRIVATE
    include/PCH.h
    ${SIMPLEINI_INCLUDE_DIRS}/SimpleIni.h
)

install(
  DIRECTORY "${PUBLIC_HEADER_DIR}"
  DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)

install(
  TARGETS ${PROJECT_NAME}
  DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)

########################################################################################################################
## Automatic plugin deployment
########################################################################################################################
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(BUILD_NAME "Debug")
else()
  set(BUILD_NAME "Release")
endif()

add_custom_command(
  TARGET ${PROJECT_NAME}
  POST_BUILD
  COMMAND
    ${CMAKE_COMMAND} -E make_directory "${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/sfse/plugins"
)
add_custom_command(
  TARGET ${PROJECT_NAME}
  POST_BUILD
  COMMAND
    ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${PROJECT_NAME}> "${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/sfse/plugins"
)
add_custom_command(
  TARGET ${PROJECT_NAME}
  POST_BUILD
  COMMAND
    ${CMAKE_COMMAND} -E copy $<TARGET_PDB_FILE:${PROJECT_NAME}> "${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/sfse/plugins"
)

file(GLOB_RECURSE OUTPUT_DLLS "${CMAKE_CURRENT_SOURCE_DIR}/contrib/**/*.dll")
file(GLOB_RECURSE OUTPUT_PDBS "${CMAKE_CURRENT_SOURCE_DIR}/contrib/**/*.pdb")

set_property(
  TARGET ${PROJECT_NAME}
  APPEND PROPERTY ADDITIONAL_CLEAN_FILES "${OUTPUT_DLLS}"
)
set_property(
  TARGET ${PROJECT_NAME}
  APPEND PROPERTY ADDITIONAL_CLEAN_FILES "${OUTPUT_PDBS}"
)
