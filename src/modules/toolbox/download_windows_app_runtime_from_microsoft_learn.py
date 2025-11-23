import webbrowser

from core.program_logger import ProgramLogger
from core.program_settings import ProgramSettings


class DownloadWindowsAppRuntimeFromMicrosoftLearn:
    def __init__(self, logger=None):
        self.logger = logger or ProgramLogger.get_logger()

    def execute(self):
        base_url = "https://learn.microsoft.com/windows/apps/windows-app-sdk/downloads-archive"
        if ProgramSettings.is_support_developer_enabled():
            download_url = base_url + ProgramSettings.get_student_ambassador_cid()
        else:
            download_url = base_url
        try:
            webbrowser.open_new(download_url)
            self.logger.info(f"Opened Windows App Runtime Download Page: {download_url}")
            return True
        except Exception:
            self.logger.exception("Failed to open Windows App Runtime download page.")
            return False
