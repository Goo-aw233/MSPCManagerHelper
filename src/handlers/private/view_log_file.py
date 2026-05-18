import os
import subprocess
from tkinter import messagebox

from core import (
    AdvancedStartup,
    AppSettings,
    InternalViewer,
    PrerequisiteChecks
)


class ViewLogFile:
    _internal_viewer_window = None

    @staticmethod
    def open_log_file(logger=None, log_file_path=None, app_translator=None):
        log_file_path = log_file_path

        def open_with_startfile():
            logger.info(f"Opening log file {log_file_path} with os.startfile.")
            os.startfile(log_file_path)

        def open_with_cmd():
            logger.info(f"Opening log file {log_file_path} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "Log File", f"{log_file_path}"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_windows_powershell():
            logger.info(f"Opening log file {log_file_path} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{log_file_path}'"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_explorer():
            logger.info(f"Opening log file {log_file_path} via File Explorer.")
            subprocess.run(["explorer.exe", f"/select,{log_file_path}"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_internal_viewer():
            logger.info(f"Opening log file {log_file_path} with internal viewer.")

            if ViewLogFile._internal_viewer_window and ViewLogFile._internal_viewer_window.winfo_exists():
                ViewLogFile._internal_viewer_window.lift()
                ViewLogFile._internal_viewer_window.focus_force()
                return

            ViewLogFile._internal_viewer_window = InternalViewer(
                file_path=log_file_path,
                app_translator=app_translator
            )

        if AppSettings.is_use_internal_viewer_enabled():
            methods = [open_with_internal_viewer]
        elif not AdvancedStartup.is_bypass_checks() and PrerequisiteChecks.check_windows_server_levels():
            methods = [
                open_with_startfile,
                open_with_cmd,
                open_with_windows_powershell
            ]
        else:
            methods = [
                open_with_startfile,
                open_with_cmd,
                open_with_windows_powershell,
                open_with_explorer
            ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the log file {log_file_path} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the log file {log_file_path}: {e}")
                continue
        logger.error(f"All methods failed to open the log file {log_file_path}.")

        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))

        messagebox.showerror(
            app_translator.translate("common.error"),
            app_translator.translate("handlers.open_log_file_error").format(log_file_path=log_file_path)
        )
