import os
import re
import subprocess
import json

use_submodule_input = input("Use git submodule? (y/n): ")
use_submodule = (
    False
    if not use_submodule_input
    else (True if use_submodule_input.lower() == "y" else False)
)

cwd = os.path.dirname(os.path.abspath(__file__))

if not use_submodule:
    use_local_fork_input = input("Use local fork? (y/n): ")
    use_local_fork = (
        False
        if not use_local_fork_input
        else (True if use_local_fork_input.lower() == "y" else False)
    )
    if use_local_fork:
        print(
            "NOTE: Remember to create an environment variable called CommonLibSFPath which points to your local fork\n"
        )
        with open(
            os.path.join(cwd, "CMakeLists.txt"), "r", encoding="utf-8"
        ) as cmakelists_file:
            cmakelists = cmakelists_file.read()

        cmakelists = cmakelists.replace(
            'CPMAddPackage("gh:Starfield-Reverse-Engineering/CommonLibSF#main")',
            'add_subdirectory("$ENV{CommonLibSFPath}" CommonLibSF)\n',
        )

        cmakelists = cmakelists.replace(
            "include(${CommonLibSF_SOURCE_DIR}/CommonLibSF/cmake/CommonLibSF.cmake)",
            'include("$ENV{CommonLibSFPath}/CommonLibSF/cmake/CommonLibSF.cmake")',
        )

        with open(
            os.path.join(cwd, "CMakeLists.txt"), "w", encoding="utf-8"
        ) as cmakelists_file:
            cmakelists_file.write(cmakelists)
else:
    print("Using git submodule...\n")
    subprocess.run(
        "git submodule add https://github.com/Starfield-Reverse-Engineering/CommonLibSF extern/CommonLibSF"
    )
    subprocess.run("git submodule update --init -f")

    with open(
        os.path.join(cwd, "CMakeLists.txt"), "r", encoding="utf-8"
    ) as cmakelists_file:
        cmakelists = cmakelists_file.read()

    cmakelists = cmakelists.replace(
        "find_package(CommonLibSF CONFIG REQUIRED)",
        "add_subdirectory(extern/CommonLibSF)\n"
        'include("extern/CommonLibSF/CommonLibSF/cmake/CommonLibSF.cmake")',
    )

    with open(
        os.path.join(cwd, "CMakeLists.txt"), "w", encoding="utf-8"
    ) as cmakelists_file:
        cmakelists_file.write(cmakelists)

project_name = input("Enter project name: ")
author = input("Enter author: ")
pattern = re.compile(r"(?<!^)(?=[A-Z])")
name = pattern.sub("-", project_name).lower()

os.remove(os.path.join(cwd, "README.md"))
os.rename(
    os.path.join(cwd, "contrib", "Config", "PluginName.ini"),
    os.path.join(cwd, "contrib", "Config", f"{project_name}.ini"),
)

with open(
    os.path.join(cwd, "CMakeLists.txt"), "r", encoding="utf-8"
) as cmakelists_file:
    cmakelists = cmakelists_file.read()

cmakelists = cmakelists.replace("PluginName", project_name)
cmakelists = cmakelists.replace("AuthorName", author)
cmakelists = cmakelists.replace("0.0.1", "1.0.0")

with open(
    os.path.join(cwd, "CMakeLists.txt"), "w", encoding="utf-8"
) as cmakelists_file:
    cmakelists_file.write(cmakelists)

with open(
    os.path.join(cwd, "src", "Settings.cpp"), "r", encoding="utf-8"
) as settings_cpp_file:
    settings_cpp = settings_cpp_file.read()

settings_cpp = settings_cpp.replace("PluginName.ini", f"{project_name}.ini")

with open(
    os.path.join(cwd, "src", "Settings.cpp"), "w", encoding="utf-8"
) as settings_cpp_file:
    settings_cpp_file.write(settings_cpp)
