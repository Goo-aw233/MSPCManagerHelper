import os
import subprocess
import webbrowser
from tkinter import messagebox


class URLHandler:
    """
    USAGE EXAMPLE:

    URLHandler.launch_url(
        url="https://example.com",
        target_name="Example Name", # To provide context in logs and error messages.
        messagebox_error_message="translation_key_for_error_message",
        logger=self.logger,
        log_file_path=self.log_file_path,
        app_translator=self.app_translator
    )
    """

    @staticmethod
    def launch_url(url, target_name, messagebox_error_message, logger=None, log_file_path=None, app_translator=None, **format_kwargs):
        def open_with_webbrowser():
            logger.info(f"Opening {target_name} ({url}) via webbrowser.")
            webbrowser.open(url)

        def open_with_startfile():
            logger.info(f"Opening {target_name} ({url}) via os.startfile.")
            os.startfile(url)

        def open_with_cmd():
            logger.info(f"Opening {target_name} ({url}) via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", target_name, f"{url}"], check=True,
                           shell=False, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_windows_powershell():
            logger.info(f"Opening {target_name} ({url}) via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{url}'"],
                           check=True, shell=False, text=True, capture_output=True,
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
                logger.info(f"Successfully opened the {target_name} ({url}) via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the {target_name} ({url}): {e}")
                continue

        logger.error(f"All methods failed to open the {target_name} ({url}).")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))

        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(messagebox_error_message).format(log_file_path=log_file_path, **format_kwargs)
        )
