<div align="center">
<h1>
<img width="160" height="150" src="assets/new_tubepy_logo.png"/>
</h1>
<h1>TUBEPY</h1> 
</div>
<p align="center"> <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg"> <img src="https://img.shields.io/badge/Python-3.10.8-blue.svg"> <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20MacOS-blue.svg"> <img src="https://img.shields.io/badge/Status-Active-green.svg"> </p>

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

### Building Binaries

Tubepy leverages the cx_freeze library to produce binaries, which can be built by running the command below:

```bash
    python setup.py build
```

Keep in mind that you might need to provide extra information or configuration options to the ``setup.py`` file for a more personalized build process.

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

> If you face any errors while installing the software, ensure that you have installed Python 3.10.8 or a newer version on your system and that you have correctly installed all the necessary dependencies in the ``requirements.txt``. If the error persists, you can raise an issue [here](https://github.com/AlbertSolomon/tubepy/issues) or start a discussion in the [discussion section](https://github.com/AlbertSolomon/tubepy/discussions).

Enjoy using Tubepy to download your favorite YouTube videos! 🍾.
