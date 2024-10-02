import stat
from os import W_OK, access, chmod, environ, remove, rename
from os.path import isdir, join
from shutil import rmtree
from subprocess import run


def onexc(func, path, exc_info):
    if not access(path, W_OK):
        chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


# Remove original git repo
if isdir(".git"):
    rmtree(".git", onexc=onexc)

# Remove README.md
remove("README.md")

# Get project name and author
project_name = input("Enter project name: ")
author = input("Enter author: ")
print()

# Update CMakeLists.txt
with open("CMakeLists.txt", "r", encoding="utf-8") as f:
    cmakelists = f.read()

cmakelists = cmakelists.replace("PluginName", project_name)
cmakelists = cmakelists.replace("AuthorName", author)
cmakelists = cmakelists.replace("0.0.1", "1.0.0")

with open("CMakeLists.txt", "w", encoding="utf-8") as f:
    f.write(cmakelists)

# Rename ini file
rename(
    join("contrib", "Config", "PluginName.ini"),
    join("contrib", "Config", f"{project_name}.ini"),
)

# Update Settings.cpp
with open(join("src", "Settings.cpp"), "r", encoding="utf-8") as f:
    settings_cpp = f.read()

settings_cpp = settings_cpp.replace("PluginName.ini", f"{project_name}.ini")

with open(join("src", "Settings.cpp"), "w", encoding="utf-8") as f:
    f.write(settings_cpp)

# Update baselines
print("Updating vcpkg.json baselines...")
run([f"{environ["VCPKG_ROOT"]}/vcpkg.exe", "x-update-baseline"])
print()

# Initialize empty git repo
run(["git", "init"])

# Self-destruct
remove(__file__)
