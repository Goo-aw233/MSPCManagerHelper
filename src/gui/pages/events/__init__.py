"""
Page Button Events Package for MSPCManagerHelper GUI
"""

from .get_localization_translators import get_localization_translators
from .on_about_windows_button_click import OnAboutWindowsButtonClick
from .on_enable_long_paths_click import OnEnableLongPathsClick
from .on_privacy_settings_button_click import OnPrivacySettingsButtonClick
from .on_restart_as_administrator import OnRestartAsAdministrator
from .on_url_button_click import OnOpenURLButtonClick
from .start_mspcm import StartMSPCM
from .start_mspcm_beta import StartMSPCMBeta

__all__ = [
    "get_localization_translators",
    "OnAboutWindowsButtonClick",
    "OnEnableLongPathsClick",
    "OnPrivacySettingsButtonClick",
    "OnRestartAsAdministrator",
    "OnOpenURLButtonClick",
    "StartMSPCM",
    "StartMSPCMBeta",
]
