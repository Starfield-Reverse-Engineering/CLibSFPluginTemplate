import os
import re
import subprocess
import json
import shutil
import stat

cwd = os.path.dirname(os.path.abspath(__file__))


def onexc(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


if os.path.isdir(os.path.join(cwd, ".git")):
    shutil.rmtree(os.path.join(cwd, ".git"), onexc=onexc)
    subprocess.Popen(["git", "init"]).communicate()

os.remove(os.path.join(cwd, "README.md"))

project_name = input("Enter project name: ")
author = input("Enter author: ")
print()

from_path = input("Use CommonLibSF from path? (Y/n): ")
if from_path == "" or from_path.lower() == "y":
    print(f"Using CommonLibSF from path {os.environ["CommonLibSFPath"]}")
elif from_path.lower() == "n":
    print("Using CommonLibSF as submodule")
else:
    print("Invalid input")
    exit()

pattern = re.compile(r"(?<!^)(?=[A-Z])")

with open(os.path.join(cwd, "vcpkg.json"), "r", encoding="utf-8") as vcpkg_json_file:
    vcpkg_json = json.load(vcpkg_json_file)

name = pattern.sub("-", project_name).lower()
vcpkg_json["name"] = name
vcpkg_json["version-semver"] = "1.0.0"

with open(os.path.join(cwd, "vcpkg.json"), "w", encoding="utf-8") as vcpkg_json_file:
    json.dump(vcpkg_json, vcpkg_json_file, indent=2)

with open(
    os.path.join(cwd, "CMakeLists.txt"), "r", encoding="utf-8"
) as cmakelists_file:
    cmakelists = cmakelists_file.read()

cmakelists = cmakelists.replace("PluginName", project_name)
cmakelists = cmakelists.replace("AuthorName", author)
cmakelists = cmakelists.replace("0.0.1", "1.0.0")

if from_path.lower() == "n":
    cmakelists = cmakelists.replace(
        "add_subdirectory($ENV{CommonLibSFPath} CommonLibSF)",
        "add_subdirectory(extern/CommonLibSF)",
    )
    cmakelists = cmakelists.replace("$ENV{CommonLibSFPath}", "extern/CommonLibSF")

with open(
    os.path.join(cwd, "CMakeLists.txt"), "w", encoding="utf-8"
) as cmakelists_file:
    cmakelists_file.write(cmakelists)

os.rename(
    os.path.join(cwd, "contrib", "Config", "PluginName.ini"),
    os.path.join(cwd, "contrib", "Config", f"{project_name}.ini"),
)

with open(
    os.path.join(cwd, "src", "Settings.cpp"), "r", encoding="utf-8"
) as settings_cpp_file:
    settings_cpp = settings_cpp_file.read()

settings_cpp = settings_cpp.replace("PluginName.ini", f"{project_name}.ini")

with open(
    os.path.join(cwd, "src", "Settings.cpp"), "w", encoding="utf-8"
) as settings_cpp_file:
    settings_cpp_file.write(settings_cpp)

print("Updating vcpkg.json...")
subprocess.Popen(
    [f"{os.environ["VCPKG_ROOT"]}\\vcpkg.exe", "x-update-baseline"], cwd=cwd, shell=True
).communicate()
print()

subprocess.Popen(["git", "init"]).communicate()

if from_path.lower() == "n":
    print("\nInitializing CommonLibSF submodule...")
    subprocess.Popen(
        [
            "git",
            "submodule",
            "add",
            "https://github.com/Starfield-Reverse-Engineering/CommonLibSF",
            "extern/CommonLibSF",
        ],
        cwd=cwd,
    ).communicate()

    subprocess.Popen(
        ["git", "submodule", "update", "--init", "--recursive"], cwd=cwd
    ).communicate()
