import os
import subprocess
from tkinter import messagebox

from core import (
    AppSettings,
    InternalViewer,
    PrerequisiteChecks,
    WindowsUtilities
)


class ViewTextFile:
    @staticmethod
    def open_text_file(logger=None, text_file_path=None, app_translator=None):
        text_file_path = text_file_path

        def open_with_startfile():
            logger.info(f"Opening text file {text_file_path} with os.startfile.")
            os.startfile(text_file_path)

        def open_with_cmd():
            logger.info(f"Opening text file {text_file_path} via CMD.")
            subprocess.run([str(WindowsUtilities.cmd()), "/C", "start", "Text File", f"{text_file_path}"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening text file {text_file_path} via Windows PowerShell.")
            subprocess.run([str(WindowsUtilities.powershell()), "-NoProfile", "-Command", f"Start-Process '{text_file_path}'"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_explorer():
            logger.info(f"Opening text file {text_file_path} via File Explorer.")
            subprocess.run(["explorer.exe", f"/select,{text_file_path}"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_internal_viewer():
            logger.info(f"Opening text file {text_file_path} with internal viewer.")
            InternalViewer.open(
                file_path=text_file_path,
                app_translator=app_translator
            )

        if AppSettings.is_use_internal_viewer_enabled():
            methods = [open_with_internal_viewer]
        elif PrerequisiteChecks.check_windows_server_levels():
            methods = [
                open_with_startfile,
                open_with_cmd,
                open_with_powershell
            ]
        else:
            methods = [
                open_with_startfile,
                open_with_cmd,
                open_with_powershell,
                open_with_explorer
            ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the text file {text_file_path} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the text file {text_file_path}: {e}")
                continue
        logger.error(f"All methods failed to open the text file {text_file_path}.")

        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))

        messagebox.showerror(
            app_translator.translate("common.error"),
            app_translator.translate("handlers.open_text_file_error").format(log_file_path=text_file_path)
        )
