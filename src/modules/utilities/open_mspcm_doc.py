import os
import subprocess
import webbrowser
from tkinter import messagebox

from core.app_translator import AppTranslator


class OpenMSPCMDoc:
    @staticmethod
    def open_mspcm_doc(logger=None, log_file_path=None, app_translator=None):
        # Use detected system language if no translator is provided.
        locale = app_translator.locale if app_translator else AppTranslator.detect_system_language()
        logger.info(f"Detected System Locale: {locale}")
        mspcm_doc_url = "https://docs.qq.com/doc/DR2FrVkJmT0NuZ0Zx" if locale == "zh-cn" else \
            "https://mspcmanager.github.io/mspcm-docs"

        def open_with_webbrowser():
            logger.info("Opening Microsoft PC Manager Help Documentation page via webbrowser.")
            webbrowser.open(mspcm_doc_url)

        def open_with_startfile():
            logger.info("Opening Microsoft PC Manager Help Documentation page via os.startfile.")
            os.startfile(mspcm_doc_url)

        def open_with_cmd():
            logger.info("Opening Microsoft PC Manager Help Documentation page via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "MSPC Doc", f"{mspcm_doc_url}"], check=True,
                           shell=False, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_windows_powershell():
            logger.info("Opening Microsoft PC Manager Help Documentation page via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{mspcm_doc_url}'"],
                           check=True, text=True, capture_output=True, shell=False,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_windows_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Microsoft PC Manager Help Documentation page via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the Microsoft PC Manager Help Documentation page: {e}")
                continue
        logger.error("All methods failed to open the Microsoft PC Manager Help Documentation page.")
        
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))

        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_mspcm_doc").format(log_file_path=log_file_path, mspcm_doc_url=mspcm_doc_url)
        )
