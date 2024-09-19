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

# Choose how to consume CommonLibSF
from_path = input("Use CommonLibSF from path? (Y/n): ")
if from_path == "" or from_path.lower() == "y":
    print(f"Using CommonLibSF from path {environ["CommonLibSFPath"]}")
elif from_path.lower() == "n":
    print("Using CommonLibSF as submodule")
else:
    print("Invalid input")
    exit()

# Update CMakeLists.txt
with open("CMakeLists.txt", "r", encoding="utf-8") as f:
    cmakelists = f.read()

cmakelists = cmakelists.replace("PluginName", project_name)
cmakelists = cmakelists.replace("AuthorName", author)
cmakelists = cmakelists.replace("0.0.1", "1.0.0")

if from_path.lower() == "n":
    cmakelists = cmakelists.replace(
        "add_subdirectory($ENV{CommonLibSFPath} CommonLibSF)",
        "add_subdirectory(extern/CommonLibSF)",
    )
    cmakelists = cmakelists.replace("$ENV{CommonLibSFPath}", "extern/CommonLibSF")

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

# Initialize CommonLibSF submodule if chosen
if from_path.lower() == "n":
    print("\nInitializing CommonLibSF submodule...")
    run(
        [
            "git",
            "submodule",
            "add",
            "https://github.com/Starfield-Reverse-Engineering/CommonLibSF",
            "extern/CommonLibSF",
        ]
    )

    run(["git", "submodule", "update", "--init", "--recursive"])

# Self-destruct
remove(__file__)
