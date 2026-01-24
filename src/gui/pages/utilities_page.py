import threading
import tkinter

import customtkinter
from CTkToolTip import CTkToolTip

from core.app_logger import AppLogger
from modules.utilities import *


class UtilitiesPage(customtkinter.CTkFrame):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(parent, fg_color="transparent")
        self.logger = AppLogger.get_logger()
        self.log_file_path = AppLogger.get_log_file_path()
        self.app_translator = app_translator
        self.font_family = font_family

        # Main Layout configuration (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Page Title Label
        self.page_title_label = customtkinter.CTkLabel(
            self,
            text=self.app_translator.translate("utilities_page"),
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        self.page_title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Tab Switching
        self.tabview = customtkinter.CTkTabview(self, fg_color="transparent")
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.tabview.grid_columnconfigure(0, weight=1)
        self.tabview._segmented_button.configure(
            font=customtkinter.CTkFont(family=self.font_family, size=14, weight="bold"))

        self.features_tab_name = self.app_translator.translate("features_tab")
        self.events_tab_name = self.app_translator.translate("events_tab")

        self.tabview.add(self.features_tab_name)
        self.tabview.add(self.events_tab_name)
        self.tabview.set(self.features_tab_name)

        # Scrollable Content (Features Tab)
        self.scroll_frame = customtkinter.CTkScrollableFrame(self.tabview.tab(self.features_tab_name),
                                                             fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Events Textbox (Events Tab)
        self.events_textbox_description = customtkinter.CTkLabel(
            self.tabview.tab(self.events_tab_name),
            text=self.app_translator.translate("events_textbox_description"),
            font=customtkinter.CTkFont(family=self.font_family, size=13),
            anchor="center"
        )
        self.events_textbox_description.pack(fill="x", padx=12, pady=(10, 0))

        self.events_textbox = customtkinter.CTkTextbox(
            self.tabview.tab(self.events_tab_name),
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            state="disabled"
        )
        # Configure tab stops: "5c" means a tab stop at 5cm.
        self.events_textbox._textbox.configure(tabs=("5c",))
        self.events_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Right-Click Menu for Events Textbox
        self.right_click_menu = tkinter.Menu(self.events_textbox, tearoff=0)
        self.right_click_menu.add_command(label=self.app_translator.translate("copy_button"), command=self._copy_events)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label=self.app_translator.translate("clear_button"),
                                          command=self._clear_events)

        self.events_textbox.bind("<Button-3>", self._show_right_click_menu)

        # === File Management ===
        self._create_section_label(self.app_translator.translate("file_management"))

        file_management_frame = self._create_group_frame()

        # --- Compute Files Hashes ---
        self.compute_files_hashes_card = self._create_settings_card(
            file_management_frame,
            title=self.app_translator.translate("compute_files_hashes_title"),
            description=self.app_translator.translate("compute_files_hashes_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
            command=self._run_compute_hashes
        )
        self.compute_files_hashes_card.configure(state="disabled")

        self._create_separator(file_management_frame)

        # - Hash Algorithm Checkboxes -
        self.hash_checkboxes_frame = customtkinter.CTkFrame(file_management_frame, fg_color="transparent")
        self.hash_checkboxes_frame.pack(fill="x", padx=10, pady=5)

        self.select_all_checkbox = customtkinter.CTkCheckBox(
            self.hash_checkboxes_frame,
            text=self.app_translator.translate("select_all"),
            command=self._toggle_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.select_all_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.hash_algos = {
            "md5": "MD5",
            "sha1": "SHA1",
            "sha224": "SHA224",
            "sha256": "SHA256",
            "sha384": "SHA384",
            "sha512": "SHA512",
            "sha3_224": "SHA3_224",
            "sha3_256": "SHA3_256",
            "sha3_384": "SHA3_384",
            "sha3_512": "SHA3_512",
            "shake_128": "Shake128",
            "shake_256": "Shake256",
            "blake2b": "Blake2b",
            "blake2s": "Blake2s"
        }
        self.hash_algo_tooltips = {
            "shake_128": "shake_128_tooltip",
            "shake_256": "shake_256_tooltip",
            "blake2b": "blake2b_tooltip",
            "blake2s": "blake2s_tooltip"
        }
        self.hash_checkbox_widgets = {}

        for i, (algo_key, algo_name) in enumerate(self.hash_algos.items()):
            cb = customtkinter.CTkCheckBox(
                self.hash_checkboxes_frame,
                text=algo_name,
                command=self._on_hash_checkbox_change,
                font=customtkinter.CTkFont(family=self.font_family)
            )
            cb.grid(row=(i // 4) + 1, column=i % 4, sticky="w", padx=10, pady=5)
            self.hash_checkbox_widgets[algo_key] = cb

            if algo_key in self.hash_algo_tooltips:
                CTkToolTip(cb, message=self.app_translator.translate(self.hash_algo_tooltips[algo_key]),
                           font=(self.font_family, 12))
        # === End of File Management ===


    # ~~~ Features Functions ~~~
    # ~ Compute Files Hashes ~
    def _update_select_all_state(self):
        if all(cb.get() == 1 for cb in self.hash_checkbox_widgets.values()):
            self.select_all_checkbox.select()
        else:
            self.select_all_checkbox.deselect()
        self._update_compute_button_state()

    def _on_hash_checkbox_change(self):
        self._update_select_all_state()

    def _update_compute_button_state(self):
        if any(cb.get() == 1 for cb in self.hash_checkbox_widgets.values()):
            self.compute_files_hashes_card.configure(state="normal")
        else:
            self.compute_files_hashes_card.configure(state="disabled")

    def _toggle_select_all(self):
        state = self.select_all_checkbox.get()
        for cb in self.hash_checkbox_widgets.values():
            if state:
                cb.select()
            else:
                cb.deselect()
        self._update_compute_button_state()

    def _run_compute_hashes(self):
        self.compute_files_hashes_card.configure(state="disabled")
        self.update_idletasks()

        hasher = ComputeFilesHashes(
            logger=self.logger,
            app_translator=self.app_translator,
            log_file_path=self.log_file_path,
            log_callback=self._log_to_events,
            selected_algos=[k for k, v in self.hash_checkbox_widgets.items() if v.get() == 1]
        )

        files = hasher.select_files()
        if not files:
            self._log_to_events(self.app_translator.translate("user_has_canceled_the_operation"))
            self._update_compute_button_state()
            return

        self._run_operation(
            lambda: hasher.compute(files),
            "compute_files_hashes_title",
            on_completion=self._update_compute_button_state
        )
    # ~ End of Compute File Hashes ~

    # ~~~ GUI/Events Functions ~~~
    def _run_operation(self, operation_func, operation_name_key, on_completion=None):
        self.tabview.set(self.events_tab_name)
        operation_name = self.app_translator.translate(operation_name_key)
        message = (
            f"{self.app_translator.translate('executing_operation_with_name').format(operation_name=operation_name)}\n"
            f"{self.app_translator.translate('please_wait_for_completion')}\n"
        )
        self.logger.info(f"Executing Operation: {operation_name}")

        # Reset Events Textbox on Main Thread
        self.events_textbox.configure(state="normal")
        self.events_textbox.delete("1.0", "end")
        self.events_textbox.insert("end", message + "\n")
        self.events_textbox.see("end")
        self.events_textbox.configure(state="disabled")

        def _thread_target():
            try:
                operation_func()
                self._log_to_events(self.app_translator.translate("operation_completed").format(operation_name=operation_name))
                self.logger.info(f"Completed Operation: {operation_name}")
            except Exception as e:
                self.logger.error(f"Error Executing {operation_name}: {e}")
                self._log_to_events(f"Error: {e}")
            finally:
                if on_completion:
                    self.after(0, on_completion)

        threading.Thread(target=_thread_target, daemon=True).start()

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

    def _copy_events(self):
        try:
            selected_text = self.events_textbox.get("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except tkinter.TclError:
            # Copy All Text If No Selection
            all_text = self.events_textbox.get("1.0", "end-1c")
            if all_text:
                self.clipboard_clear()
                self.clipboard_append(all_text)

    def _clear_events(self):
        self.events_textbox.configure(state="normal")
        self.events_textbox.delete("1.0", "end")
        self.events_textbox.configure(state="disabled")

    def _log_to_events(self, message):
        self.after(0, self._append_to_events_textbox, message)

    def _append_to_events_textbox(self, message):
        self.events_textbox.configure(state="normal")
        self.events_textbox.insert("end", message + "\n")
        self.events_textbox.see("end")
        self.events_textbox.configure(state="disabled")

    def _create_section_label(self, text):
        label = customtkinter.CTkLabel(
            self.scroll_frame,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", padx=25, pady=(20, 10))

    def _create_group_frame(self):
        frame = customtkinter.CTkFrame(
            self.scroll_frame,
            fg_color=("gray95", "#202020"),
            corner_radius=4,
            border_width=1,
            border_color=("gray90", "#2b2b2b")
        )
        frame.pack(fill="x", padx=20, pady=0)
        return frame

    @staticmethod
    def _create_separator(parent):
        separator = customtkinter.CTkFrame(parent, height=2, fg_color=("gray90", "#2b2b2b"))
        separator.pack(fill="x", padx=10)
        return separator

    def _create_settings_card(self, parent, title, description, widget_constructor=None, **widget_kwargs):
        container = customtkinter.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=8)

        # Text Column
        text_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)

        title_label = customtkinter.CTkLabel(
            text_frame,
            text=title,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        )
        title_label.pack(fill="x")

        if description:
            desc_label = customtkinter.CTkLabel(
                text_frame,
                text=description,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color=("gray50", "gray70"),
                anchor="w"
            )
            desc_label.pack(fill="x")

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None
