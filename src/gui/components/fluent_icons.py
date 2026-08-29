"""Centralized FluentSystemIcons glyph definitions.

Every Fluent icon glyph used by the UI is defined here in a single place. The
decimal codepoints are taken from FluentSystemIcons-Regular.json; the bundled
FluentSystemIcons-Regular.ttf maps these codepoints to icon glyphs.

To add a new icon, look up ``ic_fluent_<name>_24_regular`` in
FluentSystemIcons-Regular.json, take its decimal codepoint and add an entry:
``"<semantic name>": chr(<codepoint>),``

More character mappings for FluentSystemIcons-Regular.ttf
Ref: https://github.com/microsoft/fluentui-system-icons/blob/main/fonts/FluentSystemIcons-Regular.json
"""

from typing import Final

FLUENT_ICONS: Final = {
    # ===== Common =====
    "refresh": chr(61758),       # ic_fluent_arrow_clockwise_24_regular

    # ===== Navigation =====
    "about": chr(62628),         # ic_fluent_info_24_regular
    "home": chr(62593),          # ic_fluent_home_24_regular
    "installer": chr(61777),     # ic_fluent_arrow_download_24_regular
    "maintenance": chr(61954),   # ic_fluent_broom_24_regular
    "settings": chr(63146),      # ic_fluent_settings_24_regular
    "toolbox": chr(63535),       # ic_fluent_toolbox_24_regular
    "uninstaller": chr(62285),   # ic_fluent_delete_24_regular
    "utilities": chr(63681),     # ic_fluent_wrench_24_regular
}
