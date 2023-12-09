import importlib
from googletrans import Translator
from mtranslate import translate
from Cached import Cached
import sys
try:
    import translators as ts
except:
    print("Unable to connect the Internet")

class CachedTranslator(Cached):
    def __init__(self, file):
        Cached.__init__(self, file, cache_size=10000)
        self.translators = ["translators.Bing", "googletrans.googletrans==3.1.0a0", "mtranslate.google", "translators"
                                                                                                         ".Google",
                            "translators.Sogou", "translators.Iciba", "translators.Baidu", "translators.Itranslate",
                            "translators.Deepl",
                            "translators.Yandex"]
    def my_translate(self, text, dest='en', src='auto', alternative_translate=0, no_return=False, cache=True):
        try:
            library, trans = self.translators[alternative_translate].split(".", 1)
            key = str((text, dest, src, alternative_translate))
            if cache:
                res = self.get(key)
                if res != "":
                    print("Библиотека: {}, переводчик: {}, кеш: {}".format(library, trans, "да"))
                    return res

            if library=="translators":
                res = ts.translate_text(text, translator=trans.lower(), to_language=dest)
            if library=="googletrans":
                translator = Translator()
                res = translator.translate(text, dest)
                res = res.text
            if library=="mtranslate":
                res = translate(text, dest)

            self.set(key, res)

            print("Библиотека: {}, переводчик: {}, кеш: {}".format(library, trans, "нет"))
            if res:
                return res
        except:
            print("Ошибка у переводчика.")
            if no_return:
                return ""
            else:
                return text

    def close(self):
        self.save_cache_to_file()