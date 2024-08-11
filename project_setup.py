import os
import re
import subprocess
import json
import shutil
import stat


def onexc(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


# Remove original git repo
if os.path.isdir(".git"):
    shutil.rmtree(".git", onexc=onexc)

# Remove README.md
os.remove("README.md")

# Get project name and author
project_name = input("Enter project name: ")
author = input("Enter author: ")
print()

# Choose how to consume CommonLibSSE-NG
from_path = input("Use CommonLibSF from path? (Y/n): ")
if from_path == "" or from_path.lower() == "y":
    print(f"Using CommonLibSF from path {os.environ["CommonLibSFPath"]}")
elif from_path.lower() == "n":
    print("Using CommonLibSF as submodule")
else:
    print("Invalid input")
    exit()

# Update vcpkg.json
pattern = re.compile(r"(?<!^)(?=[A-Z])")

with open("vcpkg.json", "r", encoding="utf-8") as vcpkg_json_file:
    vcpkg_json = json.load(vcpkg_json_file)

name = pattern.sub("-", project_name).lower()
vcpkg_json["name"] = name
vcpkg_json["version-semver"] = "1.0.0"

with open("vcpkg.json", "w", encoding="utf-8") as vcpkg_json_file:
    json.dump(vcpkg_json, vcpkg_json_file, indent=2)

# Update CMakeLists.txt
with open("CMakeLists.txt", "r", encoding="utf-8") as cmakelists_file:
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

with open("CMakeLists.txt", "w", encoding="utf-8") as cmakelists_file:
    cmakelists_file.write(cmakelists)

# Rename ini file
os.rename(
    os.path.join("contrib", "Config", "PluginName.ini"),
    os.path.join("contrib", "Config", f"{project_name}.ini"),
)

# Update Settings.cpp
with open(
    os.path.join("src", "Settings.cpp"), "r", encoding="utf-8"
) as settings_cpp_file:
    settings_cpp = settings_cpp_file.read()

settings_cpp = settings_cpp.replace("PluginName.ini", f"{project_name}.ini")

with open(
    os.path.join("src", "Settings.cpp"), "w", encoding="utf-8"
) as settings_cpp_file:
    settings_cpp_file.write(settings_cpp)

# Update vcpkg.json builtin-baseline
print("Updating vcpkg.json...")
subprocess.run(
    [f"{os.environ["VCPKG_ROOT"]}\\vcpkg.exe", "x-update-baseline"], shell=True
)
print()

# Initialize empty git repo
subprocess.run(["git", "init"])

# Initialize CommonLibSF submodule if chosen
if from_path.lower() == "n":
    print("\nInitializing CommonLibSF submodule...")
    subprocess.run(
        [
            "git",
            "submodule",
            "add",
            "https://github.com/Starfield-Reverse-Engineering/CommonLibSF",
            "extern/CommonLibSF",
        ]
    )

    subprocess.run(["git", "submodule", "update", "--init", "--recursive"])

# Self-destruct
os.remove(__file__)
