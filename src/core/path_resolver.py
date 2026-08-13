"""Path Resolution Fallback Chain

Environment Variable > Known Folder API > Hardcoded Default:
- Prefer the environment variable (e.g. %ProgramData%).
- If missing, resolve via the Win32 Known Folder API (SHGetKnownFolderPath, ctypes → shell32).
- If that also fails, fall back to a hardcoded default based on the system drive.
"""

import ctypes
import functools
import os
import shutil
from ctypes import wintypes
from pathlib import Path


class PathResolver:
    """Resolver for key Windows system paths (env var → Known Folder API → hardcoded fallback)."""

    # Known Folder GUIDs (KNOWNFOLDERID)
    _FOLDERID_WINDOWS = "F38BF404-1D43-42F2-9305-67DE0B28FC23"
    _FOLDERID_PROGRAM_DATA = "62AB5D82-FDC1-4DC3-A9DD-070D1D495D97"
    _FOLDERID_LOCAL_APP_DATA = "F1B32785-6FBA-4FCF-9D55-7B8E7F157091"
    _FOLDERID_PROGRAM_FILES = "905e63b6-c1bf-494e-b29c-65b732d3d21a"
    _FOLDERID_PROGRAM_FILES_X86 = "7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E"
    _FOLDERID_PROFILE = "5E6C858F-0E22-4760-9AFE-EA3317B67173"

    @staticmethod
    def _known_folder(guid):
        """Query a Known Folder path via SHGetKnownFolderPath (shell32, ctypes)."""
        try:
            class GUID(ctypes.Structure):
                _fields_ = [
                    ("Data1", wintypes.DWORD),
                    ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD),
                    ("Data4", wintypes.BYTE * 8),
                ]

            # "62AB5D82-FDC1-4DC3-A9DD-070D1D495D97" -> GUID struct
            parts = guid.strip("{}").split("-")
            folder_id = GUID(
                int(parts[0], 16),
                int(parts[1], 16),
                int(parts[2], 16),
                (wintypes.BYTE * 8)(*bytes.fromhex(parts[3] + parts[4])),
            )

            shell32 = ctypes.windll.shell32
            shell32.SHGetKnownFolderPath.argtypes = [
                ctypes.POINTER(GUID),
                wintypes.DWORD,
                wintypes.HANDLE,
                ctypes.POINTER(ctypes.c_wchar_p),
            ]
            shell32.SHGetKnownFolderPath.restype = ctypes.c_long

            path_ptr = ctypes.c_wchar_p()
            if shell32.SHGetKnownFolderPath(
                ctypes.byref(folder_id), 0, None, ctypes.byref(path_ptr)
            ) != 0:
                return None
            try:
                path = path_ptr.value
                return Path(path) if path else None
            finally:
                ctypes.windll.ole32.CoTaskMemFree(path_ptr)
        except Exception:
            return None

    @staticmethod
    def _resolve(env_names, known_folder_guid, fallback):
        """Resolve a path using env vars, then Known Folder API, then a hardcoded fallback."""
        for name in env_names:
            value = os.environ.get(name)
            if value:
                return Path(value)
        path = PathResolver._known_folder(known_folder_guid)
        if path:
            return path
        return fallback()

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def system_drive():
        """System drive root (e.g. Path('C:\\'))."""
        # Must return a path with a root: Path("C:") / "ProgramData" would
        # become the drive-relative "C:ProgramData" (loses the separator).
        drive = os.environ.get("SystemDrive", "C:")
        return Path(drive + os.sep)

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def system_root():
        """Windows directory (e.g. C:\\Windows)."""
        return PathResolver._resolve(
            ("SystemRoot", "WinDir"),
            PathResolver._FOLDERID_WINDOWS,
            lambda: PathResolver.system_drive() / "Windows",
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def program_data():
        """Common application data directory (e.g. C:\\ProgramData)."""
        return PathResolver._resolve(
            ("ProgramData",),
            PathResolver._FOLDERID_PROGRAM_DATA,
            lambda: PathResolver.system_drive() / "ProgramData",
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def local_app_data():
        """Current user's local application data (e.g. C:\\Users\\<user>\\AppData\\Local)."""
        return PathResolver._resolve(
            ("LocalAppData",),
            PathResolver._FOLDERID_LOCAL_APP_DATA,
            lambda: Path.home() / "AppData" / "Local",
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def program_files():
        """64-bit Program Files directory (e.g. C:\\Program Files)."""
        return PathResolver._resolve(
            ("ProgramFiles",),
            PathResolver._FOLDERID_PROGRAM_FILES,
            lambda: PathResolver.system_drive() / "Program Files",
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def program_files_x86():
        """32-bit Program Files directory (e.g. C:\\Program Files (x86))."""
        return PathResolver._resolve(
            ("ProgramFiles(x86)",),
            PathResolver._FOLDERID_PROGRAM_FILES_X86,
            lambda: PathResolver.system_drive() / "Program Files (x86)",
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def user_profile():
        """Current user's profile directory (e.g. C:\\Users\\<user>)."""
        return PathResolver._resolve(
            ("UserProfile",),
            PathResolver._FOLDERID_PROFILE,
            lambda: Path.home(),
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def system32():
        """System32 directory (e.g. C:\\Windows\\System32)."""
        return PathResolver.system_root() / "System32"


class WindowsUtilities:
    """Builder for full paths to built-in Windows utilities.

    Known utilities are resolved directly to their full paths under System32 via
    the mapping table (no PATH dependency); unknown utilities fall back to a PATH
    search (shutil.which); if still not found, the bare name is returned as-is.
    """

    # Normalized name (lowercase, with .exe) → relative path under System32
    _RELATIVE_PATHS = {
        "dism.exe": "Dism.exe",
        "cmd.exe": "cmd.exe",
        "reg.exe": "reg.exe",
        "sc.exe": "sc.exe",
        "sfc.exe": "sfc.exe",
        "taskkill.exe": "taskkill.exe",
        "powershell.exe": "WindowsPowerShell/v1.0/powershell.exe",
    }

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def path(name):
        """Return the full path of a built-in Windows utility."""
        key = Path(name).name.lower()
        if not key.endswith(".exe"):
            key += ".exe"
        relative = WindowsUtilities._RELATIVE_PATHS.get(key)
        if relative is not None:
            return PathResolver.system32() / relative
        found = shutil.which(Path(name).name)
        if found:
            return Path(found)
        return Path(name)

    @staticmethod
    def dism():
        return WindowsUtilities.path("Dism.exe")

    # Windows PowerShell
    @staticmethod
    def powershell():
        return WindowsUtilities.path("powershell.exe")

    @staticmethod
    def cmd():
        return WindowsUtilities.path("cmd.exe")

    @staticmethod
    def reg():
        return WindowsUtilities.path("reg.exe")
