import json
import locale
from pathlib import Path


class AppTranslator:
    def __init__(self, locale):
        self.locale = locale
        self.translations = self.load_translations()

    def load_translations(self):
        file_path = (Path(__file__).resolve().parents[1] / "assets" / "locales" / f"{self.locale}.json")
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def translate(self, key):
        return self.translations.get(key, key)

    @staticmethod
    def detect_system_language():
        language_map = {
            # English
            ("en_", "en-",): "en-us",
            # Simplified Chinese
            ("zh_CN", "zh_Hans", "zh_Hans_", "zh_Hans_CN", "zh_Hans_HK", "zh_Hans_MO", "zh_Hans_SG", "zh_SG", "zh-CN",
             "zh-Hans", "zh-Hans-", "zh-Hans-CN", "zh-Hans-HK", "zh-Hans-MO", "zh-Hans-SG", "zh-SG",): "zh-cn",
            # Traditional Chinese
            ("zh_Hant", "zh_Hant_", "zh_Hant_HK", "zh_Hant_MO", "zh_Hant_TW", "zh_HK", "zh_MO", "zh_TW", "zh-Hant",
             "zh-Hant-", "zh-Hant-HK", "zh-Hant-MO", "zh-Hant-TW", "zh-HK", "zh-MO", "zh_TW",): "zh-tw"
        }
        try:
            locale_str = locale.getdefaultlocale()[0]
        except Exception:
            locale_str = None

        if not locale_str:
            return "en-us"

        for prefixes, trans_locale in language_map.items():
            if any(locale_str.startswith(prefix) for prefix in prefixes):
                return trans_locale
        return "en-us"
