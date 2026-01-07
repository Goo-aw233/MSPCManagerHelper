import customtkinter


class UtilitiesPage(customtkinter.CTkFrame):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(parent, fg_color="transparent")
        self.app_translator = app_translator
        self.font_family = font_family

        # Page Title Label
        page_title_label = customtkinter.CTkLabel(
            self,
            text=self.app_translator.translate("utilities_page"),
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        page_title_label.pack(padx=20, pady=20, anchor="w")
