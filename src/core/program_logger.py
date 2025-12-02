import locale
import logging
import os
import tempfile
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.advanced_startup import AdvancedStartup
from core.program_metadata import ProgramMetadata


class ProgramLogger:
    """
    Logging Levels:
    DEBUG    Detailed information, typically of interest only when diagnosing problems.
    INFO     Confirmation that things are working as expected.
    WARNING  An indication that something unexpected happened, or indicative of some problem
    ERROR    Due to a more serious problem, the software has not been able to perform some function.
    CRITICAL A serious error, indicating that the program itself may be unable to continue
    """
    _logger = None
    _log_file = None

    @staticmethod
    def get_logger():
        if ProgramLogger._logger is None:
            ProgramLogger._initialize_logger()
        return ProgramLogger._logger

    @staticmethod
    def get_log_file_path():
        if ProgramLogger._log_file is None:
            ProgramLogger._initialize_logger()
        return str(ProgramLogger._log_file)

    @staticmethod
    def _initialize_logger():
        # Set locale to the user's default setting to respect system date/time format.
        try:
            locale.setlocale(locale.LC_ALL, "")
        except locale.Error:
            # In case of any issue, we can log it or just pass.
            pass

        try:
            log_dir = Path(tempfile.gettempdir()) / "MSPCManagerHelper"
            log_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError):
            # If the default temporary directory is not accessible, fall back to %SystemRoot%\Temp.
            log_dir = Path(os.environ["SystemRoot"]) / "Temp" / "MSPCManagerHelper"
            # Create the directory if it does not exist.
            log_dir.mkdir(parents=True, exist_ok=True)

        # Use a fixed log file name to enable rotation.
        log_file = log_dir / f"{ProgramMetadata.PROGRAM_NAME}.log"
        ProgramLogger._log_file = log_file  # Path to the log file.

        # Add a newline to separate logs from different runs, if the log file already exists.
        if log_file.exists() and log_file.stat().st_size > 0:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write("\n")

        logger = logging.getLogger(ProgramMetadata.PROGRAM_NAME)
        log_level = logging.DEBUG if AdvancedStartup.is_debugmode() else logging.INFO
        logger.setLevel(log_level)

        # Create a rotating file handler.
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setLevel(log_level)

        # Create a console handler.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Create a formatter and set it for both handlers.
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger.
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        ProgramLogger._logger = logger
