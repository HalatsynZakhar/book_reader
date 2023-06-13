from PyQt5.QtCore import QXmlStreamReader, QXmlStreamWriter, QFile, QIODevice
from googletrans import Translator
import xml.etree.ElementTree as ET

from Cached import Cached


class CachedTranslator(Translator):
    def __init__(self, file, cache_size=10000):
        super().__init__()

        self.cache_transl = Cached(file, cache_size=10000)
    def translate(self, text, dest='en', src='auto'):
        try:
            print("translate:", end=" ")

            key = str((text, dest, src))

            res = self.cache_transl.get(key)
            if res != "":
                return res
            result = super().translate(text, dest=dest, src=src)
            self.cache_transl.set(key, result.text)
            print("google")
            return result.text
        except:
            return text

    def close(self):
        self.cache_transl.save_cache_to_file()