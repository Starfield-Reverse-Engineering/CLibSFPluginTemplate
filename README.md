# CommonLibSF Plugin Template

## Setup

- Clone the repository
- Optional:
  - Run `cd .\CLibSFPluginTemplate\`
  - Run `py .\project_setup.py\` (requires [Python 3.12+](https://www.python.org/download/pre-releases/))
  - Enter your project name (in CamelCase)
  - `project_setup.py` just does a few convenience things like setting the project name in `vcpkg.json` and `CMakeLists.txt`

## Building your project

- Visual Studio should prompt you to generate a CMake cache. Click on `Generate` and wait
- One the CMake cache is generated, build your project
- The .dll and .pdb files will be placed in `contrib\PluginRelease` or `contrib\PluginDebug` depending on your build configuration

## Build configs

- Two build configs are provided:
  - `Release`: Optimized release build, produces small and fast DLLs with associated PDBs
  - `Debug`: Debug build, produces DLLs and PDBs with full debug info, allowing the use of an interactive debugger

## Dependencies

- [vcpkg v2023.08.09+](https://github.com/microsoft/vcpkg/releases)
  - Create a new Windows environment variable called `VCPKG_ROOT` which points to your vcpkg install directory
- [CMake v3.27+](https://cmake.org/)
- [LLVM v16.0.6+](https://github.com/llvm/llvm-project/releases)
- Visual Studio 2022 with C++ workload
