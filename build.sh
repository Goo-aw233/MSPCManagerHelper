#!/bin/bash

arch=$(uname -m)

echo "$arch"
echo ""

if [ "$arch" == "x86_64" ]; then
    pyinstaller --onefile --windowed --name "MSPCManagerHelper_Beta_v0.2.0.1_x64" --add-data "locales:locales" --add-data "assets/MSPCManagerHelper-256.ico:." --add-binary "tools/procdump/procdump64.exe:." --clean --version-file=version_x64.txt -i "assets/MSPCManagerHelper-48.ico" mainWindow.py
elif [ "$arch" == "aarch64" ]; then
    pyinstaller --onefile --windowed --name "MSPCManagerHelper_Beta_v0.2.0.1_ARM64" --add-data "locales:locales" --add-data "assets/MSPCManagerHelper-256.ico:." --add-binary "tools/procdump/procdump64a.exe:." --clean --version-file=version_ARM64.txt -i "assets/MSPCManagerHelper-48.ico" mainWindow.py
else
    echo "UNKNOWN: $arch"
fi

read -n 1 -s -r -p "Press any key to continue..."
