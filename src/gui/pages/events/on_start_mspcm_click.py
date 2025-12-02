import os
import subprocess
import webbrowser


def on_start_mspcm_click(logger):
    registered_class = "shell:AppsFolder\\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe!App"

    try:
        os.startfile(registered_class)
        logger.info(f"Successfully Started Microsoft PC Manager Via os.startfile: {registered_class}")
    except Exception as e_os:
        logger.warning(f"Failed to start via os.startfile: {e_os}. Trying CMD fallback...")
        try:
            subprocess.run(["cmd.exe", "/C", "start", "Start Microsoft PC Manager", f"{registered_class}"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info(f"Successfully Started Microsoft PC Manager Via CMD: {registered_class}")
        except Exception as e_cmd:
            logger.warning(f"Failed to start Microsoft PC Manager via CMD: {e_cmd}. Trying Windows PowerShell fallback...")
            try:
                subprocess.run(
                    ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{registered_class}'"],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                logger.info(f"Successfully Started Microsoft PC Manager Via Windows PowerShell: {registered_class}")
            except Exception as e_windows_powershell:
                logger.warning(f"Failed to start Microsoft PC Manager via Windows PowerShell: {e_windows_powershell}. Trying webbrowser fallback...")
                try:
                    webbrowser.open(registered_class)
                    logger.info(f"Successfully Started Microsoft PC Manager Via webbrowser: {registered_class}")
                except Exception as e_webbrowser:
                    logger.error(f"Failed to start Microsoft PC Manager. Error: {e_webbrowser}")
