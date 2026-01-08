import os
import subprocess
import webbrowser
from tkinter import messagebox


class OnOfficialWebsiteButtonClick:
    @staticmethod
    def open_official_website(logger=None, log_file_path=None, app_translator=None):
        official_website_url = "https://pcmanager.microsoft.com"

        def open_with_webbrowser():
            logger.info("Opening Official Website via webbrowser.")
            webbrowser.open(official_website_url)

        def open_with_startfile():
            logger.info("Opening Official Website via os.startfile.")
            os.startfile(official_website_url)
        def open_with_cmd():
            logger.info("Opening Official Website via cmd.")
            subprocess.run(["cmd.exe", "/C", "start", "Official Website", f"{official_website_url}"], check=True,
                           shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info("Opening Official Website via powershell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{official_website_url}'"],
                           check=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Official Website via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Open the Official Website: {e}")
                continue
        logger.error("All methods failed to open the Official Website.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_open_official_website").format(log_file_path=log_file_path)
        )
