import re
import subprocess
import winreg

import pefile

from core.advanced_startup import AdvancedStartup
from core.path_resolver import PathResolver, WindowsUtilities


class GetMSPCMVersion:
    """Resolve the installed version of Microsoft PC Manager.

    - Stable: Read from the AppX package registry.
    - Beta: Read from its own registry keys, then from
      the version information of the installed executable.
    """

    _STORE_PACKAGE_NAMES = ("Microsoft.MicrosoftPCManager", "Microsoft.PCManager")
    _STORE_FAMILY_NAMES = (
        "Microsoft.MicrosoftPCManager_8wekyb3d8bbwe",
        "Microsoft.PCManager_8wekyb3d8bbwe",
    )

    @staticmethod
    def get_microsoft_pc_manager_version():
        """Return the installed Microsoft PC Manager (Microsoft Store) version,
        e.g. ``"1.1.4.5"``, or ``None`` when it cannot be determined.
        """
        # 1) AppX packages registered for all users.
        for package_name in GetMSPCMVersion._STORE_PACKAGE_NAMES:
            version = GetMSPCMVersion._appx_version_from_store(package_name)
            if version:
                return version

        # 2) Per-user AppX package metadata, when the above was not found.
        for family_name in GetMSPCMVersion._STORE_FAMILY_NAMES:
            version = GetMSPCMVersion._appx_version_from_package_full_name(family_name)
            if version:
                return version

        # 3) Windows PowerShell, when the registry-based lookups above failed.
        return GetMSPCMVersion._version_from_powershell()

    @staticmethod
    def get_microsoft_pc_manager_beta_version():
        """Return the installed Microsoft PC Manager Beta (EXE installer) version,
        e.g. ``"1.1.4.5"``, or ``None`` when it cannot be determined.
        """
        # 1) Beta Setup registry key.
        version = GetMSPCMVersion._read_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\MSPCManager",
            "ProductVersion",
        )
        if version:
            return version

        # 2) Beta Uninstaller registry key.
        version = GetMSPCMVersion._read_registry_value(
            winreg.HKEY_LOCAL_MACHINE,
            r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MSPCManager",
            "ProductVersion",
        )
        if version:
            return version

        # 3) Version information of the installed executable.
        return GetMSPCMVersion._version_from_exe_file(
            PathResolver.program_files() / "Microsoft PC Manager" / "MSPCManager.exe"
        )

    @staticmethod
    def _appx_version_from_store(package_name):
        """Return the version of the AppX package whose full name begins with
        ``package_name`` (e.g. ``Microsoft.MicrosoftPCManager_1.1.4.5_neutral_~_8wekyb3d8bbwe``),
        or ``None`` when it is not installed.
        """
        prefix = f"{package_name}_"
        for subkey_name in GetMSPCMVersion._iter_subkey_names(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Appx\AppxAllUserStore\Applications",
        ):
            if subkey_name.startswith(prefix):
                version = GetMSPCMVersion._extract_version_from_full_name(subkey_name)
                if version:
                    return version
        return None

    @staticmethod
    def _appx_version_from_package_full_name(family_name):
        """Return the version of the AppX package whose full name is ``family_name``,
        or ``None`` when it is not installed.
        """
        schema_path = (
            r"Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion"
            r"\AppModel\SystemAppData"
            fr"\{family_name}\Schemas"
        )
        package_full_name = GetMSPCMVersion._read_registry_value(
            winreg.HKEY_CURRENT_USER, schema_path, "PackageFullName"
        )
        return GetMSPCMVersion._extract_version_from_full_name(package_full_name)

    @staticmethod
    def _extract_version_from_full_name(package_full_name: str | None) -> str | None:
        """Extract the ``x.x.x.x`` version from a package full name such as
        ``Microsoft.MicrosoftPCManager_1.1.4.5_neutral_~_8wekyb3d8bbwe``,
        or ``None`` when the name does not carry a valid version.
        """
        if not package_full_name:
            return None
        parts = package_full_name.split("_")
        if len(parts) >= 2 and re.fullmatch(r"\d+\.\d+\.\d+\.\d+", parts[1]):
            return parts[1]
        return None

    @staticmethod
    def _read_registry_value(root, path, value_name):
        """Return the string value ``value_name`` under ``root\\path``, or ``None``
        when the key or the value does not exist (or is not accessible).
        """
        try:
            with winreg.OpenKey(root, path) as key:
                value, _ = winreg.QueryValueEx(key, value_name)
                return value if isinstance(value, str) else None
        except OSError:
            return None

    @staticmethod
    def _iter_subkey_names(root, path):
        """Yield the names of the direct subkeys under ``root\\path``."""
        try:
            with winreg.OpenKey(root, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    yield winreg.EnumKey(key, i)
        except OSError:
            # The key is missing or access is denied - nothing to enumerate.
            return

    @staticmethod
    def _version_from_exe_file(exe_path):
        """Return the file version of ``exe_path`` (e.g. ``"1.1.4.5"``), or ``None``
        when it cannot be read.
        """
        try:
            if not exe_path.is_file():
                return None
            pe = pefile.PE(str(exe_path))
            try:
                if hasattr(pe, "VS_FIXEDFILEINFO") and pe.VS_FIXEDFILEINFO:
                    ver_info = pe.VS_FIXEDFILEINFO[0]
                    ms = ver_info.FileVersionMS
                    ls = ver_info.FileVersionLS
                    return f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
            finally:
                pe.close()
        except Exception:
            return None

    @staticmethod
    def _version_from_powershell():
        """Return the Microsoft PC Manager (Microsoft Store) version via Windows
        PowerShell, or ``None`` when it cannot be determined.

        ``-AllUsers`` requires administrator privileges and is only tried when
        the process is running elevated; otherwise it is skipped.
        """
        for use_all_users in (True, False):
            if use_all_users and not AdvancedStartup.is_administrator():
                continue

            all_users_arg = " -AllUsers" if use_all_users else ""
            command = (
                fr"(Get-AppxPackage{all_users_arg} | "
                r"Where-Object { $_.Name -match '^Microsoft\.(MicrosoftPCManager|PCManager)$' }).Version"
            )

            try:
                result = subprocess.run(
                    [
                        str(WindowsUtilities.powershell()),
                        "-NoProfile",
                        "-NonInteractive",
                        "-Command",
                        command,
                    ],
                    check=False,
                    shell=False,
                    text=True,
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=10,
                )
            except subprocess.TimeoutExpired:
                continue
            except Exception:
                return None

            if result.returncode == 0:
                version = result.stdout.strip()
                if version and re.fullmatch(r"\d+\.\d+\.\d+\.\d+", version):
                    return version

        return None
