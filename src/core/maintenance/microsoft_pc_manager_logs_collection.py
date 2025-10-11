import ctypes
import datetime
import locale
import os
import subprocess
from pathlib import Path
from gui.modules.get_program_resources import GetProgramResources


class MicrosoftPCManagerLogsCollection:

    def __init__(self):
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()
        self.nsudo_path = GetProgramResources.get_nsudo_path()
        self._BASIC_LOGS_FOLDER = Path(os.getenv("UserProfile")) / "Desktop" / "microsoft_pc_manager_logs_folder"
        if not self._BASIC_LOGS_FOLDER.exists():
            os.makedirs(self._BASIC_LOGS_FOLDER, exist_ok=True)

    def collect_logs(self):
        pass

    @staticmethod
    def _set_paths():
        full_time_str = MicrosoftPCManagerLogsCollection._set_time_settings()
        # The Source Path of the CLR_v4.0 Log Under %LocalAppData%
        _APPDATA_CLR_4_0_LOGS_SOURCE = Path(os.getenv("LocalAppData")) / "Microsoft" / "CLR_v4.0" / "UsageLogs"
        # EXE Installer Log Source Path
        _EXE_SETUP_LOGS_SOURCE = Path(os.getenv("ProgramData")) / "Windows Master Setup"
        # Log Collection Destination Path
        _LOGS_DESTINATION = Path(os.getenv("UserProfile")) / "Desktop" / "microsoft_pc_manager_logs_folder" / full_time_str
        # Log Zip Archive Output Path
        _LOGS_ZIP_ARCHIVE_OUTPUT_PATH = Path(os.getenv("UserProfile")) / "Desktop"
        # Program Logs Source Path
        _PROGRAM_LOGS_SOURCE_PATH = Path(os.getenv("ProgramData")) / "Windows Master Store"
        # The Source Path of the CLR_v4.0 Log Under %SystemRoot%
        _SYSTEMROOT_CLR_4_0_LOGS_SOURCE = (
            Path(os.getenv("SystemRoot"))
            / "System32"
            / "config"
            / "systemprofile"
            / "AppData"
            / "Local"
            / "Microsoft"
            / "CLR_v4.0"
            / "UsageLogs"
        )

    @staticmethod
    def _set_time_settings():
        # Set the Current Windows Time Zone
        locale.setlocale(locale.LC_TIME, '')

        # Get the Current Local Time
        now = datetime.datetime.now()

        # Get the Localized Date and Time Format (Without Microseconds)
        local_dt = now.strftime("%x %X")
        # Concatenate Microseconds
        with_microsecond = f"{local_dt}.{now.microsecond:06d}"
        # Replace the Connector Symbols
        full_time_str = with_microsecond.replace('/', '_').replace(':', '_').replace(' ', '-')

        return full_time_str
