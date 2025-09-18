### Welcome!
To play Minesweeper, enter either of the *"dist-windows" or "dist-linux"* folders and run the executable inside.
It should not need any external dependencies. 

Alternatively, you can also run the following command (which may require the installation of additional dependencies):
`python -m src.main`

### Dependencies:
- Python 3
- curses (Linux) / windows-curses (Windows)
- Standard libraries: enum, platform, random
- pyinstaller (if you are intending to build the project)

### Terminal
You must use a terminal that supports curses mouse functionality.
This has been verified using tmux, windows terminal, and Alacritty, but may depend on 
the operating system in use and if all software has been updated. Windows 10 may not work.
The best options are WSL, Linux, or Windows 11. 

### How to build
<<<<<<< HEAD
Depending on your platform (you will need to have the dependencies), run either the make-linux.sh or make-windows.bat scripts.
=======
Depending on your platform (you will need to have the dependencies), run either the make-linux.sh or make-windows.bat scripts.
>>>>>>> e510e54 (Update README for new build system.)
