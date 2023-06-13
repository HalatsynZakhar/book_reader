from PyQt5.QtCore import QXmlStreamReader, QXmlStreamWriter, QFile, QIODevice
from googletrans import Translator
import xml.etree.ElementTree as ET

from Cached import Cached


class CachedTranslator(Translator, Cached):
    def __init__(self, file):
        super().__init__()
        Cached.__init__(self, file, cache_size=10000)

    def translate(self, text, dest='en', src='auto'):
        try:
            print("translate:", end=" ")

            key = str((text, dest, src))

            res = self.get(key)
            if res != "":
                return res
            result = super().translate(text, dest=dest, src=src)
            self.set(key, result.text)
            print("google")
            return result.text
        except:
            return text

    def close(self):
        self.save_cache_to_file()