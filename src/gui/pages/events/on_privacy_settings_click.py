import os
import subprocess
import webbrowser


def on_privacy_settings_click(logger):
    privacy_settings_uri = "ms-settings:privacy"

    try:
        os.startfile(privacy_settings_uri)
        logger.info("Opened privacy settings via os.startfile.")
    except Exception as e_os:
        logger.warning(f"os.startfile failed: {e_os}. Trying CMD fallback...")

        cmd_success = False
        try:
            subprocess.run(
                ["cmd.exe", "/C", "start", "Privacy Settings", f"{privacy_settings_uri}"],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            logger.info("Opened privacy settings via CMD.")
            cmd_success = True
        except Exception as e_cmd:
            logger.warning(f"CMD start failed: {e_cmd}. Trying webbrowser fallback...")

        if not cmd_success:
            powershell_success = False
            try:
                subprocess.run(
                    ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{privacy_settings_uri}'"],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                logger.info("Opened privacy settings via PowerShell Start-Process.")
                powershell_success = True
            except Exception as e_windows_powersshell:
                logger.warning(f"PowerShell Start-Process failed: {e_windows_powersshell}. Trying webbrowser fallback...")

            if not powershell_success:
                try:
                    webbrowser.open(privacy_settings_uri)
                    logger.info("Opened privacy settings via webbrowser.")
                except Exception as e_webbrowser:
                    logger.error(f"Failed to open privacy settings via all methods. Error: {e_webbrowser}")
