import os
import shutil
import sys
from pathlib import Path

from windows_toasts import WindowsToaster

from core.advanced_startup import AdvancedStartup
from core.app_logger import AppLogger
from core.app_metadata import AppMetadata
from core.app_resources import AppResources
from core.app_settings import AppSettings
from core.path_resolver import PathResolver


class CleanupAfterExit:
    logger = AppLogger.get_logger()

    @staticmethod
    def cleanup_all():
        CleanupAfterExit.cleanup_temp_files()
        CleanupAfterExit.cleanup_prefetch()
        CleanupAfterExit.cleanup_toast_notifications()
        CleanupAfterExit.cleanup_logs()

    @staticmethod
    def cleanup_logs():
        if not AppSettings.is_cleanup_after_exit_enabled():
            return
        for handler in CleanupAfterExit.logger.handlers:
            handler.close()

        try:
            log_file_path = Path(AppLogger.get_log_file_path())
            if log_file_path.exists():
                log_file_path.unlink()
        except Exception as e:
            CleanupAfterExit.logger.warning(f"Failed to Clean Up Log File: {e}")

    @staticmethod
    def cleanup_prefetch():
        if not AppSettings.is_cleanup_after_exit_enabled():
            return
        if not AdvancedStartup.is_administrator():
            CleanupAfterExit.logger.info("Skip Prefetch Clean Up: Not Running as Administrator")
            return

        exe_path = Path(sys.argv[0]).resolve()
        if exe_path.suffix.lower() != ".exe":
            CleanupAfterExit.logger.info("Skip Prefetch Clean Up: Not Running as EXE")
            return

        exe_name_29 = exe_path.name[:29].upper()
        CleanupAfterExit.logger.info(f"EXE Name for Matching: {exe_name_29}")
        prefetch_dir = PathResolver.system_root() / "Prefetch"
        if not (prefetch_dir.exists() and prefetch_dir.is_dir()):
            CleanupAfterExit.logger.info("Prefetch directory not found or not a directory.")
            return

        pf_files = list(prefetch_dir.glob("*.pf"))
        CleanupAfterExit.logger.info(f"Prefetch Files Found: {[pf.name for pf in pf_files]}")
        removed_files = []
        for pf_file in pf_files:
            if pf_file.name.startswith(exe_name_29):
                try:
                    pf_file.unlink()
                    removed_files.append(pf_file.name)
                except Exception as e:
                    CleanupAfterExit.logger.warning(f"Failed to Remove {pf_file.name}: {e}")
        if removed_files:
            CleanupAfterExit.logger.info(
                "Prefetch Files Removed:\n  - " + "\n  - ".join(removed_files)
            )

    @staticmethod
    def cleanup_temp_files():
        if not AppSettings.is_cleanup_after_exit_enabled():
            return
        temp_dir = Path(AppResources.app_temp_dir())
        log_file_path = Path(AppLogger.get_log_file_path())
        if not temp_dir.exists():
            return
        removed_dirs = []
        removed_files = []
        try:
            for item in temp_dir.iterdir():
                if item == log_file_path:
                    continue
                try:
                    if item.is_dir():
                        # Walk Directory Tree to Collect All Nested Items Before Removal
                        for root, dirs, files in os.walk(item):
                            rel_root = Path(root).relative_to(temp_dir)
                            for d in dirs:
                                removed_dirs.append(str(rel_root / d))
                            for f in files:
                                removed_files.append(str(rel_root / f))
                        shutil.rmtree(item, ignore_errors=True)
                        removed_dirs.append(item.name)
                    else:
                        item.unlink()
                        removed_files.append(item.name)
                except Exception as e:
                    CleanupAfterExit.logger.warning(f"Failed to Remove {item.name}: {e}")
            if removed_dirs:
                CleanupAfterExit.logger.info(
                    "Temp Subdirectories Removed:\n  - " + "\n  - ".join(removed_dirs)
                )
            if removed_files:
                CleanupAfterExit.logger.info(
                    "Temp Files Removed:\n  - " + "\n  - ".join(removed_files)
                )
            if removed_dirs or removed_files:
                CleanupAfterExit.logger.info("Temp directory cleaned up.")
        except Exception as e:
            CleanupAfterExit.logger.warning(f"Failed to Clean Up Temp Directory: {e}")

    @staticmethod
    def cleanup_toast_notifications():
        if not AppSettings.is_cleanup_after_exit_enabled():
            return
        try:
            toaster = WindowsToaster(AppMetadata.APP_NAME)
            # Clear every toast belonging to this application regardless of tag,
            # so newly added toast tags do not need to be listed here.
            toaster.clear_toasts()
            CleanupAfterExit.logger.info("Toast notifications cleaned up.")
        except Exception as e:
            CleanupAfterExit.logger.warning(f"Failed to Clean Up Toast Notifications: {e}")
