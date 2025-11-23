import webbrowser

from core.program_logger import ProgramLogger


class DownloadMicrosoftPCManagerApplicationPackageFromOneDrive:
    def __init__(self, logger=None):
        self.logger = logger or ProgramLogger.get_logger()

    def execute(self):
        download_url = "https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EoscJOQ9taJFtx9LZLPiBM0BEmVm7wsLuJOuHnwmo9EQ5w"
        try:
            webbrowser.open_new(download_url)
            self.logger.info(f"Opened OneDrive Page: {download_url}")
            return True
        except Exception:
            self.logger.exception("Failed to open OneDrive page.")
            return False
