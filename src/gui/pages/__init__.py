"""
Pages Package for MSPCManagerHelper GUI
"""

from .about_page import AboutPage
from .base_page_frame import BaseFuncPageFrame, BaseInfoPageFrame
from .home_page import HomePage
from .installer_page import InstallerPage
from .maintenance_page import MaintenancePage
from .settings_page import SettingsPage
from .toolbox_page import ToolboxPage
from .uninstaller_page import UninstallerPage
from .utilities_page import UtilitiesPage

__all__ = [
    "AboutPage",
    "BaseFuncPageFrame",
    "BaseInfoPageFrame",
    "HomePage",
    "InstallerPage",
    "MaintenancePage",
    "SettingsPage",
    "ToolboxPage",
    "UninstallerPage",
    "UtilitiesPage",
]
