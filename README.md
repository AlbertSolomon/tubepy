<div align="center">
<h1>
<img width="160" height="150" src="assets/new_tubepy_logo.png"/>
</h1>
<h1>TUBEPY</h1> 
</div>
<p align="center"> <img src="https://camo.githubusercontent.com/3dbcfa4997505c80ef928681b291d33ecfac2dabf563eb742bb3e269a5af909c/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f496c65726961796f2f6d61726b646f776e2d6261646765733f7374796c653d666f722d7468652d6261646765"> <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"> <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"><img src="https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0"><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white"> <img src="https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white"><br><img src="https://img.shields.io/badge/Status-Active-green.svg"> </p>



> A simple desktop Youtube video downloader in python.

## Version 1

> This is an application which uses the [custom tkinter](https://github.com/TomSchimansky/CustomTkinter) library to render GUI widgets and [pytube](https://pytube.io/en/latest/) library to download youtube files.

## Installation

To install Tubepy, follow the steps below:

1. Make sure you have Python 3.10.8 or higher installed on your machine.
2. Clone or fork the project from the GitHub repository.
3. Create a virtual environment in the root directory of the project. You can find more information about virtual environments [here](https://www.geeksforgeeks.org/python-virtual-environment/).
4. Activate the virtual environment and run the following command to install the required dependencies:

```bash
    pip install -r requirements.txt 
```

5. To run the application on Windows, execute the following command

```bash
    python tubepy/setup.py 
```

On Unix-based systems, run the command below:

```bash
    python3 tubepy/setup.py 
```

Ensure that you have ``tkinter`` installed while working on Linux by utilizing the package manager offered by your current distribution.

#### fedora

```bash 
    sudo dnf install python3-tkinter
```

#### Ubuntu

```bash
    sudo apt-get install python3-tk
```

### Building Binaries

Tubepy leverages the cx_freeze library to produce binaries, which can be built by running the command below:

```bash
    python setup.py build # which is present in the root directory.
```

Keep in mind that you might need to provide extra information or configuration options to the ``setup.py`` file for a more personalized build process.

### Installer Script

Before running ``tubepy_installer_exe_script.iss``, make sure you have Inno Setup installed. Open the script in the editor, modify the directory paths to match your project, and hit run. Happy installing!

## Contributions

> For more information on how to contribute please read the CONTRIBUTIONS.md file.

## Screenshots

Home page
![Home Page](https://github.com/AlbertSolomon/tubepy/blob/main/assets/screenshots/home%20page.png)

About page
![About Page](https://github.com/AlbertSolomon/tubepy/blob/main/assets/screenshots/about%20page.png)

## Demo

![Demo](https://github.com/AlbertSolomon/tubepy/blob/main/assets/demo.gif)

## Troubleshooting

If you face any errors while installing the software, please ensure that you have installed Python 3.10.8 or a newer version on your system and that you have correctly installed all the necessary dependencies in the ``requirements.txt``. If the error persists, you can raise an issue [here](https://github.com/AlbertSolomon/tubepy/issues) or start a discussion in the [discussion section](https://github.com/AlbertSolomon/tubepy/discussions).

> Enjoy using Tubepy to download your favorite YouTube videos! 🍾.

<p align="center"><a href="https://github.com/AlbertSolomon/tubepy#"><img src="https://superagi.com/wp-content/uploads/2023/05/backToTopButton.png" alt="Back to top" height="29"/></a></p>
