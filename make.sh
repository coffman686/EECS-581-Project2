#!/bin/bash
pyinstaller src/main.py --clean --onefile --distpath . --workpath build --name Minesweeper --specpath spec --noconfirm