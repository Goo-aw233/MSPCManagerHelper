<div align=center>

# MSPCManagerHelper

<img src="./src/assets/icons/MSPCManagerHelper.png" width="140" height="140" alt="MSPCManagerHelper Logo"/>
</div>

## 🖹 Choose Your Language

Please Select Your Language to Continue

請選取你的語言以繼續 | 请选择你的语言以继续

[中文 (繁體)](./docs/README.zh-Hant.md) | [中文 (简体)](./docs/README.zh-Hans.md)

## 👏 Introduction

`MSPCManagerHelper` is a utility (`PCM Assistant`, `PCM Helper` or `Microsoft PC Manager Helper`) that comes with [`Microsoft PC Manager`](https://apps.microsoft.com/detail/9PM860492SZD). This tool is designed to provide users with efficient and convenient solutions to quickly deal with problems they may encounter during use.
Visit <https://pcmanager.microsoft.com> to download and experience the latest version of Microsoft PC Manager and join our [User Community](https://mspcmanager.github.io/mspcm-docs/appendix/social-accounts.html)! 😉

> [!IMPORTANT]
> This tool is not developed or endorsed by Microsoft Corporation or its subsidiaries. The authors are independent developers with no affiliation to Microsoft or its subsidiaries.

> [!NOTE]
> Some features of `MSPCManagerHelper` include references to third-party (non-Microsoft) web pages. While these pages may offer accurate and helpful information, they might also contain advertisements categorized as PUPs (Potentially Unwanted Products). Please exercise caution and thoroughly review any products or files before downloading or installing them.

## 📦 Build from Source

1. Download Python 3.14 from [Python](https://www.python.org/downloads)

2. Clone the Code

    ```bash
    git clone https://github.com/Goo-aw233/MSPCManagerHelper.git
    cd MSPCManagerHelper
    ```

3. Create and Activate a Virtual Environment

    ```Batch
    py -3.14 -m venv .venv
    .venv\Scripts\activate
    ```

4. Install the pip Packages

    ```Batch
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    In the `scripts` directory, you can also run `install_requirements_.venv.cmd` to activate the virtual environment and install the dependencies at the same time.

5. Build

    1. Build with `PyInstaller`

        1. Install `PyInstaller`

            ```Batch
            pip install -r requirements-pyinstaller.txt
            ```

        2. Once installed, run `scripts\build\build.cmd` and follow the prompts to start building the EXE.

            > Parameters:
            > - Python: [`.venv` | `<Path to python.exe>` | `<empty>`]
            > - Builder: [`nuitka` | `pyinstaller`]
            > - Type: [`onedir` | `onefile`]
            > - Help: [`/?` | `/h` | `/help`]
            > `.venv`, `pyinstaller` and `onefile` are recommended.

            You can also invoke it from the command line: `build.cmd /python=<path\to\python.exe> /builder=<builder> /type=<type>`.

            > [!TIP]
            > `build.cmd` is a Windows command script implemented by calling the functions of `scripts\build\build.py`. You can use `build.py` instead of `build.cmd` in the same way.

            The built binary will be stored in the `dist` directory of the root directory and named `MSPCManagerHelper_..._v#.#.#.#_<Arch>.exe`.

    2. Build with `Nuitka`

        > [!IMPORTANT]
        > Although Nuitka compiles binaries with C, it only allows compilation on the target platform — cross-compilation is not allowed.

        1. Install [Visual Studio](https://visualstudio.microsoft.com/downloads) or [Visual Studio Build Tools for C++](https://visualstudio.microsoft.com/visual-cpp-build-tools)

            In `Visual Studio Installer`, check and install the following workloads:
            > - MSBuild Tools
            > - Desktop development with C++
            >   - `C++ Build Tools core features`
            >   - `Visual C++ v14 redistributable updates`
            >   - `C++ core desktop features`
            >   - `MSVC Build Tools for x64/x86 (latest)` (for the x64/x86 architecture)
            >   - `MSVC Build Tools for ARM64/ARM64EC (latest)` (for the ARM64 architecture)
            >   - `Windows SDK` (For example: `Windows 11 SDK (10.0.26100.0)`)

        2. Install `Nuitka` and `Zstandard`

            ```Batch
            pip install -r requirements-nuitka.txt
            ```

            > [!NOTE]
            > If you are using a newer version or pre-release version of Python, try using the `Nuitka` from the `factory` branch to be compatible with the new Python features. You need to [install Git](https://git-scm.com/install) first.
            > 
            > ```Batch
            > pip install "nuitka@git+https://github.com/Nuitka/Nuitka.git@factory"
            > ```

        3. Once installed, run `scripts\build\build.cmd` and follow the prompts to start building the EXE.

            > Parameters:
            > - Python: [`.venv` | `<Path to python.exe>` | `<empty>`]
            > - Builder: [`nuitka` | `pyinstaller`]
            > - Type: [`onefile` | `standalone`]
            > - Help: [`/?` | `/h` | `/help`]
            > `.venv`, `nuitka` and `onefile` are recommended.

            You can also invoke it from the command line: `build.cmd /python=<path\to\python.exe> /builder=<builder> /type=<type>`.

            > [!TIP]
            > `build.cmd` is a Windows command script implemented by calling the functions of `scripts\build\build.py`. You can use `build.py` instead of `build.cmd` in the same way.

            The built binary will be stored in the `dist` directory of the root directory and named `MSPCManagerHelper_..._v#.#.#.#_<Arch>.exe`.
