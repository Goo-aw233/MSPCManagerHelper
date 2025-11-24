from tkinter import ttk

from gui.pages.about_page import AboutPage
from gui.pages.home_page import HomePage
from gui.pages.installer_page import InstallerPage
from gui.pages.maintenance_page import MaintenancePage
from gui.pages.toolbox_page import ToolboxPage
from gui.pages.uninstaller_page import UninstallerPage
from gui.pages.utilities_page import UtilitiesPage


class Navigation(ttk.Frame):
    def __init__(self, parent, translator, font_family):
        super().__init__(parent, style="Card.TFrame", padding=10)
        self.translator = translator
        self.font_family = font_family

        # Configure Font Style
        """
        Use `#.TButton` instead of using `TButton` directly.
        E.g.: `Nav.TButton`, `Nav.Accent.TButton`, etc.
        """
        style = ttk.Style()
        style.configure("Nav.Accent.TButton", font=(self.font_family, 12))
        style.configure("Nav.TButton", font=(self.font_family, 12))
        style.configure("Title.TLabel", font=(self.font_family, 12, "bold"))

        self.pages = {}
        self.buttons = {}
        self.current_page = None

        title_label = ttk.Label(
            self,
            text=self.translator.translate("mspcmanagerhelper"),
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        self.grid_rowconfigure(8, weight=1)

        self.create_buttons()
        self.create_pages(parent)

        self.show_page("home_page")

    def create_buttons(self):
        # Translation Keys
        page_names = ["home_page", "maintenance_page", "installer_page", "uninstaller_page", "utilities_page", "toolbox_page", "about_page"]
        for i, page_name in enumerate(page_names):
            button = ttk.Button(
                self,
                text=self.translator.translate(page_name),
                command=lambda n=page_name: self.show_page(n),
                width=-12,
                style="Nav.TButton"
            )
            # Start buttons from row 1 to make space for the title.
            button.grid(row=i + 1, column=0, sticky="ew", padx=8, pady=4)
            self.buttons[page_name] = button

    def create_pages(self, parent):
        self.page_classes = {
            "home_page": HomePage,
            "maintenance_page": MaintenancePage,
            "installer_page": InstallerPage,
            "uninstaller_page": UninstallerPage,
            "utilities_page": UtilitiesPage,
            "toolbox_page": ToolboxPage,
            "about_page": AboutPage
        }
        for page_name, page_class in self.page_classes.items():
            page = page_class(parent, self.translator, self.font_family)
            self.pages[page_name] = page
            page.grid(row=0, column=1, sticky="nsew")
            page.grid_remove()  # Initially hide the page.

    def show_page(self, page_name):
        # Deselect the button for the current page.
        if self.current_page:
            self.current_page.grid_remove()
            for p_name, page_obj in self.pages.items():
                if page_obj == self.current_page:
                    button = self.buttons.get(p_name)
                    if button:
                        button.state(["!focus"])
                        button.config(style="Nav.TButton")
                    break

        page = self.pages.get(page_name)
        if page:
            page.grid()
            self.current_page = page
            # Select the button for the new page.
            button = self.buttons.get(page_name)
            if button:
                button.focus_set()
                button.config(style="Nav.Accent.TButton")
