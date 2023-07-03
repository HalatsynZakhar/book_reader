from PyQt5.QtCore import QXmlStreamReader, QXmlStreamWriter, QFile, QIODevice
from googletrans import Translator
import xml.etree.ElementTree as ET

from Cached import Cached


class CachedTranslator(Translator, Cached):
    def __init__(self, file):
        super().__init__()
        Cached.__init__(self, file, cache_size=10000)

    def my_translate(self, text, dest='en', src='auto'):
        try:
            print("translate:", end=" ")
            key = str((text, dest, src))
            res = self.get(key)
            if res != "":
                return res
            escaped_text = text.replace("\"", "\\\"")
            result = super().translate(escaped_text, dest=dest, src=src)
            unescaped_text = result.text.replace("\\\"", "\"")
            self.set(key, unescaped_text)
            print("google")
            return unescaped_text
        except:
            return text

    def close(self):
        self.save_cache_to_file()