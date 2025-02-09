<h1 align="center">MSPCManagerHelper</h1>

## 🖹 选择语言

Please select your language to continue

請選取你的語言以繼續 | 请选择你的语言以继续

[English (United States)](./README.md) | [繁體中文 (臺灣)](./README.zh-tw.md)

## 👏 简介

`MSPCManagerHelper` 是一款与 [`微软电脑管家`](https://www.microsoft.com/store/productId/9PM860492SZD) 配套的实用工具（亦称为 `PCM 助手`、`PCM 小助手`、`微软电脑管家小助手` 或 `破产猫小助手`）。本工具旨在为用户提供高效、便捷的解决方案，以快速应对使用过程中可能遇到的问题。
欢迎访问 <https://pcmanager.microsoft.com> 下载并体验最新版本的微软电脑管家，并加入到我们的 [社群](https://forms.office.com/r/7YhjaEEmKc) 当中！😉

> [!IMPORTANT]
> 请注意，本工具并非 Microsoft Corporation 及其子公司官方开发或发布。工具作者与 Microsoft Corporation 及其子公司无任何隶属关系，工具中的内容也不代表 Microsoft Corporation 或其子公司的官方立场。

> [!NOTE]
> 请注意，本辅助工具部分内容引用了来自第三方（即非 Microsoft 官方）网页的链接。这些网页似乎提供了准确、安全的信息以帮助你解决问题。但是，请仍然留意网页中推广的通常被归类为 PUP（Potentially Unwanted Products，潜在有害产品）的广告。在您下载及安装文件或应用前，请彻底地研究网页中推广的任何产品。

## 💻 开发

1. 从 [Python](https://www.python.org/downloads) 下载 Python 3.11 版本

2. 将仓库 Clone 至本地

```bash
git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
cd MSPCManagerHelper
```

3. 创建和激活虚拟环境

- **Windows**: 

```Batch
cd <path\to\MSPCManagerHelper>
python -m venv .venv
.venv\Scripts\activate
```

<details>

<summary>macOS 与 Linux 的 <code>install_requirements.sh</code> 已不再提供</summary>

- **macOS / Linux**: 

```bash
cd <path/to/MSPCManagerHelper>
python3 -m venv .venv
source .venv/bin/activate
```

</details>

4. 安装依赖包

```Batch
pip install -r requirements.txt
pip install requests
python -m pip install --upgrade pip
```

在 `scripts` 目录下，您也可以直接运行 `install_requirements.bat` 快速完成安装，或运行 `install_requirements_.venv.bat` 同时激活虚拟环境并安装依赖包。

5. 构建 EXE

直接运行 `build` 目录下的 `build.bat` 或 `build_.venv.bat` 即可自己构建。
最后，构建好的 `EXE 文件` 将会存放在 `build\dist` 目录下，并命名为 `MSPCManager_..._vx.x.x.x.exe`。
