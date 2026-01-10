import os
import subprocess
from tkinter import messagebox


class StartMSPCM:
    @staticmethod
    def start_mspcm(logger=None, log_file_path=None, app_translator=None):
        registered_class = "shell:AppsFolder\\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe!App"

        def open_with_startfile():
            logger.info("Opening Microsoft PC Manager via os.startfile.")
            os.startfile(registered_class)

        def open_with_cmd():
            logger.info("Opening Microsoft PC Manager via cmd.")
            subprocess.run(["cmd.exe", "/C", "start", "Microsoft PC Manager", f"{registered_class}"], check=True,
                           shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info("Opening Microsoft PC Manager via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{registered_class}'"],
                           check=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Microsoft PC Manager via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Open the Microsoft PC Manager: {e}")
                continue
        logger.error("All methods failed to open the Microsoft PC Manager.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_open_mspcm").format(log_file_path=log_file_path)
        )
