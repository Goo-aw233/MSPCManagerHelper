import webbrowser

from core.program_logger import ProgramLogger
from core.program_settings import ProgramSettings


class DownloadMicrosoftEdgeWebView2Runtime:
    def __init__(self, logger=None):
        self.logger = logger or ProgramLogger.get_logger()

    def execute(self):
        base_url = "https://developer.microsoft.com/microsoft-edge/webview2"
        if ProgramSettings.is_support_developer_enabled():
            download_url = base_url + ProgramSettings.get_student_ambassador_cid()
        else:
            download_url = base_url
        try:
            webbrowser.open_new(download_url)
            self.logger.info(f"Opened Microsoft Edge WebView2 Runtime Download Page: {download_url}")
            return True
        except Exception:
            self.logger.exception("Failed to open Microsoft Edge WebView2 Runtime download page.")
            return False
