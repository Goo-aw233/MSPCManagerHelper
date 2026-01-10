import os
import subprocess
import webbrowser
from tkinter import messagebox


class OnPrivacySettingsButtonClick:
    @staticmethod
    def open_privacy_settings(logger=None, log_file_path=None, app_translator=None):
        privacy_settings_uri = "ms-settings:privacy"

        def open_with_startfile():
            logger.info("Opening Privacy & Security page via os.startfile.")
            os.startfile(privacy_settings_uri)

        def open_with_cmd():
            logger.info("Opening Privacy & Security page via cmd.")
            subprocess.run(["cmd.exe", "/C", "start", "Privacy Settings", f"{privacy_settings_uri}"], check=True,
                           shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info("Opening Privacy & Security page via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{privacy_settings_uri}'"],
                           check=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Privacy & Security page via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Open the Privacy & Security Page: {e}")
                continue
        logger.error("All methods failed to open the Privacy & Security page.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_open_privacy_settings").format(log_file_path=log_file_path)
        )
