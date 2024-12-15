<h1 align="center">MSPCManagerHelper</h1>

## 🖹 Choose Your Language

Please select your language to continue

請選取你的語言以繼續 | 请选择你的语言以继续

[繁體中文 (臺灣)](./README.zh-tw.md) | [简体中文 (中国大陆)](./README.zh-cn.md)

## 👏 Introduction

`MSPCManagerHelper` is a utility tool designed to complement `Microsoft PC Manager`. It aims to provide users with efficient and convenient solutions for resolving issues they may encounter.
Visit <https://pcmanager.microsoft.com> to download and experience the latest version of Microsoft PC Manager and join our [User Community](https://forms.office.com/r/EPcrKfUbjK)! 😉

> [!IMPORTANT]  
> This tool is not developed or endorsed by Microsoft Corporation or its subsidiaries. The authors are independent developers with no affiliation to Microsoft or its subsidiaries.

> [!NOTE]  
> Some features of `MSPCManagerHelper` include references to third-party (non-Microsoft) web pages. While these pages may offer accurate and helpful information, they might also contain advertisements categorized as PUPs (Potentially Unwanted Products). Please exercise caution and thoroughly review any products or files before downloading or installing them.

## 💻 Development

1. Download Python 3.11 from [Python](https://www.python.org/downloads)

2. Clone the repository

```bash
git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
cd MSPCManagerHelper
```

3. Create and activate a virtual environment

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

4. Install the pip packages

```bash
pip install -r requirements.txt
pip install requests
python -m pip install --upgrade pip
```

Or by running `install_requirements.bat`.
You can also activate the virtual environment and install pip packages with `install_requirements_.venv.bat`.

5. Build the EXE

Build yourself by running `build.bat` or `build_.venv.bat` directly from the root directory.
