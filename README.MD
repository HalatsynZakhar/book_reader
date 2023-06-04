Reader for learning English (or any other language)

Input data: book.txt (book.fb2) or music title

Result: Displays text with parallel translation paragraph by paragraph on one page. Each sentence is highlighted and voiced as it is read.

Available options:

* The choice of any 2 languages is available as native and as studied from 36 available
* Play the current sentence at 2 different speeds
* dark theme and light theme (the ability to fully customize the interface)
* display current page and progress (optional)
* document navigation
* reading any .txt or .fb2 document on computer
* Save all settings and bookmark all documents ever opened
* Auto-tuning interface for the user's native language
* Translator data is cached to optimize translator usage
* Customized hotkeys on main keys for ease of use

To get the original lyrics, use the site: https://muztext.com/

Python was used as the programming language.

This code used the following libraries:
* threading - implemented translation of the interface and generation and playback of audio is implemented in parallel to avoid interface interruption
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

Create virt env
* Download and install Python https://www.python.org/downloads/ (my version 3.11.3 . When installing, check all the boxes that are offered)
* Open command prompt and install virtual environment (python -m venv name)
* Go to directory (cd name)
* environment activation (Scripts\activate.bat)
* install dependencies: pip install requests
* Download files *.py and add to directory name
* Install the necessary packages for work (pip install requests beautifulsoup4 nltk googletrans==3.1.0a0 gtts pygame PyQt5 lxml)
* Run the program: (python main.py)

For the next run:
* Go to directory (cd name)
* environment activation (Scripts\activate.bat)
* Run the program (python main.py)
