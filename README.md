# CommonLibSF Plugin Template

## Setup

1. Clone the repository
2. Set the `"name"` and `"version-semver"` fields in `vcpkg.json`
3. Update the `"baseline"` entries to the latest commits in both registries in `vcpkg.json`
   - Follow the links in the `"repository"` fields and copy-paste the hash of the latest commit in each repository
4. Set the name and version of your plugin in `CMakeLists.txt`
5. Set the `Author` variable in `cmake/Plugin.h.in` to your name
6. Set the name of `contrib/Config/PluginName.ini` to the name of your plugin
7. Edit the `ini.LoadFile()` call in `src/Settings.cpp` to load the renamed ini from step 6

A python script, `project_setup.py`, is provided which automates the above steps (requires [Python 3.12+](https://www.python.org/download/pre-releases/)). To run the script:

1. Run `cd .\CLibSFPluginTemplate\`
2. Run `py .\project_setup.py\`
3. Enter your project name (in CamelCase)

## Building your project

- Visual Studio should prompt you to generate a CMake cache. Click on `Generate` and wait
- One the CMake cache is generated, build your project
- The `.dll` and `.pdb` files will be placed in `contrib\PluginRelease` or `contrib\PluginDebug` depending on your build configuration

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
