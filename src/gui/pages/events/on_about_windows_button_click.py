import os
import subprocess
from tkinter import messagebox


class OnAboutWindowsButtonClick:
    @staticmethod
    def open_about_windows(logger=None, log_file_path=None, app_translator=None):
        about_windows_uri = "ms-settings:about"

        def open_with_startfile():
            logger.info("Opening About Windows page via os.startfile.")
            os.startfile(about_windows_uri)
        def open_with_cmd():
            logger.info("Opening About Windows page via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "About Windows", f"{about_windows_uri}"], check=True,
                           shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info("Opening About Windows page via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{about_windows_uri}'"],
                           check=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the About Windows page via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Open the About Windows Page: {e}")
                continue
        logger.error("All methods failed to open the About Windows page.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_open_about_windows").format(log_file_path=log_file_path)
        )
