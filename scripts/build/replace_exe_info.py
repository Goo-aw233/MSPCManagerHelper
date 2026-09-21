import platform
import subprocess
from datetime import datetime
from pathlib import Path
from runpy import run_path

AppMetadata = run_path(
    str(Path(__file__).resolve().parents[2] / "src" / "core" / "app_metadata.py")
)["AppMetadata"]
SCRIPT_PATH = Path(__file__).parent


def _get_arch():
    machine = platform.machine()
    if machine == "AMD64":
        return "x64"
    if machine == "ARM64":
        return "ARM64"
    raise RuntimeError(f"Unsupported Architecture: {machine}")

def _get_resource_hacker():
    resource_hacker_path = SCRIPT_PATH / "resource_hacker"
    resource_hacker_exe = resource_hacker_path / "ResourceHacker.exe"
    if resource_hacker_exe.exists():
        return resource_hacker_exe

    resource_hacker_zip = resource_hacker_path.with_suffix(".zip")
    # Invoke-WebRequest Requests WMF 3.0
    powershell_command = (
        "$ErrorActionPreference = 'Stop'; "
        "Invoke-WebRequest "
        "-Uri 'https://www.angusj.com/resourcehacker/resource_hacker.zip' "
        f"-OutFile '{resource_hacker_zip}'; "
        f"Expand-Archive -LiteralPath '{resource_hacker_zip}' "
        f"-DestinationPath '{resource_hacker_path}' -Force; "
        f"Remove-Item -LiteralPath '{resource_hacker_zip}' -Force"
    )
    print(f"\n\nDownloading Resource Hacker to {resource_hacker_zip}...")
    subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            powershell_command,
        ],
        check=True,
    )
    return resource_hacker_exe

def _make_manifest_rc():
    rc_path = SCRIPT_PATH / f"{AppMetadata.APP_NAME}.manifest.rc"
    rc_path.write_text(
        f'1 24 "{AppMetadata.APP_NAME}.manifest"\n',
        encoding="utf-8",
    )
    return rc_path

def _make_version_rc():
    arch = _get_arch()

    app_version = ".".join(map(str, AppMetadata.APP_VERSION_TUPLE))
    app_version_text = f"{AppMetadata.APP_VERSION} {arch}"
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    content = f'''1 VERSIONINFO
FILEVERSION {app_version.replace(".", ",")}
PRODUCTVERSION {app_version.replace(".", ",")}
FILEOS 0x4
FILETYPE 0x1
{{
BLOCK "StringFileInfo"
{{
	BLOCK "040904B0"
	{{
		VALUE "CompanyName", "{AppMetadata.APP_AUTHOR}"
		VALUE "FileDescription", "{AppMetadata.APP_NAME}"
		VALUE "FileVersion", "{app_version_text}"
		VALUE "InternalName", "{app_file_name}"
		VALUE "LegalCopyright", "\\xA9 2024 - {datetime.now().year} {AppMetadata.APP_AUTHOR} All rights reserved."
		VALUE "OriginalFilename", "{app_file_name}.exe"
		VALUE "ProductName", "{AppMetadata.APP_NAME}"
		VALUE "ProductVersion", "{app_version_text}"
	}}
}}

BLOCK "VarFileInfo"
{{
	VALUE "Translation", 0x0409 0x04B0  
}}
}}
'''

    rc_path = SCRIPT_PATH / f"{AppMetadata.APP_NAME}.version.rc"
    rc_path.write_text(content, encoding="utf-8", newline="\n")
    return rc_path

def _replace_manifest(output_path, target_path=None, new_target_path=None):
    rc_path = _make_manifest_rc()
    res_path = SCRIPT_PATH / f"{AppMetadata.APP_NAME}.manifest.res"
    resource_hacker = _get_resource_hacker()
    arch = _get_arch()

    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    target_path = target_path or output_path / f"{app_file_name}.exe"
    new_target_path = new_target_path or output_path / f"{app_file_name}_manifest.exe"

    subprocess.run(
        [
            str(resource_hacker),
            "-open", str(rc_path),
            "-save", str(res_path),
            "-action", "compile",
            "-log", "CONSOLE",
        ],
        cwd=SCRIPT_PATH,
        check=True,
    )
    subprocess.run(
        [
            str(resource_hacker),
            "-open", str(target_path),
            "-save", str(new_target_path),
            "-action", "addoverwrite",
            "-res", str(res_path),
            "-mask", "MANIFEST,",
            "-log", "CONSOLE",
        ],
        cwd=SCRIPT_PATH,
        check=True,
    )

def _replace_version(output_path, target_path=None, new_target_path=None):
    rc_path = _make_version_rc()
    res_path = SCRIPT_PATH / f"{AppMetadata.APP_NAME}.version.res"
    resource_hacker = _get_resource_hacker()
    arch = _get_arch()

    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    target_path = target_path or output_path / f"{app_file_name}_manifest.exe"
    new_target_path = new_target_path or output_path / f"{app_file_name}_new.exe"

    subprocess.run(
        [
            str(resource_hacker),
            "-open", str(rc_path),
            "-save", str(res_path),
            "-action", "compile",
            "-log", "CONSOLE",
        ],
        cwd=SCRIPT_PATH,
        check=True,
    )
    subprocess.run(
        [
            str(resource_hacker),
            "-open", str(target_path),
            "-save", str(new_target_path),
            "-action", "addoverwrite",
            "-res", str(res_path),
            "-mask", "VersionInfo,,",
            "-log", "CONSOLE",
        ],
        cwd=SCRIPT_PATH,
        check=True,
    )

def _rename_files(output_path, replacement_path):
    arch = _get_arch()
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    original_path = output_path / f"{app_file_name}.exe"
    origin_path = output_path / f"{app_file_name}_origin.exe"

    if not replacement_path.is_file():
        raise FileNotFoundError(f"Replacement File Not Found: {replacement_path}")
    original_path.rename(origin_path)
    replacement_path.rename(original_path)

def run(output_path=None, stages="all"):
    output_path = Path(output_path) if output_path else Path(__file__).parent
    if not stages:
        return
    if stages not in ("manifest", "version", "all"):
        raise ValueError(f"Unsupported replacement stages: {stages}")

    arch = _get_arch()
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    original_path = output_path / f"{app_file_name}.exe"
    manifest_path = output_path / f"{app_file_name}_manifest.exe"
    replacement_path = original_path

    if stages in ("manifest", "all"):
        _replace_manifest(output_path, replacement_path, manifest_path)
        replacement_path = manifest_path

    if stages in ("version", "all"):
        version_path = output_path / f"{app_file_name}_new.exe"
        _replace_version(output_path, replacement_path, version_path)
        replacement_path = version_path

    _rename_files(output_path, replacement_path)
    if manifest_path.exists():
        manifest_path.unlink()
