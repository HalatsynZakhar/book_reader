import re

from PyQt5.QtCore import QXmlStreamReader, QXmlStreamWriter, QFile, QIODevice
from mtranslate import translate
from translate import Translator
import xml.etree.ElementTree as ET

from unidecode import unidecode

from Cached import Cached


class CachedTranslator(Cached):
    def __init__(self, file):
        Cached.__init__(self, file, cache_size=10000)

    def my_translate(self, text, dest='en', src='auto', alternative_translate=False):
        try:
            print("translate:", end=" ")
            key = str((text, dest, src, alternative_translate))
            res = self.get(key)
            if res != "":
                return res

            if alternative_translate:
                translator = Translator(to_lang=dest)
                res = translator.translate(text)
                print("microsoft")
            else:
                res = translate(text, dest)
                print("google")

            self.set(key, res)

            return res
        except:
            print("Ошибка. Возврат оригинала")
            return text

    def close(self):
        self.save_cache_to_file()