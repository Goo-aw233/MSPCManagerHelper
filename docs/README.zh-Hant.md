<div align=center>

# MSPCManagerHelper
<img src="../src/assets/icons/MSPCManagerHelper.png" width="140" height="140"/>
</div>

## 🖹 選取語言

Please Select Your Language to Continue

請選取你的語言以繼續 | 请选择你的语言以继续

[English (United States)](./../README.md) | [中文 (简体)](./README.zh-Hans.md)

## 👏 簡介

`MSPCManagerHelper` 是一款與 [`Microsoft 電腦管家`](https://apps.microsoft.com/detail/9PM860492SZD)搭配的實用工具（亦稱為 `PCM 幫手`、`PCM 小幫手`、`Microsoft 電腦管家小幫手`或`破產貓小幫手`）。本工具旨在為用戶提供高效、便捷的解決方案，以快速應對使用過程中可能遇到的問題。
歡迎前往 <https://pcmanager.microsoft.com> 下載並體驗最新版 Microsoft 電腦管家，並加入到我們的[社群](https://mspcmanager.github.io/mspcm-docs/appendix/social-accounts.html)當中！😉

> [!IMPORTANT]
> 
> 請注意，本工具並非 Microsoft Corporation 及其子公司官方開發或發佈。開發者與 Microsoft Corporation 及其子公司無直接關聯，工具內的內容也不代表 Microsoft Corporation 或其子公司的立場。

> [!NOTE]
> 
> 請注意，本輔助工具部分內容引用了來自第三方（即非 Microsoft 官方）網頁的連結。這些網頁可能提供準確且、安全的資訊來協助您解決問題。然而，請務必留意頁面上的廣告，其中可能包含通常被歸類為 PUP（Potentially Unwanted Products，潛在有害產品）的內容。在您下載及安裝文件或應用前，請徹底地研究網頁中推廣的任何產品。

## 💻 開發

1. 從 [Python](https://www.python.org/downloads) 下載 Python 3.14 版本

2. 複製儲存庫

    ```bash
    git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
    cd MSPCManagerHelper
    ```

3. 建立並啟用虛擬環境

    - **Windows**:

        ```Batch
        py -3.14 -m venv .venv
        .venv\Scripts\activate
        ```

    <details>
    <summary>macOS 與 Linux 的 <code>install_requirements.sh</code> 已不再提供</summary>

    - **macOS / Linux**:

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

    </details>

4. 安裝套件包

    ```Batch
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    在 `scripts` 目錄下，您也可以直接執行 `install_requirements.cmd` 快速完成安裝，或執行 `install_requirements_.venv.cmd` 同時啟用虛擬環境並安裝套件。

5. 建置 EXE

    直接執行 `scripts\build` 目錄下的 `build.cmd` 或 `build_.venv.cmd` 即可自行建置。
    最後，建置好的 `EXE 檔案` 將會存放在根目錄的 `dist` 目錄下，並命名為 `MSPCManagerHelper_..._v#.#.#.#_<架構>.exe`。

> [!NOTE]
> 
> 如果您想要使用 Nuitka 建置，請在 [Visual Studio](https://visualstudio.microsoft.com/downloads) (或[適用於 C++ 的 Visual Studio 建置工具](https://visualstudio.microsoft.com/visual-cpp-build-tools)) 中安裝：
> - MSBuild 工具
> - 使用 C++ 的桌面開發 (C++ 建置工具核心功能、Visual C++ v14 重分發更新、C++ 核心桌面功能、適用於 x64/x86 的 MSVC 建置工具 (最新版))
> 在虛擬環境中安裝 `Nuitka` 和 `Zstandard`：
> 
> ```Batch
> pip install nuitka zstandard
> ```
> 
> 接著，將 `build_nuitka_.venv.cmd` 指令碼從 `scripts\disabled` 資料夾移動到 `scripts\build` 資料夾，並使用該指令碼進行建置，建置時建議使用 `zig`。
> 對於中文使用者，請添加 `chcp 65001` 到指令碼最頂部，以確保所有字元正確顯示。
