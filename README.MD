Reader for learning English (or any other language)

Input data: book.txt (book.fb2) or Music title

Displays text with parallel translation paragraph by paragraph on one page. Each sentence is highlighted while reading for easier reading.

Settings:

* voice suggestions at 2 different speeds
* dark theme and light theme
* display current page and progress (optional)
* document navigation
* choosing any .txt on the computer
* This reader saves progress and all settings on restart:

current book
current offer
current page
voice settings
window position and size
interface color

To get the original lyrics of the song, use the site https://muztext.com/

Python was used as the programming language.

This code used the following libraries:

* bs4 - parsing the page to get lyrics
* codecs - to read txt files
* googletrans - to translate text into another language via Google Translate.
* gtts - for text-to-speech synthesis.
* html - to convert HTML code to text.
* lxml - to read fb2 files
* nltk - Natural Language Toolkit (natural language processing toolkit), i.e. library for text analysis in natural language.
* os - getting the absolute path of a file
* pygame - for playing sound files and music.
* PyQt5 - for creating a GUI application.
* sys is for accessing system functions and variables.

How to use?
