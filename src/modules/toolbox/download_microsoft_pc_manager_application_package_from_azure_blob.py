import webbrowser

from core.program_logger import ProgramLogger


class DownloadMicrosoftPCManagerApplicationPackageFromAzureBlob():
    def __init__(self, logger=None):
        self.logger = logger or ProgramLogger.get_logger()

    def execute(self):
        download_url = "https://kaoz.uk/PCManagerOFL"
        try:
            webbrowser.open_new(download_url)
            self.logger.info(f"Opened Azure Blob Page: {download_url}")
            return True
        except Exception:
            self.logger.exception("Failed to open Azure Blob page.")
            return False
