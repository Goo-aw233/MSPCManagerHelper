import os
import sys
from pathlib import Path

from windows_toasts import WindowsToaster, Toast

from core.advanced_startup import AdvancedStartup
from core.app_logger import AppLogger
from core.app_metadata import AppMetadata
from core.app_settings import AppSettings


class CleanupAfterExit:
    logger = AppLogger.get_logger()

    @staticmethod
    def cleanup_all():
        CleanupAfterExit.cleanup_prefetch()
        CleanupAfterExit.cleanup_toast_notifications()
        CleanupAfterExit.cleanup_logs()

    @staticmethod
    def cleanup_logs():
        if AppSettings.is_cleanup_after_exit_enabled():
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
        try:
            if not AppSettings.is_cleanup_after_exit_enabled():
                return
            if not AdvancedStartup.is_administrator():
                CleanupAfterExit.logger.info("Skip Prefetch Clean Up: Not Running as Administrator")
                return

            exe_path = Path(sys.argv[0]).resolve()
            if exe_path.suffix.lower() == ".exe":
                exe_name_29 = exe_path.name[:29].upper()
                CleanupAfterExit.logger.info(f"EXE Name for Matching: {exe_name_29}")
                prefetch_dir = Path(os.environ["SystemRoot"]) / "Prefetch"
                if prefetch_dir.exists() and prefetch_dir.is_dir():
                    pf_files = list(prefetch_dir.glob("*.pf"))
                    CleanupAfterExit.logger.info(f"Prefetch Files Found: {[pf.name for pf in pf_files]}")
                    for pf_file in pf_files:
                        if pf_file.name.startswith(exe_name_29):
                            CleanupAfterExit.logger.info(f"Matched Prefetch File: {pf_file.name}")
                            try:
                                pf_file.unlink()
                                CleanupAfterExit.logger.info(f"Removed Prefetch File: {pf_file.name}")
                                if pf_file.exists():
                                    CleanupAfterExit.logger.warning(f"Prefetch File Still Exists After Deletion: {pf_file.name}")
                                else:
                                    CleanupAfterExit.logger.info(f"Prefetch File Successfully Removed: {pf_file.name}")
                            except Exception as e:
                                CleanupAfterExit.logger.warning(f"Failed to Remove {pf_file}: {e}")
                else:
                    CleanupAfterExit.logger.info("Prefetch directory not found or not a directory.")
            else:
                CleanupAfterExit.logger.info("Skip Prefetch Clean Up: Not Running as EXE")
        except Exception as e:
            CleanupAfterExit.logger.warning(f"Failed to Clean Up Prefetch: {e}")

    @staticmethod
    def cleanup_toast_notifications():
        if not AppSettings.is_cleanup_after_exit_enabled():
            return
        try:
            toaster = WindowsToaster(AppMetadata.APP_NAME)
            run_as_administrator_toast = Toast()
            run_as_administrator_toast.tag = "administrator_required_toast"
            toaster.remove_toast(run_as_administrator_toast)
            CleanupAfterExit.logger.info("Toast notifications cleaned up.")
        except Exception as e:
            CleanupAfterExit.logger.warning(f"Failed to Clean Up Toast Notifications: {e}")
