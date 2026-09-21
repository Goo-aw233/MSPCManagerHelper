"""Build script for the MSPCManagerHelper application.

Packages src/main.py with PyInstaller or Nuitka, using the application
metadata from src/core/app_metadata.py and the architecture reported by
platform.machine(). The script itself has no third party dependencies, but
it must be started with the interpreter that has the selected builder
installed.

Usage:
    python.exe scripts/build/build.py /builder=pyinstaller /type=[onedir | onefile]
    python.exe scripts/build/build.py /builder=nuitka /type=[onefile | standalone]

PyInstaller builds receive a version file which is generated next to this
script as version_<arch>.txt, and write their spec file there as well. Pass
'/?', '/h' or '/help' for the full command line help.
"""

import importlib.util
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from runpy import run_path

# Load src/core/app_metadata.py directly: importing the core package would drag in
# the whole GUI dependency stack (core/__init__.py imports every core module).
AppMetadata = run_path(
    str(Path(__file__).resolve().parents[2] / "src" / "core" / "app_metadata.py")
)["AppMetadata"]

ReplaceEXEInfo = run_path(
    str(Path(__file__).with_name("replace_exe_info.py"))
)

REPLACE_STAGES = {
    # ("builder", "type"): "stages",
    ("nuitka", "onefile"): "all",
    ("pyinstaller", "onefile"): "manifest",
}


def _get_arch() -> str:
    machine = platform.machine()
    if machine == "AMD64":
        return "x64"
    if machine == "ARM64":
        return "ARM64"
    raise RuntimeError(f"Unsupported Architecture: {machine}")

def _build_with_pyinstaller(build_type: str):
    if importlib.util.find_spec("PyInstaller") is None:
        sys.exit(f"PyInstaller is not installed in {sys.executable}.")

    arch = _get_arch()

    root = Path(__file__).resolve().parents[2]
    src = root / "src"
    icon = src / "assets" / "icons" / "MSPCManagerHelper.ico"
    nsudo = src / "assets" / "tools" / "NSudo" / f"NSudoLC_{arch}.exe"
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"

    subprocess.run(
        [
            sys.executable, "-m", "PyInstaller",
            f"--{build_type}",
            "--windowed",
            "--name", app_file_name,
            "--add-data", f"{src / 'assets' / 'locales'};assets/locales",
            "--add-data", f"{src / 'assets' / 'fonts' / 'FluentSystemIcons-Regular.ttf'};assets/fonts",
            "--add-data", f"{icon};assets/icons",
            "--add-data", f"{root / 'ThirdPartyNotices.txt'};assets/license",
            "--add-data", f"{root / 'docs' / 'THIRD_PARTY_NOTICES.txt'};assets/license",
            "--add-binary", f"{nsudo};assets/tools/NSudo",
            "--clean",
            "--noconfirm",  # Overwrite Existing build/dist Folders Without Asking
            "--distpath", str(root / "dist"),
            "--specpath", str(Path(__file__).resolve().parent),
            "--icon", str(icon),
            "--version-file", str(_make_version_file()),
            "--workpath", str(root / "build"),
            str(src / "main.py"),
        ],
        check=True,
    )

