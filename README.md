# CommonLibSF Plugin Template

[![C++23](https://img.shields.io/static/v1?label=standard&message=c%2B%2B23&color=blue&logo=c%2B%2B&&logoColor=red&style=flat)](https://en.cppreference.com/w/cpp/compiler_support)
[![Platform](https://img.shields.io/static/v1?label=platform&message=windows&color=dimgray&style=flat&logo=windows)]()
[![Game version](https://img.shields.io/badge/game%20version-1.14.70-orange)]()

## License requirements

This template uses CommonLibSF's [GPLv3 with exceptions](https://github.com/Starfield-Reverse-Engineering/CommonLibSF?tab=readme-ov-file#license). Per the license, **you must share the source code of your mod if you use CommonLibSF**. Violation of the license will result in your mod being taken down from the Nexus.

## Setup

- Clone the repository
- Run `cd CLibSFPluginTemplate`
- Run `py project_setup.py` (requires [Python 3.12+](https://www.python.org/download/pre-releases/))

**NOTE**: You should run `vcpkg x-update-baseline` (in the project's root directory) often to make sure that vcpkg is fetching the latest versions of CommonLibSF and other dependencies

## Building your project

- Select one of the CMake presets (release or debug), configure, and build.
- The .dll and .pdb files will be placed in `contrib\PluginRelease` or `contrib\PluginDebug` depending on your selected preset

## Requirements

- [vcpkg](https://github.com/microsoft/vcpkg)
  - Create a new environment variable called `VCPKG_ROOT` which points to your vcpkg install directory
- [CMake](https://cmake.org)
- [LLVM](https://github.com/llvm/llvm-project/releases)
- Visual Studio 2022 build tools

## Resources

- [Steamless](https://github.com/atom0s/Steamless/releases)
