<h1 align="center">MSPCManagerHelper</h1>

## 🖹 選取語言

Please select your language to continue

請選取你的語言以繼續 | 请选择你的语言以继续

[English (United States)](./README.md) | [簡體中文 (中國)](./README.zh-cn.md)

## 👏 簡介

這是一款專為 `Microsoft 電腦管家` 開發的輔助工具：`MSPCManagerHelper`，旨在協助使用者快速解決使用過程中可能遇到的問題，提供簡單高效的解決方案。
歡迎前往 <https://pcmanager.microsoft.com> 下載並體驗最新版 Microsoft 電腦管家，並加入到我們的 [社群](https://forms.office.com/r/EPcrKfUbjK) 當中！😉

> [!IMPORTANT]
> 本工具並非 Microsoft Corporation 或其子公司官方推出。開發者與 Microsoft Corporation 或其子公司無直接關聯，工具內的內容也不代表 Microsoft Corporation 或其子公司的立場。

> [!NOTE]
> 請注意，本輔助工具部分內容引用了來自第三方（即非 Microsoft 官方）網頁的連結。這些網頁可能提供準確且安全的資訊來協助您解決問題。然而，請務必留意頁面上的廣告，其中可能包含通常被歸類為 PUP（Potentially Unwanted Products，潛在有害產品）的內容。在您下載及安裝文件或應用前，請徹底地研究網頁中推廣的任何產品。

## 💻 開發

1. 從 [Python](https://www.python.org/downloads) 下載 Python 3.11 版本

2. 將倉庫 Clone 至本機

```bash
git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
cd MSPCManagerHelper
```

3. 建立並啟用虛擬環境

- **Windows**: 

```bat
cd <path\to\MSPCManagerHelper>
python.exe -m venv .venv
.venv\Scripts\activate
```

- **macOS / Linux**: 

```bash
cd <path/to/MSPCManagerHelper>
python3 -m venv .venv
source .venv/bin/activate
```

4. 安裝套件包

```bash
pip install -r requirements.txt
pip install requests
python -m pip install --upgrade pip
```

您也可以執行 `install_requirements.bat` 完成安裝，或執行 `install_requirements_.venv.bat` 同時啟用虛擬環境並安裝套件。

5. 構建 EXE

直接執行根目錄下的 `build.bat` 或 `build_.venv.bat` 即可自己構建。
