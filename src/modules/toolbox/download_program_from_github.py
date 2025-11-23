import webbrowser

from core.program_logger import ProgramLogger


class DownloadProgramFromGitHub:
    def __init__(self, logger=None):
        self.logger = logger or ProgramLogger.get_logger()

    def execute(self):
        download_url = "https://github.com/Goo-aw233/MSPCManagerHelper/releases"
        try:
            webbrowser.open_new(download_url)
            self.logger.info(f"Opened GitHub Releases: {download_url}")
            return True
        except Exception:
            self.logger.exception("Failed to open GitHub releases.")
            return False
