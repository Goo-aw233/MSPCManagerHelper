import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

VSWHERE_NAME = "vswhere.exe"
WINDOWS_11_SDK_FAMILY = "Windows11SDK"
MIN_WINDOWS_11_SDK_VERSION = 26100
WINDOWS_SDK_PATTERN = re.compile(
    r"^Microsoft\.VisualStudio\.Component\.(Windows\d*SDK)(?:\.(\d+))?$"
)
DEFAULT_VSWHERE_PATH = (
    Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))
    / "Microsoft Visual Studio"
    / "Installer"
    / VSWHERE_NAME
)

TARGETS = {
    "MSBuild Tools": ["Microsoft.Component.MSBuild"],
    "Desktop development with C++": [
        # Visual Studio
        "Microsoft.VisualStudio.Workload.NativeDesktop",
        # VS Build Tools
        "Microsoft.VisualStudio.Workload.VCTools",
    ],
    "C++ Build Tools core features": [
        # Visual Studio
        "Microsoft.VisualStudio.Component.VC.CoreIde",
        # VS Build Tools
        "Microsoft.VisualStudio.Component.VC.CoreBuildTools",
    ],
    "Visual C++ v14 redistributable updates": [
        "Microsoft.VisualStudio.Component.VC.Redist.14.Latest",
    ],
    "C++ core desktop features": [
        "Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Core",
    ],
}

ARCH_TARGETS = {
    "x64": {
        "MSVC Build Tools for x64/x86 (latest)": [
            "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
        ],
    },
    "ARM64": {
        "MSVC Build Tools for ARM64/ARM64EC (latest)": [
            "Microsoft.VisualStudio.Component.VC.Tools.ARM64",
        ],
    },
}


def _get_arch():
    machine = platform.machine()
    if machine == "AMD64":
        return "x64"
    if machine == "ARM64":
        return "ARM64"
    raise RuntimeError(f"Unsupported Architecture: {machine}")

def _find_vswhere():
    found = shutil.which(VSWHERE_NAME)
    if found:
        return Path(found)
    if DEFAULT_VSWHERE_PATH.is_file():
        return DEFAULT_VSWHERE_PATH
    print("[ERROR] vswhere.exe not found, "
          "please make sure Visual Studio or Build Tools is installed.")
    sys.exit(1)

def _query_instances(vswhere_path):
    cmd = [
        str(vswhere_path),
        "-all",
        "-products", "*",
        "-include", "packages",
        "-format", "json",
    ]
    try:
        output = subprocess.check_output(cmd, encoding="utf-8", errors="ignore")
        instances = json.loads(output)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"[ERROR] Failed to Run vswhere.exe: {error}")
        sys.exit(1)
    if not instances:
        print("[ERROR] No Visual Studio instance detected.")
        sys.exit(1)
    return instances

def _find_windows_sdks(installed_packages):
    sdks = []
    for package in installed_packages:
        match = WINDOWS_SDK_PATTERN.match(package)
        if match:
            sdks.append((match.group(1), int(match.group(2) or 0), package))
    return sorted(sdks)

def _check_any(installed_packages, candidate_ids):
    for cid in candidate_ids:
        if cid in installed_packages:
            return cid
    return None

def check_vs_workload():
    instances = _query_instances(_find_vswhere())

    installed_packages = {
        package["id"]
        for instance in instances
        for package in instance.get("packages", [])
        if "id" in package
    }

    installed_products = {
        instance.get("productId", "Unknown")
        for instance in instances
    }

    print("=== Installed Products ===")
    for pid in sorted(installed_products):
        print(f"[INFO] {pid}")

    print("\n=== Visual Studio Core Components ===")
    targets = {**TARGETS, **ARCH_TARGETS[_get_arch()]}
    ok = True
    for name, candidate_ids in targets.items():
        matched = _check_any(installed_packages, candidate_ids)
        installed = matched is not None
        ok = ok and installed
        status = "[ OK ]" if installed else "[MISS]"
        detail = matched if matched else " / ".join(candidate_ids)
        print(f"{status} {name:<45} -> {detail}")

    sdks = _find_windows_sdks(installed_packages)
    qualified = {
        package
        for family, version, package in sdks
        if family == WINDOWS_11_SDK_FAMILY and version >= MIN_WINDOWS_11_SDK_VERSION
    }

    print(f"\n=== Windows 11 SDK (At Least Version {MIN_WINDOWS_11_SDK_VERSION}) ===")
    if qualified:
        for package in sorted(qualified):
            print(f"[ OK ] {package}")
    else:
        print("[MISS] No Windows 11 SDK installed through Visual Studio.")
        ok = False

    unqualified = [
        package for _, _, package in sdks if package not in qualified
    ]
    if unqualified:
        print("\n=== Other Windows SDK ===")
        for package in unqualified:
            print(f"[INFO] {package}")

    print(f"\n{'[ OK ]' if ok else '[FAIL]'} Visual Studio workload check "
          f"{'passed' if ok else 'failed'}.")
    return ok

if __name__ == "__main__":
    sys.exit(0 if check_vs_workload() else 1)
