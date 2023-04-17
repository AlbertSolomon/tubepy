import sys

from cx_Freeze import Executable, setup

packages = ["tkinter", "customtkinter", "tubepy", "pytube"]

# Add 'tubepy' to the path to allow Python to import modules from it at runtime
sys.path.append("tubepy")

# Define any extra files or directories to include in the build
includefiles = [
    "tubepy/",
    "utilities/",
    "assets/",
]


# Define the build options
build_options = {
    "packages": packages,
    "excludes": ["requirements.txt", ".github", "assets/screenshots/", "assets/demo.gifdemo.gif"],
    "include_files": includefiles,
}

# Define the executablesy
base = "Win32GUI" if sys.platform == "win32" else None
executables = [Executable("tubepy/setup.py", base=base, target_name="tubepy.msi")]

# Define the setup parameters
setup(
    name="tubepy",
    version="1.0.0-beta",
    description="YouTube video downloader in python 😎",
    options={"build_exe": build_options},
    executables=executables,
)
