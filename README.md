# CommonLibSF Plugin Template

[![C++23](https://img.shields.io/static/v1?label=standard&message=c%2B%2B23&color=blue&logo=c%2B%2B&&logoColor=red&style=flat)](https://en.cppreference.com/w/cpp/compiler_support)
[![Platform](https://img.shields.io/static/v1?label=platform&message=windows&color=dimgray&style=flat&logo=windows)]()
[![Game version](https://img.shields.io/badge/game%20version-1.7.29-orange)]()
[![Test build](https://img.shields.io/github/actions/workflow/status/Starfield-Reverse-Engineering/CLibSFPluginTemplate/testbuild.yml)](https://github.com/Starfield-Reverse-Engineering/CLibSFPluginTemplate/actions/workflows/testbuild.yml)

## Setup

There are a few housekeeping tasks to do before you get started developing your plugin.

### Automatic

A python script, `project_setup.py`, is provided which automates the steps in [the section below](#manual) (requires [Python 3.12+](https://www.python.org/download/pre-releases/))\*. To run the script:

1. Run `cd .\CLibSFPluginTemplate\`
2. Run `py .\project_setup.py\`
3. Enter your project name (in CamelCase)

**\*NOTE**: If you're using Python 3.11 or below, change `onexc=onexc` to `onerror=onexc` in lines 31 and 33 in `project_setup.py`

### Manual

1. Clone the repository
2. Set the `"name"` and `"version-semver"` fields in `vcpkg.json`
3. Update the `"baseline"` entries to the latest commits in both registries in `vcpkg.json`
   - Follow the links in the `"repository"` fields and copy-paste the hash of the latest commit in each repository
4. Set the name and version of your plugin in `CMakeLists.txt`
5. Change `"AuthorName"` in `CMakeLists.txt` to your name
6. Set the name of `contrib/Config/PluginName.ini` to the name of your plugin
7. Edit the `ini.LoadFile()` call in `src/Settings.cpp` to load the renamed ini from step 6

## Building your project

- Visual Studio should prompt you to generate a CMake cache. Click on `Generate` and wait
- One the CMake cache is generated, build your project
- The `.dll` and `.pdb` files will be placed in `contrib\PluginRelease` or `contrib\PluginDebug` depending on your build configuration

## Build configs

- Two build configs are provided:
  - `Release`: Optimized release build, produces small and fast DLLs with associated PDBs
  - `Debug`: Debug build, produces DLLs and PDBs with full debug info, allowing the use of an interactive debugger

## Dependencies

- [CMake v3.27+](https://cmake.org/)
- [vcpkg v2023.08.09+](https://github.com/microsoft/vcpkg/releases)
  - Create a new Windows environment variable called `VCPKG_ROOT` which points to your vcpkg install directory
- [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/) with C++ workload
- [LLVM v17.0.0+](https://github.com/llvm/llvm-project/releases) (not really a dependency but nice to have)
