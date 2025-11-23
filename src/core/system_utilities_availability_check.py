import os
import shutil
import subprocess
from pathlib import Path
from subprocess import CompletedProcess

import psutil

from core.program_logger import ProgramLogger


class SystemUtilitiesAvailabilityCheck:
    @staticmethod
    def check_system_utilities_availability() -> dict[str, bool]:
        # Text output without encoding errors group.
        text_based_utilities: list[str] = [
            "cmd.exe",
            "Dism.exe",
            "powershell.exe",
            "reg.exe",
            "sc.exe",
            "where.exe"
        ]

        # Encoding errors group.
        byte_based_utilities: list[str] = [
            "sfc.exe"
        ]

        availability_status: dict[str, bool] = {}

        # Processing text mode utilities.
        for utility in text_based_utilities:
            try:
                result: CompletedProcess = subprocess.run(
                    [utility, "/?"],
                    capture_output=True,
                    text=True,
                    check=False,
                    errors="ignore",  # Ignore potential decoding errors for robustness.
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                is_available: bool = result.stdout.strip() != "" or result.stderr.strip() != ""
                availability_status[utility] = is_available
            except FileNotFoundError:
                availability_status[utility] = False
            except Exception:
                availability_status[utility] = False

        # Processing byte mode utilities.
        for utility in byte_based_utilities:
            try:
                result: CompletedProcess = subprocess.run(
                    [utility, "/?"],
                    capture_output=True,
                    text=False,  # Run in byte stream mode.
                    check=False,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                is_available: bool = result.stdout.strip() != b"" or result.stderr.strip() != b""
                availability_status[utility] = is_available
            except FileNotFoundError:
                availability_status[utility] = False
            except Exception:
                availability_status[utility] = False
        
        return availability_status

    @staticmethod
    def check_narrator_status() -> bool:
        for proc in psutil.process_iter(["name"]):
            try:
                if "narrator" in proc.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    @staticmethod
    def check_system_utilities_version() -> None:
        logger = ProgramLogger.get_logger()
        logger.info("---------- Checking System Utilities Version ----------")
        utilities: list[str] = [
            "cmd.exe",
            "Dism.exe",
            "powershell.exe",
            "reg.exe",
            "sc.exe",
            "sfc.exe",
            "where.exe"
        ]

        for utility in utilities:
            # Use shutil.which() to find the full path of the executable.
            exe_path = shutil.which(utility)

            # Check if a path was found and the file exists.
            if exe_path and Path(exe_path).exists():
                try:
                    import win32api
                    info = win32api.GetFileVersionInfo(exe_path, "\\")
                    if info:
                        ms, ls = info["FileVersionMS"], info["FileVersionLS"]
                        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
                        logger.info(f"{exe_path} Version: {version}")
                    else:
                        logger.warning(f"Could not retrieve version info for {utility} at {exe_path}.")
                except (FileNotFoundError, ImportError) as e:
                    logger.warning(f"Failed to get version for {utility} due to an error: {e}")
            else:
                logger.warning(f"{utility} not found in PATH.")
        logger.info("---------- System Utilities Version Check Completed ----------")

    @staticmethod
    def check_system_path_availability() -> None:
        logger = ProgramLogger.get_logger()
        logger.info("---------- Checking System PATH Availability ----------")

        system_root = os.environ.get("SystemRoot")
        if not system_root:
            logger.error("SystemRoot environment variable not found.")
            logger.info("---------- System PATH Availability Check Completed ----------")
            return
        else:
            logger.info(f"Exist: {system_root}")

        path_env = os.environ.get("PATH", "").lower()
        path_dirs = [p.rstrip("\\") for p in path_env.split(os.pathsep)]

        paths_to_check = [
            os.path.join(system_root, "system32"),
            os.path.join(system_root, "System32", "WindowsPowerShell", "v1.0")
        ]

        all_paths_found = True
        for path_to_check in paths_to_check:
            if path_to_check.lower().rstrip("\\") in path_dirs:
                logger.info(f"Exist: {path_to_check}")
            else:
                logger.warning(f"System PATH is missing: {path_to_check}")
                all_paths_found = False

        if all_paths_found:
            logger.info("All critical system paths are present in the PATH environment variable.")

        logger.info("---------- System PATH Availability Check Completed ----------")
