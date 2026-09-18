<div align=center>

# MSPCManagerHelper

<img src="../src/assets/icons/MSPCManagerHelper.png" width="140" height="140" alt="MSPCManagerHelper Logo"/>
</div>

## 🖹 选择语言

Please Select Your Language to Continue

請選取您的語言以繼續 | 请选择您的语言以继续

[English (United States)](./../README.md) | [中文 (繁體)](./README.zh-Hant.md)

## 👏 简介

`MSPCManagerHelper` 是一款与[`微软电脑管家`](https://apps.microsoft.com/detail/9PM860492SZD)配套的实用工具（亦称为 `PCM 助手`、`PCM 小助手`、`微软电脑管家小助手`或`破产猫小助手`）。本工具旨在为用户提供高效、便捷的解决方案，以快速应对使用过程中可能遇到的问题。
欢迎访问 <https://pcmanager.microsoft.com> 下载并体验最新版本的微软电脑管家，并加入到我们的[社群](https://forms.office.com/r/7YhjaEEmKc)当中！😉

> [!IMPORTANT]
> 请注意，本工具并非 Microsoft Corporation 及其子公司官方开发或发布。工具作者与 Microsoft Corporation 及其子公司无任何隶属关系，工具中的内容也不代表 Microsoft Corporation 或其子公司的官方立场。

> [!NOTE]
> 请注意，本辅助工具部分内容引用了来自第三方（即非 Microsoft 官方）网页的链接。这些网页似乎提供了准确、安全的信息以帮助您解决问题。但是，请仍然留意网页中推广的通常被归类为 PUP（Potentially Unwanted Products，潜在有害产品）的广告。在您下载及安装文件或应用前，请彻底地研究网页中推广的任何产品。

## 📦 构建源码

1. 从 [Python](https://www.python.org/downloads) 下载 Python 3.14 版本

2. 克隆代码

    ```bash
    git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
    cd MSPCManagerHelper
    ```

3. 创建和激活虚拟环境

    ```Batch
    py -3.14 -m venv .venv
    .venv\Scripts\activate
    ```

4. 安装依赖包

    ```Batch
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    在 `scripts` 目录下，您也可以直接运行 `install_requirements_.venv.cmd` 以同时激活虚拟环境并安装依赖包。

5. 构建

    1. 使用 `PyInstaller` 构建

        1. 安装 `PyInstaller`

            ```Batch
            pip install -r requirements-pyinstaller.txt
            ```

        2. 安装完成后，运行 `scripts\build\build.cmd`，跟随指引即可开始构建 EXE。

            > 参数：
            > - Python: [`.venv` | `<Path to python.exe>` | `<empty>`]
            > - Builder: [`nuitka` | `pyinstaller`]
            > - Type: [`onedir` | `onefile`]
            > - Help: [`/?` | `/h` | `/help`]
            > 推荐使用 `.venv`、`pyinstaller` 与 `onefile`。

            也可以通过命令调用：`build.cmd /python=<path\to\python.exe> /builder=<builder> /type=<type>`。

            > [!TIP]
            > `build.cmd` 是通过调用 `scripts\build\build.py` 的函数所实现的 Windows 命令脚本。您可以使用相同的方法使用 `build.py` 而不是使用 `build.cmd`。

            构建好的二进制文件，将会存放在根目录的 `dist` 目录下，并命名为 `MSPCManagerHelper_..._v#.#.#.#_<架构>.exe`。

    2. 使用 `Nuitka` 构建

        > [!IMPORTANT]
        > 尽管 Nuitka 使用 C 语言构建二进制文件，但是仅允许在目标平台上进行编译，不允许交叉编译。

        1. 安装 [Visual Studio](https://visualstudio.microsoft.com/downloads) 或[适用于 C++ 的 Visual Studio 生成工具](https://visualstudio.microsoft.com/visual-cpp-build-tools)

            在 `Visual Studio Installer` 中，勾选并安装以下工作负载：
            > - MSBuild 工具
            > - 使用 C++ 的桌面开发
            >   - C++ 生成工具核心功能
            >   - Visual C++ v14 可再发行更新
            >   - C++ 核心桌面功能
            >   - 适用于 x64/x86 的 MSVC 生成工具 (最新版)（x64/x86 架构）
            >   - 适用于 ARM64/ARM64EC 的 MSVC 生成工具 (最新版)（ARM64 架构）
            >   - Windows SDK（例如：`Windows 11 SDK (10.0.26100.0)`）

        2. 安装 `Nuitka` 及 `Zstandard`

            ```Batch
            pip install -r requirements-nuitka.txt
            ```

            > [!NOTE]
            > 若正在使用较新版本或预发布版的 Python，请尝试使用 `factory` 分支的 `Nuitka`，以兼容新的 Python 特性，需要先[安装 Git](https://git-scm.com/install)。
            > 
            > ```Batch
            > pip install "nuitka@git+https://github.com/Nuitka/Nuitka.git@factory"
            > ```

        3. 安装完成后，运行 `scripts\build\build.cmd`，跟随指引即可开始构建 EXE。

            > 参数：
            > - Python: [`.venv` | `<Path to python.exe>` | `<empty>`]
            > - Builder: [`nuitka` | `pyinstaller`]
            > - Type: [`onefile` | `standalone`]
            > - Help: [`/?` | `/h` | `/help`]
            > 推荐使用 `.venv`、`nuitka` 与 `onefile`。

            也可以通过命令调用：`build.cmd /python=<path\to\python.exe> /builder=<builder> /type=<type>`。

            > [!TIP]
            > `build.cmd` 是通过调用 `scripts\build\build.py` 的函数所实现的 Windows 命令脚本。您可以使用相同的方法使用 `build.py` 而不是使用 `build.cmd`。

            构建好的二进制文件，将会存放在根目录的 `dist` 目录下，并命名为 `MSPCManagerHelper_..._v#.#.#.#_<架构>.exe`。
