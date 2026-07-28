import tkinter
import tkinter.filedialog

import customtkinter
from CTkToolTip import CTkToolTip

from gui.components import (
    BaseWidgets,
)
from modules.maintenance import (
    CollectMSPCMLogs,
)
from .base_page_frame import BaseFuncPageFrame


class MaintenancePage(BaseFuncPageFrame, BaseWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="pages.navigation.maintenance",
            events_textbox_wrap="none"
        )

        # === Log Collection Section ===
        self._create_section_label(self.app_translator.translate("pages.maintenance.log_collection"))

        # --- Collect MSPCM Logs
        collect_mspcm_logs_frame = self._create_group_frame()
        collect_mspcm_logs_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.collect_mspcm_logs_card = self._create_actions_card(
            parent=collect_mspcm_logs_frame,
            title=self.app_translator.translate("pages.maintenance.collect_mspcm_logs"),
            description=self.app_translator.translate("pages.maintenance.collect_mspcm_logs_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_collect_mspcm_logs,
            state="disabled"
        )

        self._create_separator(collect_mspcm_logs_frame)

        # - Collect MSPCM Logs Options -
        self.collect_mspcm_logs_options_frame = customtkinter.CTkScrollableFrame(
            collect_mspcm_logs_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=42
        )
        self.collect_mspcm_logs_options_frame.pack(fill="x", padx=10, pady=5)

        self.procdump_from_var = tkinter.StringVar(value="online_download")

        # ProcDump from Radio Buttons (in a sub-frame)
        self.procdump_source_frame = customtkinter.CTkFrame(
            self.collect_mspcm_logs_options_frame,
            fg_color="transparent"
        )
        self.procdump_source_frame.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=5)

        # Online Download
        self.procdump_online_radiobutton = customtkinter.CTkRadioButton(
            self.procdump_source_frame,
            text=self.app_translator.translate("pages.maintenance.online_download"),
            variable=self.procdump_from_var,
            value="online_download",
            command=self._toggle_local_procdump_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.procdump_online_radiobutton.pack(side="left", padx=(0, 5))
        CTkToolTip(self.procdump_online_radiobutton,
                   self.app_translator.translate("pages.maintenance.online_download_procdump_tooltip"),
                   font=(self.font_family, 12))

        # Local
        self.procdump_local_radiobutton = customtkinter.CTkRadioButton(
            self.procdump_source_frame,
            text=self.app_translator.translate("pages.maintenance.local_file"),
            variable=self.procdump_from_var,
            value="local_file",
            command=self._toggle_local_procdump_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.procdump_local_radiobutton.pack(side="left")
        
        # Local ProcDump Path Entry
        self.local_procdump_path_entry = customtkinter.CTkEntry(
            self.collect_mspcm_logs_options_frame,
            placeholder_text=self.app_translator.translate("pages.maintenance.local_file_placeholder"),
            font=customtkinter.CTkFont(family=self.font_family),
            width=650
        )
        self.local_procdump_path_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=5, columnspan=2)
        self.local_procdump_path_entry.bind("<KeyRelease>", lambda _: self._update_collect_mspcm_logs_state())

        # Local ProcDump Path Select Button
        self.local_procdump_path_select_button = customtkinter.CTkButton(
            self.collect_mspcm_logs_options_frame,
            text=self.app_translator.translate("pages.common.browse"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._select_local_procdump_path
        )
        self.local_procdump_path_select_button.grid(row=0, column=3, sticky="w", padx=(0, 10), pady=5)

        # Apply Initial Toggle States
        self._toggle_local_procdump_state()
        self._update_collect_mspcm_logs_state()


    # ~~~ Features Functions ~~~
    # ~ Collect MSPCM Logs ~
    def _set_entry_group_state(self, enabled, entry, button=None):
        if button is not None:
            button.configure(state="normal" if enabled else "disabled")
        if enabled:
            entry.configure(state="normal")
            entry.unbind("<Button-1>")
        else:
            entry.configure(state="normal")
            entry.bind("<Button-1>", self._block_entry_event, add="+")

    @staticmethod
    def _set_entry_text(entry, text):
        entry.delete(0, tkinter.END)
        entry.insert(0, text)

    @staticmethod
    def _block_entry_event(_):
        return "break"

    def _toggle_local_procdump_state(self):
        enabled = self.procdump_from_var.get() == "local_file"
        self._set_entry_group_state(enabled, self.local_procdump_path_entry,
                                     self.local_procdump_path_select_button)
        self._update_collect_mspcm_logs_state()

    def _select_local_procdump_path(self):
        file_path = tkinter.filedialog.askopenfilename(
            title=self.app_translator.translate("pages.maintenance.collect_mspcm_logs"),
            filetypes=[("ProcDump", "*.exe")]
        )
        if file_path:
            self._set_entry_text(self.local_procdump_path_entry, file_path)
        self._update_collect_mspcm_logs_state()

    def _update_collect_mspcm_logs_state(self):
        if self.procdump_from_var.get() == "local_file" and not self.local_procdump_path_entry.get().strip():
            self.collect_mspcm_logs_card.configure(state="disabled")
            return
        self.collect_mspcm_logs_card.configure(state="normal")

    def _run_collect_mspcm_logs(self):
        self.collect_mspcm_logs_card.configure(state="disabled")
        self.update_idletasks()

        worker = CollectMSPCMLogs(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            procdump_source=self.procdump_from_var.get(),
            local_procdump_path=self.local_procdump_path_entry.get(),
        )

        self._run_operation(
            worker.execute,
            "pages.maintenance.collect_mspcm_logs",
            on_completion=lambda: self._update_collect_mspcm_logs_state()
        )
    # ~ End of Collect MSPCM Logs ~
