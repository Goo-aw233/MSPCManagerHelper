#!/bin/bash

arch=$(uname -m)

echo "$arch"
echo ""

if [ "$arch" == "x86_64" ]; then
    pyinstaller --onefile --windowed --name "MSPCManagerHelper_Preview_v24103_-_we11D_x64" --add-data "locales:locales" --add-binary "tools/procdump/procdump64.exe:." --clean --version-file=version_x64.txt mainWindow.py
elif [ "$arch" == "aarch64" ]; then
    pyinstaller --onefile --windowed --name "MSPCManagerHelper_Preview_v24103_-_we11D_ARM64" --add-data "locales:locales" --add-binary "tools/procdump/procdump64a.exe:." --clean --version-file=version_ARM64.txt mainWindow.py
else
    echo "UNKNOWN: $arch"
fi

read -n 1 -s -r -p "Press any key to continue..."
