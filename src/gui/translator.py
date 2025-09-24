import json
import os


class Translator:
    def __init__(self, locale):
        self.locale = locale
        self.translations = self.load_translations()

    def load_translations(self):
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                 'assets', 'locales', f'{self.locale}.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def translate(self, key):
        return self.translations.get(key, key)
