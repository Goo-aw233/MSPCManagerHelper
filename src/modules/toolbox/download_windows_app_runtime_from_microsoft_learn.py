import os
import subprocess
import webbrowser

from core.program_logger import ProgramLogger
from core.program_settings import ProgramSettings


class DownloadWindowsAppRuntimeFromMicrosoftLearn:
    def __init__(self, logger=None):
        self.logger = logger or ProgramLogger.get_logger()

    def execute(self):
        base_url = "https://learn.microsoft.com/windows/apps/windows-app-sdk/downloads-archive"
        if ProgramSettings.is_support_developer_enabled():
            download_url = base_url + ProgramSettings.get_ms_student_ambassador_cid()
        else:
            download_url = base_url

        try:
            opened = webbrowser.open_new(download_url)
            if opened:
                self.logger.info(f"Opened Windows App Runtime Download Page: {download_url}")
                return True
            else:
                self.logger.warning(f"webbrowser.open_new returned False for {download_url}. Trying os.startfile fallback...")
        except Exception as e_webbrowser:
            self.logger.warning(f"Failed to open {download_url} via webbrowser.open_new: {e_webbrowser}. Trying os.startfile fallback...")

        try:
            os.startfile(download_url)
            self.logger.info(f"Opened Windows App Runtime Download Page via os.startfile: {download_url}")
            return True
        except Exception as e_os:
            self.logger.warning(f"Failed to open {download_url} via os.startfile: {e_os}. Trying CMD fallback...")

        try:
            subprocess.run(
                ["cmd.exe", "/C", "start", "Windows App Runtime", f"{download_url}"],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.logger.info(f"Opened Windows App Runtime Download Page via CMD: {download_url}")
            return True
        except Exception as e_cmd:
            self.logger.warning(f"Failed to open {download_url} via CMD: {e_cmd}. Trying Windows PowerShell fallback...")

        try:
            subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{download_url}'"],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.logger.info(f"Opened Windows App Runtime Download Page via Windows PowerShell: {download_url}")
            return True
        except Exception as e_windows_powershell:
            self.logger.error(f"Failed to open Windows App Runtime download page via all methods. Error: {e_windows_powershell}")
            return False
