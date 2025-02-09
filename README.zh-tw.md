<h1 align="center">MSPCManagerHelper</h1>

## 🖹 選取語言

Please select your language to continue

請選取你的語言以繼續 | 请选择你的语言以继续

[English (United States)](./README.md) | [簡體中文 (中國)](./README.zh-cn.md)

## 👏 簡介

`MSPCManagerHelper` 是一款與 [`Microsoft 電腦管家`](https://www.microsoft.com/store/productId/9PM860492SZD) 配套的實用工具（亦稱為 `PCM 幫手`、`PCM 小幫手`、`Microsoft 電腦管家小幫手` 或 `破產貓小幫手`）。本工具旨在為用戶提供高效、便捷的解決方案，以快速應對使用過程中可能遇到的問題。
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

```Batch
cd <path\to\MSPCManagerHelper>
python.exe -m venv .venv
.venv\Scripts\activate
```

<details>

<summary>macOS 與 Linux 的 <code>install_requirements.sh</code> 已不再提供</summary>

- **macOS / Linux**: 

```bash
cd <path/to/MSPCManagerHelper>
python3 -m venv .venv
source .venv/bin/activate
```

</details>

4. 安裝套件包

```Batch
pip install -r requirements.txt
pip install requests
python -m pip install --upgrade pip
```

在 `scripts` 目錄下，您也可以直接執行 `install_requirements.bat` 快速完成安裝，或執行 `install_requirements_.venv.bat` 同時啟用虛擬環境並安裝套件。

5. 構建 EXE

直接執行 `build` 目錄下的 `build.bat` 或 `build_.venv.bat` 即可自己構建。
最後，構建好的 `EXE 檔案` 將會存放在 `build\dist` 目錄下，並命名為 `MSPCManager_..._vx.x.x.x.exe`。
