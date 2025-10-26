import json
from pathlib import Path


class Translator:
    def __init__(self, locale=None, file_path=None):
        self.locale = locale
        self.load_translations(file_path)

    def load_translations(self, file_path=None):
        if file_path is None:
            base_path = Path(__file__).parent
            file_path = base_path / 'locales' / f'{self.locale}.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            self.translations = json.load(file)
        self.locale = str(file_path)
        self.current_language = self.translate(self.translate("current_language"))

    def translate(self, key):
        return self.translations.get(key, key)
