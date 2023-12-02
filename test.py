from CachedTranslator import CachedTranslator

test_text = "Hello world"
original_lang = "en"
translate_lang = "ru"



translator = CachedTranslator("test.xml")
for n in range(10):
    print(translator.my_translate(test_text, translate_lang, original_lang, n, cache=False))
translator.close()
