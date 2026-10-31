import time

from pathlib import Path

import customtkinter

from .advanced_startup import AdvancedStartup
from .app_logger import AppLogger
from .app_metadata import AppMetadata
from .app_resources import AppResources
from .app_settings import AppSettings
from .app_translator import AppTranslator
from .set_font_family import SetFontFamily


class InternalViewer(customtkinter.CTkToplevel):
    # Keyed by resolved file path so the same file reuses its own window while other files open in new windows.
    _open_viewers = {}

    # Monotonic counter so a new window never reuses the offset of a closed one.
    _next_cascade_offset = 0

    # Class-level default so destroy() stays safe if __init__ fails before the instance key is assigned.
    _viewer_key = ""

    @classmethod
    def open(cls, file_path=None, app_translator=None):
        viewer_key = cls._make_viewer_key(file_path)
        existing_viewer = cls._open_viewers.get(viewer_key)

        if isinstance(existing_viewer, InternalViewer) and existing_viewer.winfo_exists():
            existing_viewer.refresh_content()
            existing_viewer.bring_to_front()
            return existing_viewer

        cls._open_viewers.pop(viewer_key, None)
        viewer = cls(file_path=file_path, app_translator=app_translator)
        cls._open_viewers[viewer_key] = viewer
        return viewer

    @staticmethod
    def _make_viewer_key(file_path):
        if not file_path:
            return ""
        try:
            return str(Path(file_path).resolve()).casefold()
        except OSError:
            return str(file_path).casefold()

    def __init__(self, file_path=None, app_translator=None):
        super().__init__()

        self.language = ""
        self.file_path = Path(file_path) if file_path else None
        self.app_translator = app_translator
        self.logger = AppLogger.get_logger()

        self._viewer_key = self._make_viewer_key(file_path)
        self._cascade_offset = 28 * (InternalViewer._next_cascade_offset % 6)
        InternalViewer._next_cascade_offset += 1
        self._last_raise_time = 0.0

        self.logger.info("========================= Initializing Internal Viewer =========================")
        self._set_language()
        self._configure_window()

        # Set font family.
        language = getattr(self, "language", "").lower()
        # Determine whether to follow system font through AppSettings.
        follow_system_font = AppSettings.is_follow_system_font_enabled()
        self.font_family = SetFontFamily.apply_font_setting(follow_system_font=follow_system_font, language=language)
        self.logger.info(f"Follow Font Setting: {follow_system_font}")

        self._create_widgets()

        self.logger.info("========================= Internal Viewer Initialized =========================")

    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.content_textbox = customtkinter.CTkTextbox(
            self,
            font=(SetFontFamily.apply_font_setting(monospaced=True), 13),
            # Set the default state to read-only.
            state="disabled",
            wrap="none"
        )
        self.content_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Right-Click Menu
        # Avoid a core -> gui import cycle while packages initialize.
        from gui.components.widgets.content_menu import ContentMenu

        self.content_menu = ContentMenu(
            parent=self,
            textbox=self.content_textbox,
            app_translator=self.app_translator,
            font_family=self.font_family,
            actions=[
                ContentMenu.REFRESH,
                None,
                ContentMenu.COPY,
                None,
                ContentMenu.SELECT_ALL
            ],
            content_provider=self._read_content,
        )
        self.content_menu.bind_to()
        self.content_menu.load_content(self._read_content() or "")

        # Keyboard Shortcuts
        self.content_textbox.bind("<Control-r>", lambda e: self.refresh_content())
        self.content_textbox.bind("<Control-w>", lambda e: self.destroy())
        self.content_textbox.bind("<Escape>", lambda e: self.destroy())
        self.content_textbox.bind("<F5>", lambda e: self.refresh_content())

    def _configure_window(self):
        if self.file_path:
            app_title = f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION} - {self.file_path.name}"
        else:
            app_title = f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION} Internal Viewer"
        self.title(app_title)

        icon_path = AppResources.app_icon()
        if icon_path:
            self.after(200, lambda: self.iconbitmap(icon_path))
            self.logger.info(f"Window Icon: {icon_path}")

        self._set_window_geometry()

        # The window manager close button runs Tcl's destroy directly, bypassing the overridden destroy().
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Raise and focus once; CTk withdraws/deiconifies the window shortly after creation, so wait it out.
        self.after(250, self.bring_to_front)

    def bring_to_front(self):
        if not self.winfo_exists():
            return

        if self.state() == "iconic":
            self.deiconify()

        self.lift()
        self.focus_force()

        # Skip the topmost flicker if this window was raised moments ago (e.g. a double click).
        now = time.monotonic()
        if now - self._last_raise_time < 0.4:
            return

        self._last_raise_time = now
        # A brief topmost toggle makes the raise stick on Windows without keeping the window always on top.
        self.attributes("-topmost", True)
        self.after(10, lambda: self.winfo_exists() and self.attributes("-topmost", False))

    def _set_language(self):
        if self.app_translator is not None:
            self.language = self.app_translator.locale
            self.logger.info(f"Internal Viewer Display Language: {self.language} (Inherited from Caller)")
            return

        self.language = AdvancedStartup.specify_locale() or AppTranslator.detect_system_language()
        self.app_translator = AppTranslator(self.language)
        self.logger.info(f"Internal Viewer Display Language: {self.language}")

    def _set_window_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = 640
        height = 480

        # Cascade additional windows so they do not completely cover each other.
        x = (screen_width - width) // 2 + self._cascade_offset
        y = (screen_height - height) // 2 + self._cascade_offset

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.logger.info(
            f"Window Geometry Set to: {width} x {height} (x + {x}, y + {y}), Scaling Factor: {self._get_window_scaling()}")

    def _read_content(self):
        if not self.file_path or not self.file_path.exists():
            return None

        try:
            return self.file_path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            self.logger.error(f"Error Reading File {self.file_path}: {e}")
            return None

    def refresh_content(self):
        self.content_menu.refresh_content()

    def destroy(self):
        if InternalViewer._open_viewers.get(self._viewer_key) is self:
            InternalViewer._open_viewers.pop(self._viewer_key, None)
        super().destroy()
