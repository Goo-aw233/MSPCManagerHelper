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

        x64_path = tool_folder / x64_binary
        arm64_path = tool_folder / arm64_binary

        arch_key = None

        # Method 1: platform.machine()
        try:
            machine = (platform.machine() or "").lower()
            if any(k in machine for k in ("amd64", "x86_64", "x64", "intel64")):
                arch_key = "AMD64"
            elif any(k in machine for k in ("arm64", "aarch64")):
                arch_key = "ARM64"
        except Exception:
            pass

        # Method 2: winreg
        if not arch_key:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                    processor_architecture, _ = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")
                    arch_key = processor_architecture
            except (FileNotFoundError, OSError):
                pass

        # Depend on Detected Architecture
        if arch_key == "ARM64":
            if arm64_path.exists():
                return str(arm64_path)
            if x64_path.exists():
                return str(x64_path)

        if x64_path.exists():
               return str(x64_path)

        return None

    @staticmethod
    def nsudo_path():
        return AppResources._get_binary_path("NSudo", "NSudoLC_x64.exe", "NSudoLC_ARM64.exe")

    @staticmethod
    def procdump_path():
        return AppResources._get_binary_path("ProcDump", "procdump64.exe", "procdump64a.exe")