def _build_with_nuitka(build_type: str):
    if importlib.util.find_spec("nuitka") is None:
        sys.exit(f"Nuitka is not installed in {sys.executable}.")

    arch = _get_arch()

    root = Path(__file__).resolve().parents[2]
    src = root / "src"
    icon = src / "assets" / "icons" / "MSPCManagerHelper.ico"
    nsudo = src / "assets" / "tools" / "NSudo" / f"NSudoLC_{arch}.exe"
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"
    app_version = ".".join(map(str, AppMetadata.APP_VERSION_TUPLE))

    subprocess.run(
        [
            sys.executable, "-m", "nuitka",
            f"--{build_type}",
            "--windows-console-mode=disable",
            "--assume-yes-for-downloads",   # Automatically Download Required Dependencies
            f"--output-dir={root / 'dist'}",
            f"--output-filename={app_file_name}.exe",
            f"--include-data-dir={src / 'assets' / 'locales'}=assets/locales",
            f"--include-data-files={src / 'assets' / 'fonts' / 'FluentSystemIcons-Regular.ttf'}=assets/fonts/FluentSystemIcons-Regular.ttf",
            f"--include-data-files={icon}=assets/icons/MSPCManagerHelper.ico",
            f"--include-data-files={root / 'ThirdPartyNotices.txt'}=assets/license/ThirdPartyNotices.txt",
            f"--include-data-files={root / 'docs' / 'THIRD_PARTY_NOTICES.txt'}=assets/license/THIRD_PARTY_NOTICES.txt",
            f"--include-data-files={nsudo}=assets/tools/NSudo/NSudoLC_{arch}.exe",
            "--include-module=winrt.windows.foundation",
            "--include-module=winrt.windows.foundation.collections",
            "--include-windows-runtime-dlls=yes",
            "--enable-plugin=tk-inter",
            f"--windows-icon-from-ico={icon}",
            f"--file-version={app_version}",
            f"--product-version={app_version}",
            f"--file-description={AppMetadata.APP_NAME}",
            f"--product-name={AppMetadata.APP_NAME}",
            f"--company-name={AppMetadata.APP_AUTHOR}",
            f"--copyright=© 2024 - {datetime.now().year} {AppMetadata.APP_AUTHOR} All rights reserved.",
            f"--main={src / 'main.py'}",
        ],
        check=True,
    )

def _replace_exe_info(builder: str, build_type: str, stages: str):
    root = Path(__file__).resolve().parents[2]
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{_get_arch()}"
    output_path = root / "dist"
    if builder == "pyinstaller" and build_type == "onedir":
        output_path /= app_file_name
    ReplaceEXEInfo["run"](output_path, stages)

def _make_version_file() -> Path:
    arch = _get_arch()

    app_version = f"{AppMetadata.APP_VERSION} {arch}"
    app_file_name = f"{AppMetadata.APP_NAME}_{AppMetadata.APP_VERSION_WITHOUT_SPACES}_{arch}"

    content = f"""\
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
#

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={AppMetadata.APP_VERSION_TUPLE},
    prodvers={AppMetadata.APP_VERSION_TUPLE},
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [
        StringStruct('CompanyName', '{AppMetadata.APP_AUTHOR}'),
        StringStruct('FileDescription', '{AppMetadata.APP_NAME}'),
        StringStruct('FileVersion', '{app_version}'),
        StringStruct('InternalName', '{app_file_name}'),
        StringStruct('LegalCopyright', '© 2024 - {datetime.now().year} {AppMetadata.APP_AUTHOR} All rights reserved.'),
        StringStruct('OriginalFilename', '{app_file_name}.exe'),
        StringStruct('ProductName', '{AppMetadata.APP_NAME}'),
        StringStruct('ProductVersion', '{app_version}')
        ]
      )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""

    path = Path(__file__).with_name(f"version_{arch}.txt")
    path.write_text(content, encoding="utf-8", newline="\r\n")
    return path

def _get_help() -> str:
    return f"""\
{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION} Build Helper

Usage: build.py /builder=[nuitka | pyinstaller] /type=[onedir | onefile | standalone]

Every argument needs the /, - or -- prefix, and argument names and values
are case-insensitive. Name and value may be joined by = or :, so
/type=onedir and /type:onedir are both accepted.

Arguments:
  /builder=[nuitka | pyinstaller]   Builder name (required).
  /type=[onefile | standalone]      Output build type of Nuitka (required).
  /type=[onedir | onefile]          Output build type of PyInstaller (required).
  /?, /h, /help                   Show this help and exit.

