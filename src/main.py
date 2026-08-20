import atexit

from core.advanced_startup import AdvancedStartup
from core.app_user_model_id import AppUserModelID
from core.cleanup_after_exit import CleanupAfterExit
from gui import HelpWindow, MainWindow


def main():
    if AdvancedStartup.is_open_help_window():
        app = HelpWindow()
    else:
        atexit.register(CleanupAfterExit.cleanup_all)
        AppUserModelID.register()
        app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
