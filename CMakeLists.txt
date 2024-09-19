cmake_minimum_required(VERSION 3.30)
message("Using toolchain file ${CMAKE_TOOLCHAIN_FILE}.")

project(
  PluginName
  VERSION 0.0.1
  LANGUAGES CXX
)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_DEBUG OFF)
set(CMAKE_OPTIMIZE_DEPENDENCIES ON)

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cmake/version.rc.in
  ${CMAKE_CURRENT_BINARY_DIR}/version.rc
  @ONLY
)

# Add sources
file(
  GLOB_RECURSE
  sources
  ${CMAKE_CURRENT_SOURCE_DIR}/include/*.h
  ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
  ${CMAKE_CURRENT_BINARY_DIR}/version.rc
)
list(REMOVE_ITEM headers ${CMAKE_CURRENT_SOURCE_DIR}/include/PCH.h)

source_group(
  TREE ${CMAKE_CURRENT_SOURCE_DIR}
  FILES ${sources}
)

# Add CommonLibSF
set(BUILD_TESTS OFF)
add_subdirectory($ENV{CommonLibSFPath} CommonLibSF)
include($ENV{CommonLibSFPath}/cmake/CommonLibSF.cmake)

add_commonlibsf_plugin(
  ${PROJECT_NAME}
  AUTHOR AuthorName
  SOURCES ${headers} ${sources}
)

add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

# Add dependencies
find_path(SIMPLEINI_INCLUDE_DIRS "SimpleIni.h")

target_include_directories(
  ${PROJECT_NAME}
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${SIMPLEINI_INCLUDE_DIRS}
)

target_precompile_headers(
  ${PROJECT_NAME}
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include/PCH.h
  ${SIMPLEINI_INCLUDE_DIRS}/SimpleIni.h
)

if(CMAKE_BUILD_TYPE STREQUAL Debug)
  set(BUILD_NAME Debug)
else()
  set(BUILD_NAME Release)
endif()

add_custom_command(
  TARGET ${PROJECT_NAME}
  POST_BUILD
  COMMAND
  ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/skse/plugins
  COMMAND
  ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${PROJECT_NAME}> ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/skse/plugins
  COMMAND
  ${CMAKE_COMMAND} -E copy $<TARGET_PDB_FILE:${PROJECT_NAME}> ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/skse/plugins
  COMMAND
  ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Config/${PROJECT_NAME}.ini ${CMAKE_CURRENT_SOURCE_DIR}/contrib/Plugin${BUILD_NAME}/skse/plugins
)

file(GLOB_RECURSE OUTPUT_DLLS ${CMAKE_CURRENT_SOURCE_DIR}/contrib/**/*.dll)
file(GLOB_RECURSE OUTPUT_PDBS ${CMAKE_CURRENT_SOURCE_DIR}/contrib/**/*.pdb)

set_property(
  TARGET ${PROJECT_NAME}
  APPEND PROPERTY ADDITIONAL_CLEAN_FILES ${OUTPUT_DLLS} ${OUTPUT_PDBS}
)
