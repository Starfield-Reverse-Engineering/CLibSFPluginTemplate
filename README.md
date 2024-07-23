# CommonLibSF Plugin Template

[![C++23](https://img.shields.io/static/v1?label=standard&message=c%2B%2B23&color=blue&logo=c%2B%2B&&logoColor=red&style=flat)](https://en.cppreference.com/w/cpp/compiler_support)
[![Platform](https://img.shields.io/static/v1?label=platform&message=windows&color=dimgray&style=flat&logo=windows)]()
[![Game version](https://img.shields.io/badge/game%20version-1.12.36-orange)]()
[![Test build](https://img.shields.io/github/actions/workflow/status/Starfield-Reverse-Engineering/CLibSFPluginTemplate/testbuild.yml)](https://github.com/Starfield-Reverse-Engineering/CLibSFPluginTemplate/actions/workflows/testbuild.yml)

## License requirements

This template uses CommonLibSF's [GPLv3 with exceptions](https://github.com/Starfield-Reverse-Engineering/CommonLibSF?tab=readme-ov-file#license). Per the license, **you must share the source code of your mod if you use CommonLibSF**. Violation of the license will result in your mod being taken down from the Nexus.

## Setup

This template consumes CommonLibSF as a [CPM](https://github.com/cpm-cmake/CPM.cmake) package, a git submodule, or a local fork. When you run the project setup script, you will be prompted to choose between the three (the default is as a CPM package).

A python script, `project_setup.py`, is provided which automates several housekeeping steps required to get the template development-ready (requires [Python](https://www.python.org/download)). To run the script:

1. If you want to use a local fork of CommonLibSF instead of a submodule, create a Windows environment variable called `CommonLibSFPath` that points to your local fork
2. Run `cd .\CLibSFPluginTemplate\`
3. Run `py .\project_setup.py`
4. Enter your project name (in CamelCase)
5. Choose how to consume CommonLibSF
   1. Press `Enter` to use the default of consuming CommonLibSF via a local fork
   2. Enter `n` to consume CommonLibSF as a git submodule instead

## Building your project

- Select one of the CMake presets (release or debug), configure, and build.
- The .dll and .pdb files will be placed in `contrib\PluginRelease` or `contrib\PluginDebug` depending on your selected preset

## Requirements

- [vcpkg](https://github.com/microsoft/vcpkg)
  - Create a new environment variable called `VCPKG_ROOT` which points to your vcpkg install directory
- [CMake](https://cmake.org/)
- [LLVM](https://github.com/llvm/llvm-project/releases)
- Visual Studio 2022 build tools

## Resources

- [Steamless](https://github.com/atom0s/Steamless/releases)
