from PyQt5.QtCore import QSettings
from googletrans import Translator


class CachedTranslator(Translator):
    def __init__(self, cache_size=10000):
        super().__init__()
        self.cache_size = cache_size
        self.cache = {}

    def translate(self, text, dest='en', src='auto'):
        try:
            print("translate:", end=" ")
            key = (text, dest, src)
            if key in self.cache:
                print("cache")
                return self.cache[key]
            result = super().translate(text, dest=dest, src=src)
            if len(self.cache) >= self.cache_size:
                self.cache.popitem()
            self.cache[key] = result.text
            print("google")
            return result.text
        except:
            return text
    def load_cache_from_settings(self, MyWindow):
        self.cache = MyWindow.settings.value("cache", {})

    def save_cache_to_settings(self, MyWindow):
        MyWindow.settings.setValue("cache", self.cache)