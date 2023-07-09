import nltk
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')
class Nltk_decorator:
    def sent_tokenize(self, currentParagraph, language):
        try:
            list_sentences = nltk.sent_tokenize(currentParagraph, language=language)
        except:
            try:
                print('Language not supported')
                list_sentences = nltk.sent_tokenize(currentParagraph)
            except:
                print("Вовзрат оригинального текста, не удалось разбить на предложения")
                return currentParagraph
        return list_sentences