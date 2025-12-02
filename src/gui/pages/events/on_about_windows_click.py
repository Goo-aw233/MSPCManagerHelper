import os
import subprocess
import webbrowser


def on_about_windows_click(logger):
    about_windows_uri = "ms-settings:about"
    try:
        os.startfile(about_windows_uri)
        logger.info(f"Successfully opened {about_windows_uri} via os.startfile.")
    except Exception as e_os:
        logger.warning(f"Failed to open {about_windows_uri} via os.startfile: {e_os}. Trying CMD fallback...")
        try:
            subprocess.run(["cmd.exe", "/C", "start", "About Windows", about_windows_uri], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info(f"Successfully opened {about_windows_uri} via CMD.")
        except Exception as e_cmd:
            logger.warning(f"Failed to open {about_windows_uri} via CMD: {e_cmd}. Trying Windows PowerShell fallback...")
            try:
                subprocess.run(
                    ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{about_windows_uri}'"],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                logger.info(f"Successfully opened {about_windows_uri} via Windows PowerShell.")
            except Exception as e_windows_powershell:
                logger.warning(f"Failed to open {about_windows_uri} via Windows PowerShell: {e_windows_powershell}. Trying webbrowser fallback...")
                try:
                    webbrowser.open(about_windows_uri)
                    logger.info(f"Successfully opened {about_windows_uri} via webbrowser.")
                except Exception as e_webbrowser:
                    logger.error(f"Failed to open {about_windows_uri}. Error: {e_webbrowser}")
