import customtkinter
from core.app_metadata import AppMetadata
from core.app_resources import AppResources


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._configure_window()

    def _configure_window(self):
        self.title(f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION}")

        icon_path = AppResources.app_icon()
        if icon_path:
            self.iconbitmap(icon_path)

        self._set_window_geometry()

    def _set_window_geometry(self):
        # Use a target size that feels native, but ensure it fits within 85% of the screen for smaller displays.
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        target_width = 1100
        target_height = 750

        width = min(target_width, int(screen_width * 0.85))
        height = min(target_height, int(screen_height * 0.85))

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(800, 600)
