# CommonLibSF Plugin Template

[![C++23](https://img.shields.io/static/v1?label=standard&message=c%2B%2B23&color=blue&logo=c%2B%2B&&logoColor=red&style=flat)](https://en.cppreference.com/w/cpp/compiler_support)
[![Platform](https://img.shields.io/static/v1?label=platform&message=windows&color=dimgray&style=flat&logo=windows)]()
[![Game version](https://img.shields.io/badge/game%20version-1.7.36-orange)]()
[![Test build](https://img.shields.io/github/actions/workflow/status/Starfield-Reverse-Engineering/CLibSFPluginTemplate/testbuild.yml)](https://github.com/Starfield-Reverse-Engineering/CLibSFPluginTemplate/actions/workflows/testbuild.yml)

## Dependencies

- [CMake v3.27+](https://cmake.org/)
- [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/) with C++ workload
- [Python](https://www.python.org/download)
- [LLVM v17.0.0+](https://github.com/llvm/llvm-project/releases)

## License requirements

This template uses CommonLibSF's [GPLv3 with exceptions](https://github.com/Starfield-Reverse-Engineering/CommonLibSF?tab=readme-ov-file#license). Per the license, **you must share the source code of your mod if you use CommonLibSF**. Violation of the license will result in your mod being taken down from the Nexus.

## Setup

This template consumes CommonLibSF as a [CPM](https://github.com/cpm-cmake/CPM.cmake) package, a git submodule, or a local fork. When you run the project setup script, you will be prompted to choose between the three (the default is as a CPM package).

A python script, `project_setup.py`, is provided which automates several housekeeping steps required to get the template development-ready (requires [Python](https://www.python.org/download)). To run the script:

1. Run `cd .\CLibSFPluginTemplate\`
2. Run `py .\project_setup.py`
3. Choose how to consume CommonLibSF
   1. Press `Enter` to use the default of consuming CommonLibSF via CPM
   2. Enter `y` to consume CommonLibSF as a git submodule instead
4. To use a local fork of CommonLibSF instead of the vcpkg port or a git submodule:
   1. Create a Windows environment variable called `CommonLibSFPath` that points to your local fork of CommonLibSF
   2. Enter `y` when the setup script asks if you'd like to use a local fork
5. Enter your project name (in CamelCase)

## Building your project

- Visual Studio should prompt you to generate a CMake cache. Click on `Generate` and wait
- One the CMake cache is generated, build your project
- The `.dll` and `.pdb` files will be placed in `contrib\PluginRelease` or `contrib\PluginDebug` depending on your build configuration

## Build configs

- Two build configs are provided:
  - `Release`: Optimized release build, produces small and fast DLLs with associated PDBs
  - `Debug`: Debug build, produces DLLs and PDBs with full debug info, allowing the use of an interactive debugger

Variants of both of the above configs are provided which use MSVC (`cl/link`) and Clang (`clang-cl/lld-link`) respectively.

## Plugin configuration using an `.ini`

Many CommonLib plugins expose settings through configuration files so that the user can control plugin behavior. This template includes [simpleini](https://github.com/brofield/simpleini) which allows you to read settings from the ini file in `contrib\config` (see `Settings.cpp`).
