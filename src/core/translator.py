import json
from pathlib import Path


class Translator:
    def __init__(self, locale):
        self.locale = locale
        self.translations = self.load_translations()

    def load_translations(self):
        file_path = (Path(__file__).resolve().parents[1] / "assets" / "locales" / f"{self.locale}.json")
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def translate(self, key):
        return self.translations.get(key, key)
