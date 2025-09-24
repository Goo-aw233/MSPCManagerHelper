import ctypes
import subprocess


class OpenDeveloperSettings:

    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def open_developer_settings(self):
        start_developer_settings_cmd = [
            "cmd.exe",
            "/C",
            "start",
            "ms-settings:developers"
        ]
        try:
            subprocess.run(
                start_developer_settings_cmd,
                creationflags=subprocess.CREATE_NO_WINDOW,
                check=True
            )
            return self.translator.translate("developer_settings_opened_successfully")
        except Exception as e:
            self.error_code = ctypes.get_last_error()
            self.error_message = ctypes.FormatError(self.error_code).strip()
            error_info = (f"{self.translator.translate('exception_context')}: {e}\n"
                          f"{self.translator.translate('error_code')}: {self.error_code}\n"
                          f"{self.translator.translate('error_message')}: {self.error_message}")
            return f"{self.translator.translate('an_error_occurred_when_opening_settings')}\n{error_info}"
