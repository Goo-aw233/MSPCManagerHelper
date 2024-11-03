import json
import os

class Translator:
    def __init__(self, locale):
        self.locale = locale
        self.load_translations()

    def load_translations(self, file_path=None):
        if file_path == None:
            base_path = os.path.dirname(__file__)
            file_path = os.path.join(base_path, 'locales', f'{self.locale}.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            self.translations = json.load(file)

    def translate(self, key):
        return self.translations.get(key, key)
