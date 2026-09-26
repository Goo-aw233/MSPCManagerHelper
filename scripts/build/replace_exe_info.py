import platform
import shutil
import subprocess
import zipfile
from pathlib import Path
from runpy import run_path

AppMetadata = run_path(
    str(Path(__file__).resolve().parents[2] / "src" / "core" / "app_metadata.py")
)["AppMetadata"]
SCRIPT_PATH = Path(__file__).resolve().parent


def _get_arch():
    machine = platform.machine()
    if machine == "AMD64":
        return "x64"
    if machine == "ARM64":
        return "ARM64"
    raise RuntimeError(f"Unsupported Architecture: {machine}")

def _get_curl_version(curl_exe):
    # --retry-all-errors arrived in curl 7.71, probe rather than assume.
    try:
        version = subprocess.run(
            [curl_exe, "--version"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()[1]
        major, minor = (int(part) for part in version.split(".")[:2])
    except (OSError, IndexError, ValueError, subprocess.CalledProcessError):
        return False
    return (major, minor) >= (7, 71)

def _download_resource_hacker(archive_path, extract_path):
    url = "https://www.angusj.com/resourcehacker/resource_hacker.zip"

    curl_exe = shutil.which("curl.exe")
    try:
        if curl_exe:
            print(f"\n\nDownloading Resource Hacker to {archive_path} "
                  "with curl.exe...")
            curl_command = [
                curl_exe,
                "--fail",           # Treat HTTP Errors as Failures
                "--location",       # Follow Redirects
                "--show-error",
                "--output", str(archive_path),
                "--retry", "3",     # Retry Transient Failures
            ]
            if _get_curl_version(curl_exe):
                curl_command.append("--retry-all-errors")
            else:
                print("This curl does not support --retry-all-errors, "
                      "only transient errors will be retried.")
            curl_command.append(url)

            subprocess.run(curl_command, check=True)
        else:
            print(f"\n\nDownloading Resource Hacker to {archive_path} "
                  "with Windows PowerShell..."
                  "\nDownload progress display is turned off.")
            # Invoke-WebRequest Requests WMF 3.0
            powershell_command = (
                "$ErrorActionPreference = 'Stop'; "
                "$ProgressPreference = 'SilentlyContinue'; "    # Turn Off Progress Display
                "Invoke-WebRequest "
                "-UseBasicParsing " # Avoid Relying on Internet Explorer
                f"-Uri '{url}' "
                f"-OutFile '{archive_path}'"
            )
            subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-Command",
                    powershell_command,
                ],
                check=True,
            )

        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(extract_path)
    except BaseException:
        shutil.rmtree(extract_path, ignore_errors=True)
        raise
    finally:
        archive_path.unlink(missing_ok=True)

def _get_resource_hacker():
    resource_hacker_path = SCRIPT_PATH / "resource_hacker"
    resource_hacker_exe = resource_hacker_path / "ResourceHacker.exe"
    if resource_hacker_exe.exists():
        return resource_hacker_exe

    _download_resource_hacker(
        resource_hacker_path.with_suffix(".zip"), resource_hacker_path
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
    # Resource Hacker may decode non-ASCII bytes in .rc files using the system ANSI code page.
    # Write the copyright sign as the ASCII-only RC escape \xA9.
    copyright_text = AppMetadata.APP_COPYRIGHT.replace("\u00a9", r"\xA9")
    content = f'''1 VERSIONINFO
FILEVERSION {app_version.replace(".", ",")}
PRODUCTVERSION {app_version.replace(".", ",")}
FILEOS 0x4
FILETYPE 0x1
{{
BLOCK "StringFileInfo"
{{
	BLOCK "000004B0"
	{{
		VALUE "CompanyName", "{AppMetadata.APP_AUTHOR}"
		VALUE "FileDescription", "{AppMetadata.APP_NAME}"
		VALUE "FileVersion", "{app_version_text}"
		VALUE "InternalName", "{app_file_name}"
		VALUE "LegalCopyright", "{copyright_text}"
		VALUE "OriginalFilename", "{app_file_name}.exe"
		VALUE "ProductName", "{AppMetadata.APP_NAME}"
		VALUE "ProductVersion", "{app_version_text}"
	}}
}}

BLOCK "VarFileInfo"
{{
	VALUE "Translation", 0x0000 0x04B0  
}}
}}
'''

    rc_path = SCRIPT_PATH / f"{AppMetadata.APP_NAME}.version.rc"
    rc_path.write_text(content, encoding="utf-8", newline="\n")
    return rc_path

def _replace_manifest(output_path, target_path=None, new_target_path=None):
    arch = _get_arch()
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    target_path = target_path or output_path / f"{app_file_name}.exe"
    new_target_path = new_target_path or output_path / f"{app_file_name}_manifest.exe"

    if not target_path.is_file():
        raise FileNotFoundError(f"Target File Not Found: {target_path}")

    rc_path = _make_manifest_rc()
    res_path = SCRIPT_PATH / f"{AppMetadata.APP_NAME}.manifest.res"
    resource_hacker = _get_resource_hacker()

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
    arch = _get_arch()
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    target_path = target_path or output_path / f"{app_file_name}_manifest.exe"
    new_target_path = new_target_path or output_path / f"{app_file_name}_new.exe"

    if not target_path.is_file():
        raise FileNotFoundError(f"Target File Not Found: {target_path}")

    rc_path = _make_version_rc()
    res_path = SCRIPT_PATH / f"{AppMetadata.APP_NAME}.version.res"
    resource_hacker = _get_resource_hacker()

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

def _get_backup_dir(output_path):
    for parent in (output_path, *output_path.parents):
        if parent.name == "dist":
            return parent.with_name(f"{parent.name}.bak")
    return output_path.with_name(f"{output_path.name}.bak")

def _rename_files(output_path, replacement_path):
    arch = _get_arch()
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    original_path = output_path / f"{app_file_name}.exe"
    backup_path = _get_backup_dir(output_path) / f"{app_file_name}_backup.exe"

    if not replacement_path.is_file():
        raise FileNotFoundError(f"Replacement File Not Found: {replacement_path}")
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    original_path.replace(backup_path)
    try:
        replacement_path.replace(original_path)
    except BaseException:
        # Move the backup back to the original location if replacement fails.
        backup_path.replace(original_path)
        raise
    print(f"\nMoved the Backup EXE to: {backup_path}")

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
