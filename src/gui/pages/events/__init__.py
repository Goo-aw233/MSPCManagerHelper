"""
Events Package for MSPCManagerHelper GUI Pages
"""

from .get_localization_translators import get_localization_translators
from .on_about_windows_click import on_about_windows_click
from .on_enable_long_paths_click import EnableLongPathsHandler
from .on_get_help_button_click import on_get_help_button_click
from .on_privacy_settings_click import on_privacy_settings_click
from .on_restart_as_administrator import on_restart_as_administrator
from .on_restart_program_click import on_restart_program_click
from .on_start_mspcm_beta_click import on_start_mspcm_beta_click
from .on_start_mspcm_click import on_start_mspcm_click
from .on_theme_selected import on_theme_selected
from .on_toggle_cleanup_after_exit import on_toggle_cleanup_after_exit
from .on_toggle_compatibility_mode import on_toggle_compatibility_mode
from .on_toggle_support_developer import on_toggle_support_developer

__all__ = [
    "get_localization_translators",
    "on_about_windows_click",
    "EnableLongPathsHandler",
    "on_get_help_button_click",
    "on_privacy_settings_click",
    "on_restart_as_administrator",
    "on_restart_program_click",
    "on_start_mspcm_beta_click",
    "on_start_mspcm_click",
    "on_theme_selected",
    "on_toggle_cleanup_after_exit",
    "on_toggle_compatibility_mode",
    "on_toggle_support_developer"
]
