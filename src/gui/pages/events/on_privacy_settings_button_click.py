import os
import subprocess
from tkinter import messagebox


class OnPrivacySettingsButtonClick:
    @staticmethod
    def open_privacy_settings(logger=None, log_file_path=None, app_translator=None):
        privacy_settings_uri = "ms-settings:privacy"

        def open_with_startfile():
            logger.info("Opening Privacy & Security page via os.startfile.")
            os.startfile(privacy_settings_uri)

        def open_with_cmd():
            logger.info("Opening Privacy & Security page via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "Privacy Settings", f"{privacy_settings_uri}"], check=True,
                           shell=False, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info("Opening Privacy & Security page via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{privacy_settings_uri}'"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Privacy & Security page via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the Privacy & Security Page: {e}")
                continue

        logger.error("All methods failed to open the Privacy & Security page.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")

        logger.error("\n".join(error_details))

        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_privacy_settings").format(log_file_path=log_file_path)
        )
