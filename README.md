### Welcome!
To play Minesweeper, enter either of the *"dist-windows", "dist-linux", or "dist-mac"* folders and run the executable inside.
It should not need any external dependencies. However, you do need a properly setup terminal environment.
- For mouse input, your terminal must support curses mouse functionality. Otherwise, you can just use the keyboard interface.
- Our flag icon uses a fancy unicode code point, so if you're missing some rendering support it may appear as a missing character.
- Your terminal needs to have a properly setup terminfo database. This should not be an issue, as most terminals should be configured correctly by default. However, if you have an improperly configured terminal, the program will crash due to being unable to initialize the user interface. This issue occurs most often in the Linux builds. If it happens, then you must rebuild your executable by following the instructions below in the "How to build" section. 

Alternatively, you can also run the following command (which may require the installation of additional dependencies):
`python -m src.main`

### Dependencies:
- Python 3
- curses (Linux) / windows-curses (Windows)
- Standard libraries: enum, platform, random
- pyinstaller (if you are intending to build the project)
- pytest (if you're interesting in running tests)

### Terminal
You must use a terminal that supports curses mouse functionality.
This has been verified using tmux, windows terminal, and Alacritty, but may depend on 
the operating system in use and if all software has been updated. Windows 10 may not work.
The best options are WSL, Linux, or Windows 11. 

### How to build
Depending on your platform (you will need to have the dependencies), run the make-linux.sh, make-windows.bat, or make-mac.sh script.
The dist-\<os\> folders contain the executables. The build-\<os\> folders contain temporary build files, and the spec-\<os\> folders 
contain specification files used by pyinstaller. The executables should be self-contained with all the necessary dependencies, but if
you run into issues try rebuilding them. The provided Linux build was created using WSL Ubuntu and Windows with Windows 11. 

If you do not have pyinstaller, you can install it with the following command: `pip install pyinstaller`

### Other Repository details
- __src__: For source files. Within src, see the __tui__ folder for frontend-specific files. 
  - Note that this repository uses a python module structure (the "-m" in the command given above). The "\_\_init\_\_.py" file in each folder is necessary to define each module. 
  
- __test__: For files related to testing our project using pytest. This would be a good area of expansion as there are only a limited number of unit tests at the moment. 
  
- __docs__: For relevant documentation about our project.

- __requirements.txt__: Used to specify dependency requirements for our GitHub continuous integration (CI) environment. 