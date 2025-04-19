<h1 align="center">MSPCManagerHelper</h1>

<div align=center>
<img src="./src/assets/MSPCManagerHelper.png" width="140" height="140"/>
</div>

> [!IMPORTANT]  
> This repository will go into slow mode and there will be no updates for a short period of time unless there are major bugs, vulnerabilities, or Microsoft PC Manager updates that need to be adapted, etc.

## 🖹 Choose Your Language

Please select your language to continue

請選取你的語言以繼續 | 请选择你的语言以继续

[繁體中文 (臺灣)](./README.zh-tw.md) | [简体中文 (中国大陆)](./README.zh-cn.md)

## 👏 Introduction

`MSPCManagerHelper` is a utility (`PCM Assistant`, `PCM Helper` or `Microsoft PC Manager Helper`) that comes with [`Microsoft PC Manager`](https://apps.microsoft.com/detail/9PM860492SZD). This tool is designed to provide users with efficient and convenient solutions to quickly deal with problems they may encounter during use.
Visit <https://pcmanager.microsoft.com> to download and experience the latest version of Microsoft PC Manager and join our [User Community](https://forms.office.com/r/EPcrKfUbjK)! 😉

> [!IMPORTANT]  
> This tool is not developed or endorsed by Microsoft Corporation or its subsidiaries. The authors are independent developers with no affiliation to Microsoft or its subsidiaries.

> [!NOTE]  
> Some features of `MSPCManagerHelper` include references to third-party (non-Microsoft) web pages. While these pages may offer accurate and helpful information, they might also contain advertisements categorized as PUPs (Potentially Unwanted Products). Please exercise caution and thoroughly review any products or files before downloading or installing them.

## 💻 Development

1. Download Python 3.11 from [Python](https://www.python.org/downloads)

2. Clone the Repository

```bash
git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
cd MSPCManagerHelper
```

3. Create and Activate a Virtual Environment

- **Windows**: 

```Batch
cd <path\to\MSPCManagerHelper>
python -m venv .venv
.venv\Scripts\activate
```

<details>

<summary>The <code>install_requirements.sh</code> for macOS and Linux is no longer available</summary>

- **macOS / Linux**: 

```bash
cd <path/to/MSPCManagerHelper>
python3 -m venv .venv
source .venv/bin/activate
```

</details>

4. Install the pip Packages

```Batch
pip install -r requirements.txt
pip install requests
python -m pip install --upgrade pip
```

In the `scripts` directory, you can also run `install_requirements.bat` directly to quickly complete the installation, or run `install_requirements_.venv.bat` to activate the virtual environment and install the dependencies at the same time.

5. Build the EXE

Run `build.bat` or `build_.venv.bat` directly from the `scripts\build` directory to build it yourself.
Finally, the built `EXE file` will be stored in the `dist` directory of the root directory and named `MSPCManagerHelper_... _vx.x.x.x.x.exe`.
