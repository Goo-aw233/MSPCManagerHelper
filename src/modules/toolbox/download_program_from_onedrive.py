import os
import subprocess
import webbrowser

from core.program_logger import ProgramLogger


class DownloadProgramFromOneDrive:
    def __init__(self, logger=None):
        self.logger = logger or ProgramLogger.get_logger()

    def execute(self):
        download_url = "https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EtKwa-2la71HmG2RxkB5lngBvvRt9CFOYsyJG_HOwYIzNA"

        try:
            opened = webbrowser.open_new(download_url)
            if opened:
                self.logger.info(f"Opened OneDrive Page: {download_url}")
                return True
            else:
                self.logger.warning(f"webbrowser.open_new returned False for {download_url}. Trying os.startfile fallback...")
        except Exception as e_webbrowser:
            self.logger.warning(f"Failed to open {download_url} via webbrowser.open_new: {e_webbrowser}. Trying os.startfile fallback...")

        try:
            os.startfile(download_url)
            self.logger.info(f"Opened OneDrive Page via os.startfile: {download_url}")
            return True
        except Exception as e_os:
            self.logger.warning(f"Failed to open {download_url} via os.startfile: {e_os}. Trying CMD fallback...")

        try:
            subprocess.run(
                ["cmd.exe", "/C", "start", "OneDrive Page", f"{download_url}"],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.logger.info(f"Opened OneDrive Page via CMD: {download_url}")
            return True
        except Exception as e_cmd:
            self.logger.warning(f"Failed to open {download_url} via CMD: {e_cmd}. Trying Windows PowerShell fallback...")

        try:
            subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{download_url}'"],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.logger.info(f"Opened OneDrive Page via Windows PowerShell: {download_url}")
            return True
        except Exception as e_windows_powershell:
            self.logger.error(f"Failed to open OneDrive page via all methods. Error: {e_windows_powershell}")
            return False
