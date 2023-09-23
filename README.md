# CommonLibSF Plugin Template

[![C++23](https://img.shields.io/static/v1?label=standard&message=c%2B%2B23&color=blue&logo=c%2B%2B&&logoColor=red&style=flat)](https://en.cppreference.com/w/cpp/compiler_support)
[![Platform](https://img.shields.io/static/v1?label=platform&message=windows&color=dimgray&style=flat&logo=windows)]()
[![Game version](https://img.shields.io/badge/game%20version-1.7.29-orange)]()
[![Test build](https://img.shields.io/github/actions/workflow/status/Starfield-Reverse-Engineering/CLibSFPluginTemplate/testbuild.yml)](https://github.com/Starfield-Reverse-Engineering/CLibSFPluginTemplate/actions/workflows/testbuild.yml)

## Setup

This template consumes CommonLibSF either as a vcpkg port or as a git submodule. When you run the project setup script, you will be prompted to choose between the two (the default is via vcpkg).

A python script, `project_setup.py`, is provided which automates several housekeeping steps required to get the template development-ready (requires [Python](https://www.python.org/download)). To run the script:

1. Run `cd .\CLibSFPluginTemplate\`
2. Run `py .\project_setup.py`
3. Choose how to consume CommonLibSF
   1. Press `Enter` to use the default of consuming CommonLibSF via vcpkg
   2. Enter `y` to consume CommonLibSF as a git submodule instead
4. Enter your project name (in CamelCase)

## Building your project

- Visual Studio should prompt you to generate a CMake cache. Click on `Generate` and wait
- One the CMake cache is generated, build your project
- The `.dll` and `.pdb` files will be placed in `contrib\PluginRelease` or `contrib\PluginDebug` depending on your build configuration

## Build configs

- Two build configs are provided:
  - `Release`: Optimized release build, produces small and fast DLLs with associated PDBs
  - `Debug`: Debug build, produces DLLs and PDBs with full debug info, allowing the use of an interactive debugger

## Plugin configuration using an `.ini`

Many CommonLib plugins expose settings through configuration files so that the user can control plugin behavior. This template includes [simpleini](https://github.com/brofield/simpleini) which allows you to read settings from the ini file in `contrib\config` (see `Settings.cpp`).

## License requirements

This template uses CommonLibSF's GPLv3 with exceptions. Per the license, **you must share the source code of your mod if you use CommonLibSF**. Violation of the license will result in your mod being taken down from the Nexus.

## Dependencies

- [CMake v3.27+](https://cmake.org/)
- [vcpkg v2023.08.09+](https://github.com/microsoft/vcpkg/releases)
  - Create a new Windows environment variable called `VCPKG_ROOT` which points to your vcpkg install directory
- [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/) with C++ workload
- [Python](https://www.python.org/download)
- [LLVM v17.0.0+](https://github.com/llvm/llvm-project/releases) (not really a dependency but nice to have)
