import os
import tempfile
from pathlib import Path


class AppResources:
    @staticmethod
    def app_temp_dir():
        for candidate in (
            Path(tempfile.gettempdir()) / "MSPCManagerHelper",
            Path(os.getenv("SystemRoot", r"C:\Windows")) / "Temp" / "MSPCManagerHelper",
            Path.home() / ".cache" / "MSPCManagerHelper",
        ):
            try:
                candidate.mkdir(parents=True, exist_ok=True)
                return str(candidate)
            except OSError:
                continue
        # Current working directory as the last resort.
        final = Path.cwd() / "MSPCManagerHelper"
        final.mkdir(parents=True, exist_ok=True)
        return str(final)

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

        from core.system_checks import PrerequisiteChecks
        arch_key = PrerequisiteChecks.check_os_architecture()

        if arch_key == "ARM64" and arm64_path.exists():
            return str(arm64_path)

        # Compatible with ARM64 when using x64.
        if x64_path.exists():
            return str(x64_path)

        return None

    @staticmethod
    def nsudo_path():
        return AppResources._get_binary_path("NSudo", "NSudoLC_x64.exe", "NSudoLC_ARM64.exe")

    @staticmethod
    def procdump_path():
        return AppResources._get_binary_path("ProcDump", "procdump64.exe", "procdump64a.exe")
