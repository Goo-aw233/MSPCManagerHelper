<div align=center>

# MSPCManagerHelper

<img src="../src/assets/icons/MSPCManagerHelper.png" width="140" height="140" alt="MSPCManagerHelper Logo"/>
</div>

## 🖹 選取語言

Please Select Your Language to Continue

請選取您的語言以繼續 | 请选择您的语言以继续

[English (United States)](./../README.md) | [中文 (简体)](./README.zh-Hans.md)

## 👏 簡介

`MSPCManagerHelper` 是一款與 [`Microsoft 電腦管家`](https://apps.microsoft.com/detail/9PM860492SZD)搭配的實用工具（亦稱為 `PCM 幫手`、`PCM 小幫手`、`Microsoft 電腦管家小幫手`或`破產貓小幫手`）。本工具旨在為用戶提供高效、便捷的解決方案，以快速應對使用過程中可能遇到的問題。
歡迎前往 <https://pcmanager.microsoft.com> 下載並體驗最新版 Microsoft 電腦管家，並加入到我們的[社群](https://mspcmanager.github.io/mspcm-docs/appendix/social-accounts.html)當中！😉

> [!IMPORTANT]
> 請注意，本工具並非 Microsoft Corporation 及其子公司官方開發或發佈。開發者與 Microsoft Corporation 及其子公司無直接關聯，工具內的內容也不代表 Microsoft Corporation 或其子公司的立場。

> [!NOTE]
> 請注意，本輔助工具部分內容引用了來自第三方（即非 Microsoft 官方）網頁的連結。這些網頁可能提供準確且、安全的資訊來協助您解決問題。然而，請務必留意頁面上的廣告，其中可能包含通常被歸類為 PUP（Potentially Unwanted Products，潛在有害產品）的內容。在您下載及安裝文件或應用前，請徹底地研究網頁中推廣的任何產品。

## 📦 建置原始碼

1. 從 [Python](https://www.python.org/downloads) 下載 Python 3.14 版本

2. 複製儲存庫

    ```bash
    git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
    cd MSPCManagerHelper
    ```

3. 建立並啟用虛擬環境

    ```Batch
    py -3.14 -m venv .venv
    .venv\Scripts\activate
    ```

4. 安裝套件包

    ```Batch
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    在 `scripts` 目錄下，您也可以直接執行 `install_requirements_.venv.cmd` 以同時啟用虛擬環境並安裝套件包。

5. 建置

    1. 使用 `PyInstaller` 建置

        1. 安裝 `PyInstaller`

            ```Batch
            pip install -r requirements-pyinstaller.txt
            ```

        2. 安裝完成後，執行 `scripts\build\build.cmd`，跟隨指引即可開始建置 EXE。

            > 參數：
            > - Python: [`.venv` | `<Path to python.exe>` | `<empty>`]
            > - Builder: [`nuitka` | `pyinstaller`]
            > - Type: [`onedir` | `onefile`]
            > - Help: [`/?` | `/h` | `/help`]
            > 推薦使用 `.venv`、`pyinstaller` 與 `onefile`。

            也可以透過命令呼叫：`build.cmd /python=<path\to\python.exe> /builder=<builder> /type=<type>`。

            > [!TIP]
            > `build.cmd` 是透過呼叫 `scripts\build\build.py` 的函式所實作的 Windows 命令指令碼。您可以使用相同的方法使用 `build.py` 而不是使用 `build.cmd`。

            建置好的二進位檔案，將會存放在根目錄的 `dist` 目錄下，並命名為 `MSPCManagerHelper_..._v#.#.#.#_<架構>.exe`。

    2. 使用 `Nuitka` 建置

        > [!IMPORTANT]
        > 儘管 Nuitka 使用 C 語言建置二進位檔，但是僅允許在目標平台上進行編譯，不允許交叉編譯。

        1. 安裝 [Visual Studio](https://visualstudio.microsoft.com/downloads) 或[適用於 C++ 的 Visual Studio 建置工具](https://visualstudio.microsoft.com/visual-cpp-build-tools)

            在 `Visual Studio Installer` 中，勾選並安裝以下工作負載：
            > - MSBuild 工具
            > - 使用 C++ 的桌面開發
            >   - C++ 建置工具核心功能
            >   - Visual C++ v14 重分發更新
            >   - C++ 核心桌面功能
            >   - 適用於 x64/x86 的 MSVC 建置工具 (最新版)（x64/x86 架構）
            >   - 適用於 ARM64/ARM64EC 的 MSVC 建置工具 (最新版)（ARM64 架構）
            >   - Windows SDK（例如：`Windows 11 SDK (10.0.26100.0)`）

        2. 安裝 `Nuitka` 及 `Zstandard`

            ```Batch
            pip install -r requirements-nuitka.txt
            ```

            > [!NOTE]
            > 若正在使用較新版本或預發布版的 Python，請嘗試使用 `factory` 分支的 `Nuitka`，以相容新的 Python 特性，需要先[安裝 Git](https://git-scm.com/install)。
            > 
            > ```Batch
            > pip install "nuitka@git+https://github.com/Nuitka/Nuitka.git@factory"
            > ```

        3. 安裝完成後，執行 `scripts\build\build.cmd`，跟隨指引即可開始建置 EXE。

            > 參數：
            > - Python: [`.venv` | `<Path to python.exe>` | `<empty>`]
            > - Builder: [`nuitka` | `pyinstaller`]
            > - Type: [`onefile` | `standalone`]
            > - Help: [`/?` | `/h` | `/help`]
            > 推薦使用 `.venv`、`nuitka` 與 `onefile`。

            也可以透過命令呼叫：`build.cmd /python=<path\to\python.exe> /builder=<builder> /type=<type>`。

            > [!TIP]
            > `build.cmd` 是透過呼叫 `scripts\build\build.py` 的函式所實作的 Windows 命令指令碼。您可以使用相同的方法使用 `build.py` 而不是使用 `build.cmd`。

            建置好的二進位檔案，將會存放在根目錄的 `dist` 目錄下，並命名為 `MSPCManagerHelper_..._v#.#.#.#_<架構>.exe`。
