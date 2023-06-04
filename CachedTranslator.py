from PyQt5.QtCore import QSettings
from googletrans import Translator


class CachedTranslator(Translator):
    def __init__(self, cache_size=10000):
        super().__init__()
        self.cache_size = cache_size
        self.cache = {}
        self.settings = QSettings("halatsyn_zakhar", "book_reader")

    def translate(self, text, dest='en', src='auto'):
        key = (text, dest, src)
        if key in self.cache:
            return self.cache[key]
        result = super().translate(text, dest=dest, src=src)
        if len(self.cache) >= self.cache_size:
            self.cache.popitem()
        self.cache[key] = result.text
        self.settings.setValue("cache", self.cache)
        return result.text

    def load_cache_from_settings(self):
        self.cache = self.settings.value("cache", {})

    def save_cache_to_settings(self):
        self.settings.setValue("cache", self.cache)