import webbrowser
from tkinter import messagebox


def on_get_help_button_click(logger, translator):
    messagebox.showinfo(
        title=translator.translate("info"),
        message=translator.translate("redirect_to_official_website_to_get_help")
    )
    webbrowser.open_new("https://pcmanager.microsoft.com")
    logger.info("Redirected user to official website for help.")
