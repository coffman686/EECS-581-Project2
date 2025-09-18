#!/bin/bash
pyinstaller src/main.py --clean --onefile --distpath dist-linux --workpath build-linux --name Minesweeper --specpath spec-linux --noconfirm