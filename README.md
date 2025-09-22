### Welcome!
To play Minesweeper, enter either of the *"dist-windows", "dist-linux", or "dist-mac"* folders and run the executable inside.
It should not need any external dependencies. 

Alternatively, you can also run the following command from the project's root directory (which may require the installation of additional dependencies, but will likely work with a much larger variety of configurations):
`python -m src.main` 

As the provided executables are not guaranteed to work across all devices, this command is the best way to ensure that the program will function correctly. 

### Dependencies:
- Python 3
- curses (Linux) / windows-curses (Windows)
- Standard libraries: enum, platform, random
- pyinstaller (if you are intending to build the project)
- pytest (if you're interesting in running tests)

### Terminal requirements
- For mouse input, your terminal must support curses mouse functionality. Otherwise, you'll only be able to use the keyboard interface.
- Our flag icon uses a fancy unicode code point, so if you're missing some rendering support it may appear as a missing character.
- Your terminal needs to have a properly setup terminfo database.
  - This should not be an issue, as most terminals should be configured correctly by default. However, if you have an improperly configured terminal (or a terminal configuration that isn't compatible with the provided executable), the program will crash due to being unable to initialize the user interface. This issue occurs most often in the Linux builds. If this happens, then you must rebuild your executable by following the instructions below in the "How to build" section or by acquiring the dependencies and running through python directly.
- On MacOS devices, Apple's security software may prevent you from running the executable. In this case, you may need to build the app yourself following the same instructions below or overwrite permissions.

This program has been verified and tested using tmux, windows terminal, and Alacritty, but may depend on 
the operating system in use and if all software has been updated. Windows 11 is the recommended
operating system for running the executable, Linux and MacOS are more likely to require a new build from scratch. 
Linux is the preferred platform for builds or for running the program using python directly due to native curses support
and easier environment management. 

### How to build
Depending on your platform (you will need to have the dependencies), run the make-linux.sh, make-windows.bat, or make-mac.sh script.
The dist-\<os\> folders contain the executables. The build-\<os\> folders contain temporary build files, and the spec-\<os\> folders 
contain specification files used by pyinstaller. The resulting executable should be self-contained with all the necessary dependencies, but if
you run into issues try rebuilding it. The provided executables are not guranteed to work across all devices. 

If you do not have pyinstaller, you can install it with pip using the following command: `pip install pyinstaller`

### Other Repository details
- __src__: For our program's source files. Within src, see the __tui__ folder for frontend-specific files. 
  - Note that this repository uses python's module structure (seen in the "-m" in the command given above). The "\_\_init\_\_.py" file in each folder is necessary to define each folder as a module. 
  
- __test__: For files related to testing our project using pytest. This would be a good area of expansion as there are only a limited number of unit tests at the moment. 
  
- __docs__: For relevant documentation about our project.

- __requirements.txt__: Used to specify dependency requirements for our GitHub continuous integration (CI) environment. 
