from gui.components import (
    BaseWidgets,
)
from .base_page_frame import BaseFuncPageFrame


class MaintenancePage(BaseFuncPageFrame, BaseWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="maintenance_page"
        )
