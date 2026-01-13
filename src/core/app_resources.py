import platform
import winreg
from pathlib import Path


class AppResources:
    @staticmethod
    def app_icon():
        app_base_dir = Path(__file__).resolve().parents[1]
        app_icon_path = app_base_dir / "assets" / "icons" / "MSPCManagerHelper.ico"
        if app_icon_path.exists():
            return str(app_icon_path)
        else:
            return None

    @staticmethod
    def _get_binary_path(tool_folder, x64_binary, arm64_binary):
        app_base_dir = Path(__file__).resolve().parents[1]
        tool_folder = app_base_dir / "assets" / "tools" / tool_folder

        arch_map = {
            "AMD64": tool_folder / x64_binary,
            "ARM64": tool_folder / arm64_binary
        }

        # Method 1: platform.machine()
        try:
            machine = (platform.machine() or "").lower()
            if any(k in machine for k in ("amd64", "x86_64", "x64", "intel64")):
                arch_key = "AMD64"
            elif any(k in machine for k in ("arm64", "aarch64")):
                arch_key = "ARM64"
            else:
                arch_key = None
        except Exception:
            arch_key = None

        if arch_key:
            path = arch_map.get(arch_key)
            if path and path.exists():
                return str(path)

        # Method 2: winreg
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                processor_architecture, _ = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")
        except (FileNotFoundError, OSError):
            return None

        path = arch_map.get(processor_architecture)
        return str(path) if path and path.exists() else None

    @staticmethod
    def nsudo_path():
        return AppResources._get_binary_path("NSudo", "NSudoLC_x64.exe", "NSudoLC_ARM64.exe")

    @staticmethod
    def procdump_path():
        return AppResources._get_binary_path("ProcDump", "procdump64.exe", "procdump64a.exe")
