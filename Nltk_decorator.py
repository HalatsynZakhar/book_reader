import nltk
class Nltk_decorator:
    def sent_tokenize(self, currentParagraph, language):
        try:
            list_sentences = nltk.sent_tokenize(currentParagraph, language=language)
        except:
            print('Language not supported')
            list_sentences = nltk.sent_tokenize(currentParagraph)
        return list_sentences