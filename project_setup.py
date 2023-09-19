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

project_name = input("Enter project name: ")
author = input("Enter author: ")
pattern = re.compile(r"(?<!^)(?=[A-Z])")
name = pattern.sub("-", project_name).lower()

vcpkg_repo = "https://github.com/microsoft/vcpkg"
clibsf_repo = "https://github.com/Starfield-Reverse-Engineering/Starfield-RE-vcpkg"
process1 = subprocess.Popen(["git", "ls-remote", vcpkg_repo], stdout=subprocess.PIPE)
process2 = subprocess.Popen(["git", "ls-remote", clibsf_repo], stdout=subprocess.PIPE)
stdout, stderr = process1.communicate()
sha = re.split(r"\t+", stdout.decode("ascii"))[0]
vcpkg_sha = sha
stdout, stderr = process2.communicate()
sha = re.split(r"\t+", stdout.decode("ascii"))[0]
clibsf_sha = sha

os.remove(os.path.join(cwd, "README.md"))
os.rename(
    os.path.join(cwd, "contrib", "Config", "PluginName.ini"),
    os.path.join(cwd, "contrib", "Config", f"{project_name}.ini"),
)

with open(os.path.join(cwd, "vcpkg.json"), "r", encoding="utf-8") as vcpkg_json_file:
    vcpkg_json = json.load(vcpkg_json_file)

vcpkg_json["name"] = name
vcpkg_json["version-semver"] = "1.0.0"

vcpkg_json["vcpkg-configuration"]["default-registry"]["baseline"] = vcpkg_sha
vcpkg_json["vcpkg-configuration"]["registries"][0]["baseline"] = clibsf_sha

with open(os.path.join(cwd, "vcpkg.json"), "w", encoding="utf-8") as vcpkg_json_file:
    json.dump(vcpkg_json, vcpkg_json_file, indent=2)

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

if not use_submodule:
    print("Using vcpkg port...\n")
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
        "add_subdirectory(extern/CommonLibSF)\n\n"
        'find_path(SPDLOG_DIR "spdlogConfig.cmake")\n'
        'find_path(FMT_DIR "fmt-config.cmake")\n'
        'find_path(XBYAK_DIR "xbyak-config.cmake")',
    )

    cmakelists = cmakelists.replace("add_commonlibsf_plugin", "target_link_libraries")
    cmakelists = cmakelists.replace("AUTHOR AuthorName", "PRIVATE")
    cmakelists = cmakelists.replace(
        "SOURCES ${headers} ${sources}", "  CommonLibSF::CommonLibSF"
    )

    with open(
        os.path.join(cwd, "CMakeLists.txt"), "w", encoding="utf-8"
    ) as cmakelists_file:
        cmakelists_file.write(cmakelists)

    with open(
        os.path.join(cwd, "vcpkg.json"), "r", encoding="utf-8"
    ) as vcpkg_json_file:
        vcpkg_json = json.load(vcpkg_json_file)

    vcpkg_json["dependencies"] = ["simpleini"]

    with open(
        os.path.join(cwd, "vcpkg.json"), "w", encoding="utf-8"
    ) as vcpkg_json_file:
        json.dump(vcpkg_json, vcpkg_json_file, indent=2)

    with open(
        os.path.join(cwd, "build-clibsf.bat"), "w+", encoding="utf-8"
    ) as buildscript:
        clibsf_dir = os.path.join(cwd, "extern", "CommonLibSF", "CommonLibSF")
        build_dir = os.path.join(clibsf_dir, "build")
        buildscript.write(
            f"cd {clibsf_dir}\n"
            f'cmake -B "{build_dir}" -S "{clibsf_dir}" --preset=build-release-msvc-ninja\n'
            f'cmake --build "{build_dir}" --preset=release-msvc-ninja',
        )
