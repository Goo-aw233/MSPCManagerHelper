import atexit

from core.advanced_startup import AdvancedStartup
from core.app_logger import AppLogger
from core.app_translator import AppTranslator
from core.app_user_model_id import AppUserModelID
from core.cleanup_after_exit import CleanupAfterExit
from gui import HelpWindow, MainWindow
from handlers.shared import RestartProgram


def _request_run_as_administrator():
    logger = AppLogger.get_logger()

    if AdvancedStartup.is_administrator():
        logger.info(
            "The /runas parameter is set, but the application is already running "
            "as administrator. Ignoring the parameter and launching normally."
        )
        return False

    logger.info(
        "The /runas parameter is set. Relaunching the application as administrator..."
    )

    launch_args = AdvancedStartup.remove_runas_argument(AdvancedStartup.get_runtime_arguments())

    return RestartProgram.restart_program(
        AdvancedStartup,
        logger=logger,
        app_translator=AppTranslator(
            AdvancedStartup.specify_locale() or AppTranslator.detect_system_language()
        ),
        log_file_path=AppLogger.get_log_file_path(),
        verb="runas",
        launch_args=launch_args,
    )


def main():
    if AdvancedStartup.is_runas():
        # A successful elevated restart exits this process (SystemExit inside
        # RestartProgram); on failure or when already elevated it returns and
        # we fall through to a normal launch below.
        _request_run_as_administrator()
    if AdvancedStartup.is_open_help_window():
        app = HelpWindow()
    else:
        atexit.register(CleanupAfterExit.cleanup_all)
        AppUserModelID.register()
        app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
