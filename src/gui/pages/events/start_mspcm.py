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
            logger.info("Opening Microsoft PC Manager via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "Microsoft PC Manager", f"{registered_class}"], check=True,
                           shell=False, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info("Opening Microsoft PC Manager via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{registered_class}'"],
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
                logger.info(f"Successfully opened the Microsoft PC Manager via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the Microsoft PC Manager: {e}")
                continue
        logger.error("All methods failed to open the Microsoft PC Manager.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_mspcm").format(log_file_path=log_file_path)
        )
