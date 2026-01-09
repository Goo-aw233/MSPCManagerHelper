"""
Page Button Events Package for MSPCManagerHelper GUI
"""

from .get_localization_translators import get_localization_translators
from .on_privacy_settings_button_click import OnPrivacySettingsButtonClick
from .on_url_button_click import OnOpenURLButtonClick

__all__ = [
    "get_localization_translators",
    "OnPrivacySettingsButtonClick",
    "OnOpenURLButtonClick",
]
