import importlib
from googletrans import Translator
from mtranslate import translate
from Cached import Cached
import translators as ts
import sys


class CachedTranslator(Cached):
    def __init__(self, file):
        Cached.__init__(self, file, cache_size=10000)
    def my_translate(self, text, dest='en', src='auto', alternative_translate=0):
        try:
            print("translate:", end=" ")
            key = str((text, dest, src, alternative_translate))
            res = self.get(key)
            if res != "":
                return res

            if alternative_translate == 0:
                print("translators: Bing")
                res = ts.translate_text(text, translator="Bing".lower(), to_language=dest)
            if alternative_translate == 1:
                translator = Translator()
                translation = translator.translate(text, dest)
                print("googletrans==3.1.0a0")
            if alternative_translate == 2:
                res = translate(text, dest)
                print("mtranslate (google)")
            if alternative_translate == 3:
                print("translators: Google")
                res = ts.translate_text(text, translator="Google".lower(), to_language=dest)
            if alternative_translate == 4:
                print("translators: Sogou")
                res = ts.translate_text(text, translator="Sogou".lower(), to_language=dest)
            if alternative_translate == 5:
                print("translators: Iciba")
                res = ts.translate_text(text, translator="Iciba".lower(), to_language=dest)
            if alternative_translate == 6:
                print("translators: Baidu")
                res = ts.translate_text(text, translator="Baidu".lower(), to_language=dest)
            if alternative_translate == 7:
                print("translators: Itranslate")
                res = ts.translate_text(text, translator="Itranslate".lower(), to_language=dest)

            self.set(key, res)

            return res
        except:
            print("Ошибка. Возврат оригинала")
            return text

    def close(self):
        self.save_cache_to_file()