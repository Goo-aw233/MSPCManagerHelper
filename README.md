<h1 align="center">MSPCManagerHelper</h1>

## 🖹 Choose Your Language

Select your region and language to continue.

选择你的语言地区以继续。

[繁體中文 (臺灣)](./README.zh-tw.md) | [简体中文 (中国大陆)](./README.zh-cn.md)

## 👏 Introduction

This is a utility `MSPCManagerHelper` designed for **Microsoft Corporation** `Microsoft PC Manager`, this tool is designed to help users to solve the problems encountered to provide fast and convenient solutions. Welcome to <https://pcmanager.microsoft.com> to download and try the latest version of Microsoft PC Manager! 😉

> [!IMPORTANT]
> We are not organized by Microsoft Coporation or its subsidiaries to write this document, and are not employees of Microsoft Coporation or its subsidiaries.

> [!NOTE]
> Parts of MSPCManagerHelper refer to links from third-party (i.e., non-official Microsoft) web pages. These pages appear to provide accurate and safe information to help you solve your problem. However, please remain aware of ads promoted on these pages that are often categorized as PUPs (Potentially Unwanted Products). Before downloading and installing a file or application, please thoroughly research any products promoted on the page.

## 💻 Development

1. Download Python 3.11 from [Python](https://www.python.org/downloads).

2. Clone the repository

```
git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
cd MSPCManagerHelper
```

3. Create and activate the virtual environment

```
python -m venv <path\to\MSPCManagerHelper>
<path\to\MSPCManagerHelper>\Scripts\activate
```

4. Install the pip packages

```
pip install -r requirements.txt
pip install requests
python -m pip install --upgrade pip
```

Or by running `install_requirements.bat`.

5. Build the EXE

Build yourself by running `build` directly from the root directory.

- Build for Windows x64:
`build_x64.bat` or `build_x64.sh`

- Build for Windows ARM64:
`build_ARM64.bat` or `build_ARM64.sh`.
