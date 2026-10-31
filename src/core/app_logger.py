import locale
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .advanced_startup import AdvancedStartup
from .app_metadata import AppMetadata
from .app_resources import AppResources


class ColoredConsoleFormatter(logging.Formatter):
    """Custom formatter for console output with ANSI color coding per log level."""

    _RESET = "\033[0m"
    _COLORS = {
        logging.DEBUG: "\033[36m",      # Cyan
        logging.INFO: "\033[32m",       # Green
        logging.WARNING: "\033[33m",    # Yellow
        logging.ERROR: "\033[31m",      # Red
        logging.CRITICAL: "\033[1;31m", # Bold Red
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self._COLORS.get(record.levelno, "")
        original_levelname = record.levelname

        if color:
            # Inject color codes while preserving the 8-character width alignment.
            record.levelname = f"{color}{original_levelname:<8}{self._RESET}"
        else:
            record.levelname = f"{original_levelname:<8}"

        try:
            return super().format(record)
        finally:
            # Restore the original levelname so subsequent handlers (e.g., file handler) are unaffected.
            record.levelname = original_levelname


class AppLogger:
    """Logging Levels:

    DEBUG    Detailed information, typically of interest only when diagnosing problems.
    INFO     Confirmation that things are working as expected.
    WARNING  An indication that something unexpected happened, or indicative of some problem.
    ERROR    Due to a more serious problem, the software has not been able to perform some function.
    CRITICAL A serious error, indicating that the program itself may be unable to continue.
    """
    _logger = None
    _log_file = None

    @staticmethod
    def get_logger():
        if AppLogger._logger is None:
            AppLogger._initialize_logger()
        return AppLogger._logger

    @staticmethod
    def get_log_file_path():
        if AppLogger._log_file is None:
            AppLogger._initialize_logger()
        return str(AppLogger._log_file)

    @staticmethod
    def _initialize_logger():
        # Set locale to the user's default setting to respect system date/time format.
        try:
            locale.setlocale(locale.LC_TIME, "")
        except locale.Error:
            # In case of any issue, we can log it or just pass.
            pass

        log_dir = Path(AppResources.app_temp_dir())
        log_dir.mkdir(parents=True, exist_ok=True)

        # Use a fixed log file name to enable rotation.
        log_file = log_dir / f"{AppMetadata.APP_NAME}.log"
        AppLogger._log_file = log_file  # Path to the log file.

        # Add a newline to separate logs from different runs, if the log file already exists.
        if log_file.exists() and log_file.stat().st_size > 0:
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"\n{'=' * 35} NEW SESSION {'=' * 35}\n\n")
            except OSError:
                pass

        logger = logging.getLogger(AppMetadata.APP_NAME)
        log_level = logging.DEBUG if AdvancedStartup.is_debugmode() else logging.INFO
        logger.setLevel(log_level)
        # Disable propagation to avoid duplicate logs in the root logger.
        logger.propagate = False

        # Create a rotating file handler.
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
            delay=True,  # Delay file creation until the first log message is emitted.
        )
        file_handler.setLevel(log_level)

        # Create a console handler sending logs to stdout.
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        # File Formatter: outputs pure text without any ANSI escape codes.
        file_formatter = logging.Formatter(
            "%(asctime)s | PID:%(process)-5d | %(levelname)-8s | %(filename)28s:%(lineno)-4d | %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        # Console Formatter: outputs colored level names with the same column alignment.
        console_formatter = ColoredConsoleFormatter(
            "%(asctime)s | PID:%(process)-5d | %(levelname)s | %(filename)28s:%(lineno)-4d | %(message)s"
        )
        console_handler.setFormatter(console_formatter)

        # Add the handlers to the logger.
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        AppLogger._logger = logger