Example: build.py /builder=pyinstaller /type=onedir
"""

def _get_environment() -> str:
    import ctypes
    import os
    import shutil
    import winreg
    from importlib.metadata import PackageNotFoundError, version
    from typing import Any

    def read(path: str, name: str) -> Any:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as registry_key:
                return winreg.QueryValueEx(registry_key, name)[0]
        except OSError:
            return ""

    def package_version(name: str) -> str:
        try:
            return version(name)
        except PackageNotFoundError:
            return ""

    def format_line(label: str, value: str) -> str:
        return f"{label:<16}: {value}"

    def get_processor_count() -> int:
        relation_processor_package = 3
        buffer_length = ctypes.c_ulong(0)
        ctypes.windll.kernel32.GetLogicalProcessorInformationEx(
            relation_processor_package,
            None,
            ctypes.byref(buffer_length),
        )
        buffer = ctypes.create_string_buffer(buffer_length.value)
        if not ctypes.windll.kernel32.GetLogicalProcessorInformationEx(
            relation_processor_package,
            buffer,
            ctypes.byref(buffer_length),
        ):
            return 1

        package_count = 0
        offset = 0
        while offset < buffer_length.value:
            relation = ctypes.c_uint.from_buffer(buffer, offset).value
            record_size = ctypes.c_uint.from_buffer(buffer, offset + 4).value
            if relation == relation_processor_package:
                package_count += 1
            offset += record_size
        return package_count or 1

    class DisplayDevice(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_ulong),
            ("DeviceName", ctypes.c_wchar * 32),
            ("DeviceString", ctypes.c_wchar * 128),
            ("StateFlags", ctypes.c_ulong),
            ("DeviceID", ctypes.c_wchar * 128),
            ("DeviceKey", ctypes.c_wchar * 128),
        ]

    def get_gpu_memory(device_key: str) -> str:
        registry_prefix = "\\Registry\\Machine\\"
        if not device_key.startswith(registry_prefix):
            return "Unknown"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, device_key[len(registry_prefix):]) as registry_key:
                try:
                    memory_size = winreg.QueryValueEx(
                        registry_key,
                        "HardwareInformation.qwMemorySize",
                    )[0]
                except OSError:
                    memory_size = winreg.QueryValueEx(
                        registry_key,
                        "HardwareInformation.MemorySize",
                    )[0]
        except OSError:
            return "Unknown"
        if isinstance(memory_size, bytes):
            memory_size = int.from_bytes(memory_size, byteorder="little")
        if not isinstance(memory_size, int) or not memory_size:
            return "Unknown"
        memory_gb: float = float(memory_size) / 2**30
        return f"{memory_gb:.1f} GB"

    def get_gpu() -> str:
        display_devices = []
        index = 0
        while True:
            display_device = DisplayDevice()
            display_device.cb = ctypes.sizeof(display_device)
            if not ctypes.windll.user32.EnumDisplayDevicesW(None, index, ctypes.byref(display_device), 0):
                break
            if display_device.DeviceString:
                gpu_info = f"{display_device.DeviceString} ({get_gpu_memory(display_device.DeviceKey)})"
                if gpu_info not in display_devices:
                    display_devices.append(gpu_info)
            index += 1
        return "\n".join(
            format_line(f"GPU{index}", gpu_info)
            for index, gpu_info in enumerate(display_devices)
        )

    class MemoryStatus(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    builder = " / ".join(
        f"{name} {found}" for name in ("Nuitka", "PyInstaller") if (found := package_version(name))
    )

    current_version = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    ubr = read(current_version, "UBR")
    build = f"{platform.version()}.{ubr}" if ubr else platform.version()
    os_info = " ".join(
        part
        for part in (
            "Microsoft Windows",
            platform.release(),
            platform.win32_edition(),
            read(current_version, "DisplayVersion"),
            f"Build {build}",
        )
        if part
    )

    build_lab_ex = read(current_version, "BuildLabEx")

    cpu_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
    cpu_name = read(cpu_path, "ProcessorNameString")
    cpu_mhz: int = read(cpu_path, "~MHz")
    cpu_ghz = f"~{cpu_mhz / 1000:.2f} GHz" if cpu_mhz else ""
    processor_count = get_processor_count()
    logical_processor_count = os.cpu_count() or 1
    cores_per_processor = max(1, logical_processor_count // processor_count)
    cpu_spec = " / ".join(
        part
        for part in (read(cpu_path, "Identifier"), f"{cores_per_processor} Cores", cpu_ghz)
        if part
    )
    cpu = "\n".join(
        format_line(f"CPU{index}", f"{cpu_name} ({cpu_spec})")
        for index in range(processor_count)
    )

    gpu = get_gpu()

    memory = MemoryStatus()
    memory.dwLength = ctypes.sizeof(memory)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
    ram_total: float = memory.ullTotalPhys / 2**30
    ram_free: float = memory.ullAvailPhys / 2**30
    ram = f"{ram_total:.1f} GB ({ram_free:.1f} GB Available)"

    root = Path(__file__).resolve().parents[2]
    disk = shutil.disk_usage(root)
    disk_total: float = disk.total / 2**30
    disk_free: float = disk.free / 2**30
    rom = f"{root.drive} {disk_total:.1f} GB ({disk_free:.1f} GB Available)"

    return (
        "\n=== Machine Information ===\n"
        f"{format_line('Environment', f'Python {platform.python_version()} @ {sys.executable}')}\n"
        f"{format_line('Python', f'{platform.python_implementation()} {platform.python_compiler()}')}\n"
        f"{format_line('Builder', builder)}\n"
        f"{format_line('OS', os_info)}\n"
        f"{format_line('BuildLabEx', build_lab_ex)}\n"
        f"{format_line('Arch', platform.machine())}\n"
        f"{format_line('Device Name', platform.node())}\n"
        f"{cpu}\n"
        f"{gpu}\n"
        f"{format_line('RAM', ram)}\n"
        f"{format_line('ROM', rom)}\n\n"
        f"{'#' * 20}\n"
    )


if __name__ == "__main__":
    prefixes = ("/", "-", "--")
    separators = ("=", ":")

    def argument_forms(names, with_value=False):
        tails = separators if with_value else ("",)
        return [f"{prefix}{name}{tail}" for prefix in prefixes for name in names for tail in tails]

    def argument_values(forms):
        return [arg[len(form):].lower() for arg in sys.argv[1:] for form in forms if arg.lower().startswith(form)]

    builder_forms = argument_forms(("builder",), with_value=True)
    type_forms = argument_forms(("type",), with_value=True)
    help_forms = argument_forms(("?", "h", "help"))

    if len(sys.argv) < 2:
        print(_get_help())
        sys.exit(1)

    if any(arg.lower() in help_forms for arg in sys.argv[1:]):
        print(_get_help())
        sys.exit(0)

    builders = argument_values(builder_forms)
    build_types = argument_values(type_forms)
    duplicates = [name for name, found in (("builder", builders), ("type", build_types)) if len(found) > 1]
    if duplicates:
        sys.exit(f"Duplicate Argument: {', '.join(sorted(duplicates))}")

    unknown = set()
    for arg in sys.argv[1:]:
        if arg.lower() in help_forms or any(arg.lower().startswith(form) for form in builder_forms + type_forms):
            continue
        unknown.add(arg)
    if unknown:
        sys.exit(f"Unknown Argument: {', '.join(sorted(unknown))}")

    selected_builder = builders[0] if builders else ""
    selected_type = build_types[0] if build_types else ""
    allowed_types = ("onedir", "onefile") if selected_builder == "pyinstaller" else ("onefile", "standalone")

    if not selected_builder:
        sys.exit("Missing Argument: builder=[nuitka | pyinstaller] is required.")
    elif selected_builder not in ("nuitka", "pyinstaller"):
        sys.exit(f"Invalid Value: builder={selected_builder}\nExpected Value: builder=[nuitka | pyinstaller]")

    if not selected_type:
        sys.exit(f"Missing Argument: type=[{'|'.join(allowed_types)}] is required.")
    elif selected_type not in allowed_types:
        sys.exit(f"Invalid Value: type={selected_type}\nExpected Value: type=[{'|'.join(allowed_types)}]")

    print(_get_environment())

    if selected_builder == "pyinstaller":
        _build_with_pyinstaller(selected_type)
    elif selected_builder == "nuitka":
        _build_with_nuitka(selected_type)
    else:
        raise RuntimeError(f"Unsupported Builder: {selected_builder}")

    selected_stages = REPLACE_STAGES.get((selected_builder, selected_type))
    if selected_stages:
        _replace_exe_info(selected_builder, selected_type, selected_stages)
