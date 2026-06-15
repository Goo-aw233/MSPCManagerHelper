<div align=center>

# MSPCManagerHelper
<img src="../src/assets/icons/MSPCManagerHelper.png" width="140" height="140"/>
</div>

## 🖹 选择语言

Please Select Your Language to Continue

請選取你的語言以繼續 | 请选择你的语言以继续

[English (United States)](./../README.md) | [中文 (繁體)](./README.zh-Hant.md)

## 👏 简介

`MSPCManagerHelper` 是一款与[`微软电脑管家`](https://apps.microsoft.com/detail/9PM860492SZD)配套的实用工具（亦称为 `PCM 助手`、`PCM 小助手`、`微软电脑管家小助手`或`破产猫小助手`）。本工具旨在为用户提供高效、便捷的解决方案，以快速应对使用过程中可能遇到的问题。
欢迎访问 <https://pcmanager.microsoft.com> 下载并体验最新版本的微软电脑管家，并加入到我们的[社群](https://forms.office.com/r/7YhjaEEmKc)当中！😉

> [!IMPORTANT]
> 
> 请注意，本工具并非 Microsoft Corporation 及其子公司官方开发或发布。工具作者与 Microsoft Corporation 及其子公司无任何隶属关系，工具中的内容也不代表 Microsoft Corporation 或其子公司的官方立场。

> [!NOTE]
> 
> 请注意，本辅助工具部分内容引用了来自第三方（即非 Microsoft 官方）网页的链接。这些网页似乎提供了准确、安全的信息以帮助你解决问题。但是，请仍然留意网页中推广的通常被归类为 PUP（Potentially Unwanted Products，潜在有害产品）的广告。在您下载及安装文件或应用前，请彻底地研究网页中推广的任何产品。

## 💻 开发

1. 从 [Python](https://www.python.org/downloads) 下载 Python 3.14 版本

2. 克隆代码

    ```bash
    git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
    cd MSPCManagerHelper
    ```

3. 创建和激活虚拟环境

    - **Windows**:

        ```Batch
        py -3.14 -m venv .venv
        .venv\Scripts\activate
        ```

    <details>
    <summary>macOS 与 Linux 的 <code>install_requirements.sh</code> 已不再提供</summary>

    - **macOS / Linux**:

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

    </details>

4. 安装依赖包

    ```Batch
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    在 `scripts` 目录下，您也可以直接运行 `install_requirements.cmd` 快速完成安装，或运行 `install_requirements_.venv.cmd` 同时激活虚拟环境并安装依赖包。

5. 构建 EXE

    直接运行 `scripts\build` 目录下的 `build.cmd` 或 `build_.venv.cmd` 即可自己构建。
    最后，构建好的 `EXE 文件` 将会存放在根目录的 `dist` 目录下，并命名为 `MSPCManagerHelper_..._v#.#.#.#_<架构>.exe`。

> [!NOTE]
> 
> 如果你想使用 Nuitka 构建，请在 [Visual Studio](https://visualstudio.microsoft.com/downloads)（或[适用于 C++ 的 Visual Studio 生成工具](https://visualstudio.microsoft.com/visual-cpp-build-tools)）中安装：
> - MSBuild 工具
> - 使用 C++ 的桌面开发
>   - C++ 生成工具核心功能
>   - Visual C++ v14 可再发行更新
>   - C++ 核心桌面功能
>   - 适用于 x64/x86 的 MSVC 生成工具 (最新版)
>   - Windows SDK（例如：`Windows 11 SDK (10.0.26100.0)`）
> 
> 在虚拟环境中安装 `Nuitka` 和 `Zstandard`：
> 
> ```Batch
> pip install nuitka zstandard
> ```
> 
> 随后，将 `build_nuitka_.venv.cmd` 脚本从 `scripts\disabled` 文件夹移动到 `scripts\build` 文件夹，并使用脚本构建，构建时推荐使用 `ziglang`。
> **对于中文用户，请添加 `chcp 65001` 到脚本最顶部，以确保所有字符正确显示。**
