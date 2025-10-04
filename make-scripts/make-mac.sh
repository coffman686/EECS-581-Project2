#!/bin/bash
pyinstaller src/main.py --clean --onefile --distpath dist-mac --workpath build-mac --name Minesweeper --specpath spec-mac --noconfirm