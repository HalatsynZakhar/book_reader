**Reader for learning a foreign language (from the current one)

*Input data: book.txt (book.fb2) or the name of a piece of music.
*Result: Displays text with parallel translation point by point on one page. Each sentence is highlighted and spoken out as you read.

**Programming language: Python, main GUI library: PyQt5

The program has additional options:
*You can choose any 2 languages, both native and studied, out of 36 available.
*Voiceover of text (Google Translator voice) at selected speed.
*Dark theme and light theme (the ability to fully customize the interface, text sizes, fonts, sentence highlight colors, etc.).
*Displays the current page and progress (can be partially or completely hidden).
*History and history editing of current books and songs is available.
*Navigate the document using the mouse, keyboard, and navigation bar.
*Read any .txt or .fb2 document on your computer.
*Ability to select up to 10 translators with an indication of priority to achieve a more accurate comparison of sentences in the original and target language.
*Full saving of user actions when restarting the application. Saving position in the text, interface settings, translator settings, etc. The settings are saved in any case, even if the application is unexpectedly closed and reinstalled.
*Auto-tuning of the interface to the user’s native language.
*Data received from third-party servers (translation of text, songs) is cached to minimize repeated requests, the cache is preserved across reboots.
*Data for displaying pages is generated in parallel threads 10 pages ahead and temporarily cached to achieve smooth operation of the interface.
*Customizable hotkeys for basic actions for ease of use.
*Continuous playback
*To obtain the lyrics, the following websites are used: https://muztext.com/, https://ru.musinfo.net/. If this material is not there, it is recommended to save the necessary text with separate paragraphs in .fb2 or .txt format.

**This code used the following libraries:

*threading - used to avoid stopping the GUI. To make the interface responsive, the translation is performed 10 pages in advance. Also, text voicing is performed in a parallel process with the possibility of interruption.
*bs4 - page analysis to get song lyrics
*codecs - for reading text files
*googletrans, mtranslate, translators - to translate text into another language using different translators.
*gtts - for speech synthesis.
*html - to convert HTML code into text.
*lxml, chardet - for reading fb2 files
*nltk - Natural Language Toolkit (a set of natural language processing tools), i.e. library for natural language text analysis.
*os - get the absolute path to the file
*vlc, pygame - for playing sound files and music.
*PyQt5 - for creating a GUI application.
*sys - is intended for access to system functions and variables.
*inspect - debugging
*requests - get song lyrics
*xml.etree.ElementTree - for working with XML files. Save cache to minimize internet requests
*functools – the lru_cache decorator is used to optimize program performance
*itertools, re, unidecode – used for text processing.
*chardet – read files
*langcodes – for robots with a translator

**Attention:
*Testing of the program was carried out mainly while learning English. I may not take into account some features of the encoding of foreign languages, features of sentence analysis. Some translators may not work with rarer languages.
*Also, when unpacking the book, only text was taken into account; images and other non-text data will not be displayed. The preferred format is .txt (the main testing format).
*The song search function involves searching for English-language songs. If you are looking for songs in another language, you should use transliteration.

**How to use?
*Create a virtual environment
*Download and install Python https://www.python.org/downloads/ (my version is 3.11.3. When installing, check all the suggested boxes)
*Clone the project by downloading the archive, or use the command line: git clone --length 1 https://github.com/HalatsynZakhar/book_reader
*Run install-package.py or use the command: pip install language_data, langcodes, qtpy, pygame, requests, beautifulsoup4, nltk, mtranslate, googletrans==4.0.0-rc1, translators, gtts, python-vlc, PyQt5, lxml, chardet , unidecode
*Run main.py from the current directory or use the command: 
cd.../book_reader
python main.py