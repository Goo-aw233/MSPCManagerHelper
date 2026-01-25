import os
import tkinter

import customtkinter

from core.app_logger import AppLogger
from core.app_metadata import AppMetadata
from core.app_resources import AppResources
from core.app_settings import AppSettings
from core.app_translator import AppTranslator
from core.set_font_family import SetFontFamily


class InternalViewer(customtkinter.CTkToplevel):
    def __init__(self, file_path=None, app_translator=None):
        super().__init__()

        self.file_path = file_path
        self.app_translator = app_translator
        self.logger = AppLogger.get_logger()

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
            font=(self.font_family, 13),
            wrap="none"
        )
        self.content_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        if self.file_path and os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                self.content_textbox.insert("0.0", content)
            except Exception as e:
                self.content_textbox.insert("0.0", f"Error Reading File: {e}")
                self.logger.error(f"Error Reading File {self.file_path}: {e}")
        else:
            self.content_textbox.insert("0.0", "")

        self.content_textbox.configure(state="disabled")

        # Right-Click Menu
        self.right_click_menu = tkinter.Menu(self, tearoff=0)
        self.right_click_menu.add_command(label=self.app_translator.translate("copy_button"),
                                          command=self._copy_content)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label=self.app_translator.translate("refresh_button"),
                                          command=self._refresh_content)

        self.content_textbox.bind("<Button-3>", self._show_right_click_menu)

    def _configure_window(self):
        if self.file_path:
            app_title = f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION} - {os.path.basename(self.file_path)}"
        else:
            app_title = f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION} Internal Viewer"
        self.title(app_title)

        icon_path = AppResources.app_icon()
        if icon_path:
            self.after(200, lambda: self.iconbitmap(icon_path))
            self.logger.info(f"Window Icon: {icon_path}")

        self._set_window_geometry()

        # Ensure Window is On Top & Focused
        self.after(250, lambda: (self.lift(), self.focus_force()))

    def _set_language(self):
        self.language = AppTranslator.detect_system_language()
        self.app_translator = AppTranslator(self.language)
        self.logger.info(f"Internal Viewer Display Language: {self.language}")

    def _set_window_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = 640
        height = 480

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.logger.info(
            f"Window Geometry Set: {width} x {height} (x + {x}, y + {y}), Scaling Factor: {self._get_window_scaling()}")

    def _show_right_click_menu(self, event):
        bg = self._apply_appearance_mode(["#e3e3e3", "#333333"])
        fg = self._apply_appearance_mode(["#191919", "#e2e2e2"])
        active_bg = self._apply_appearance_mode(["#bebebe", "#464646"])
        active_fg = self._apply_appearance_mode(["#191919", "#e2e2e2"])

        self.right_click_menu.configure(
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=active_fg,
            font=(self.font_family, 10)
        )
        self.right_click_menu.tk_popup(event.x_root, event.y_root)

    def _copy_content(self):
        try:
            selected_text = self.content_textbox.get("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except tkinter.TclError:
            # Copy All Text If No Selection
            all_text = self.content_textbox.get("1.0", "end-1c")
            if all_text:
                self.clipboard_clear()
                self.clipboard_append(all_text)

    def _refresh_content(self):
        if self.file_path and os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()

                self.content_textbox.configure(state="normal")
                self.content_textbox.delete("0.0", "end")
                self.content_textbox.insert("0.0", content)
                self.content_textbox.configure(state="disabled")
            except Exception as e:
                self.logger.error(f"Error Refreshing File {self.file_path}: {e}")
