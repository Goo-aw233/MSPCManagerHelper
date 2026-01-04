from core.advanced_startup import AdvancedStartup
from gui import HelpWindow, MainWindow


def main():
    if AdvancedStartup.is_open_help_window():
        app = HelpWindow()
    else:
        app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
