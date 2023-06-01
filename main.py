import html
import os
import sys

import requests
from bs4 import BeautifulSoup

import nltk
from googletrans import Translator
from gtts import gTTS
import pygame

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QSettings, QEvent
from PyQt5.QtGui import QPalette, QColor, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLabel, \
    QSpinBox, QLineEdit, QCheckBox, QFileDialog


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.download_settings()

        self.create_GUI()

        # чтение файла (указан путь к примеру файлу txt) и генерация страницы далее
        if self.active_mode == "book":
            self.read_txt()
        elif self.active_mode == "song":
            self.read_song()

        # устанавливаем ночную тему,если это соотвтетсвует настройке
        if self.night_toggle == "fusion":
            self.toggle_theme()

    def create_GUI(self):
        # создаем главный вертикальный лейаут
        main_layout = QVBoxLayout()

        # создаем textBrowser и добавляем его в вертикальный лейаут
        self.text_browser = QTextBrowser()
        main_layout.addWidget(self.text_browser)
        font = QtGui.QFont()
        font.setPointSize(self.fontSize)
        self.text_browser.setFont(font)

        # создаем горизонтальный лейаут
        horizontal_layout = QHBoxLayout()

        # создаем маленький вертикальный лейаут
        prev_buttons_layout = QVBoxLayout()
        horizontal_layout.addLayout(prev_buttons_layout)

        # создаем кнопку "prev prev" и добавляем ее в горизонтальный лейаут
        prev_prev_button = QPushButton("Previous paragraph (Ctrl+Left)")
        prev_prev_button.setShortcut("Ctrl+Left")
        prev_buttons_layout.addWidget(prev_prev_button)

        # создаем кнопку "previous" и добавляем ее в горизонтальный лейаут
        prev_button = QPushButton("Previous (Left)")
        prev_button.setShortcut("Left")
        prev_buttons_layout.addWidget(prev_button)

        # создаем label "Font size" и добавляем его в горизонтальный лейаут
        font_size_label = QLabel("Font size")
        horizontal_layout.addWidget(font_size_label)
        font_size_label.setAlignment(QtCore.Qt.AlignCenter)

        # создаем spinBox и добавляем его в горизонтальный лейаут
        self.spin_box = QSpinBox()
        self.spin_box.setValue(self.text_browser.font().pointSize())
        horizontal_layout.addWidget(self.spin_box)

        # создаем маленький вертикальный лейаут для аудио
        audio_setting_layout = QVBoxLayout()
        horizontal_layout.addLayout(audio_setting_layout)

        # создаем кнопку "Repeat" и добавляем ее в вертикальний аудио лейаут
        repeat_button = QPushButton("Repeat (R)")
        audio_setting_layout.addWidget(repeat_button)
        repeat_button.setShortcut("R")

        self.switch_audio = QCheckBox("Audio (V)", self)
        audio_setting_layout.addWidget(self.switch_audio)
        self.switch_audio.setShortcut("V")
        if self.audio_enabled:
            self.switch_audio.toggle()

        self.switch_audio_slow = QCheckBox("Slow", self)
        audio_setting_layout.addWidget(self.switch_audio_slow)
        if self.slow_reading:
            self.switch_audio_slow.toggle()

        # создаем маленький вертикальный лейаут
        go_to_page_layout = QVBoxLayout()
        horizontal_layout.addLayout(go_to_page_layout)

        # создаем кнопку "go to page" и добавляем ее в горизонтальный лейаут
        self.go_to_page_label = QLabel("Go to page:")
        go_to_page_layout.addWidget(self.go_to_page_label)
        self.go_to_page_label.setMinimumWidth(80)
        self.go_to_page_label.setMaximumWidth(100)
        self.go_to_page_label.setAlignment(Qt.AlignCenter)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_field = QLineEdit()
        go_to_page_layout.addWidget(self.input_field)
        self.input_field.setMinimumWidth(80)
        self.input_field.setMaximumWidth(100)
        self.input_field.setAlignment(QtCore.Qt.AlignCenter)

        # создаем маленький вертикальный лейаут
        pages_layout = QVBoxLayout()
        horizontal_layout.addLayout(pages_layout)

        self.switch_Hide_current_page = QCheckBox("View current page", self)
        pages_layout.addWidget(self.switch_Hide_current_page)
        if self.view_current_page:
            self.switch_Hide_current_page.toggle()

        self.switch_Hide_all_pages = QCheckBox("View all pages", self)
        pages_layout.addWidget(self.switch_Hide_all_pages)
        if self.view_all_pages:
            self.switch_Hide_all_pages.toggle()

        # создаем маленький вертикальный лейаут
        label_layout = QVBoxLayout()
        horizontal_layout.addLayout(label_layout)

        # создаем label "???" и добавляем его в горизонтальный лейаут
        self.current_page_label = QLabel("?")
        label_layout.addWidget(self.current_page_label)
        self.current_page_label.setMinimumWidth(60)
        self.current_page_label.setAlignment(Qt.AlignCenter)

        # создаем label "???" и добавляем его в горизонтальный лейаут
        self.all_pages_label = QLabel("?")
        label_layout.addWidget(self.all_pages_label)
        self.all_pages_label.setMinimumWidth(60)
        self.all_pages_label.setAlignment(Qt.AlignCenter)

        # создаем кнопку и добавляем ее в вертикальный лейаут
        toggle_button = QPushButton("Change toggle")
        horizontal_layout.addWidget(toggle_button)

        # создаем маленький вертикальный лейаут
        next_next_layout = QVBoxLayout()
        horizontal_layout.addLayout(next_next_layout)

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        next_next_button = QPushButton("next paragraph (Ctrl+Right)")
        next_next_button.setShortcut("Ctrl+Right")
        next_next_layout.addWidget(next_next_button)

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        next_button = QPushButton("next sentence (Right)")
        next_button.setShortcut("Right")
        next_next_layout.addWidget(next_button)

        # добавляем горизонтальный лейаут в вертикальный лейаут
        main_layout.addLayout(horizontal_layout)

        # создаем маленький горизонтальный лейаут
        path_to_file_layout = QHBoxLayout()
        main_layout.addLayout(path_to_file_layout)

        # создаем label
        path_to_file_label = QLabel("Path to file: ")
        path_to_file_layout.addWidget(path_to_file_label)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_path_to_file = QLineEdit()
        path_to_file_layout.addWidget(self.input_path_to_file)
        self.input_path_to_file.setAlignment(QtCore.Qt.AlignCenter)

        # создаем кнопку
        button_navigator = QPushButton("Open (O)")
        button_navigator.setShortcut("O")
        path_to_file_layout.addWidget(button_navigator)

        # создаем маленький горизонтальный лейаут
        find_song_layout = QHBoxLayout()
        main_layout.addLayout(find_song_layout)

        # создаем label
        find_song_label = QLabel("Find song:    ")
        find_song_layout.addWidget(find_song_label)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_find_songs = QLineEdit()
        find_song_layout.addWidget(self.input_find_songs)
        self.input_find_songs.setAlignment(QtCore.Qt.AlignCenter)

        # устанавливаем вертикальный лейаут в качестве главного лейаута окна
        self.setLayout(main_layout)

        # связываем кнопку со слотом
        toggle_button.clicked.connect(self.toggle_theme)
        next_button.clicked.connect(self.next_button)
        next_next_button.clicked.connect(self.next_next_button)
        prev_button.clicked.connect(self.prev_button)
        prev_prev_button.clicked.connect(self.prev_prev_button)

        self.switch_audio.stateChanged.connect(self.audio_switch)
        repeat_button.clicked.connect(self.repeat)
        # Соединение событий прокрутки колесика мыши и изменения размера шрифта в text_browser
        self.spin_box.valueChanged.connect(self.changeFont)
        self.switch_Hide_all_pages.stateChanged.connect(self.hide_all_pages)
        self.switch_Hide_current_page.stateChanged.connect(self.hide_curren_page)
        self.spin_box.setMaximumWidth(40)

        # устанавливаем обработчик событий для поля input_field
        self.input_field.editingFinished.connect(self.handle_editing_finished)
        self.input_path_to_file.editingFinished.connect(self.handle_editing_path)
        self.input_find_songs.editingFinished.connect(self.handle_editing_song)

        button_navigator.clicked.connect(self.select_file)

        self.input_path_to_file.setPlaceholderText("{}".format(self.last_book))
        self.input_find_songs.setPlaceholderText("{}".format(self.last_song))

        if self.active_mode == "book":
            self.setWindowTitle("{}".format(self.last_book))
        if self.active_mode == "song":
            self.setWindowTitle("{}".format(self.last_song))

    def handle_editing_song(self):
        self.active_mode = "song"
        find_text_filtered = self.input_find_songs.text().replace(" ", "-").lower()
        if find_text_filtered != "":
            if find_text_filtered in self.bookmarks_song:
                self.bookmark, self.count = self.bookmarks_song[find_text_filtered]
            else:
                self.bookmark = 0
                self.count = 0
            self.last_song = find_text_filtered

        self.input_find_songs.setPlaceholderText("{}".format(self.last_song))
        self.setWindowTitle("{}".format(self.last_song))

        self.input_find_songs.clearFocus()

        self.read_song()

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", ".txt file (*.txt)",
                                                  options=options)
        if fileName:
            self.input_path_to_file.setText(fileName)
            self.handle_editing_path()



    def read_song(self):
        self.text = ""
        try:
            lyrict_title = self.last_song

            # URL страницы с текстом песни
            url = 'https://muztext.com/lyrics/{}'.format(lyrict_title)

            # Отправляем GET-запрос на сервер
            response = requests.get(url)

            # Парсим HTML-страницу с помощью BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим элемент с текстом песни
            lyrics = soup.find('table', {'class': 'orig'})

            # Выводим текст песни
            self.text = lyrics.text
        except:
            pass

        self.bookmark, self.count = self.bookmarks_song.get(self.last_song, (0, 0))

        if self.text == "":
            self.text += "The song was not found. Try again. Input format: artist title. Example: Dynazty Waterfall"
            self.count = 0
            self.bookmark = 0
        else:
            self.input_find_songs.clear()

        temp_list = self.text.split("(оригинал)")
        self.list_paragraph = temp_list[-1].split("\n")
        self.list_paragraph = [x for x in self.list_paragraph if x]
        self.formint_output_text()

    def download_settings(self):
        self.settings = QSettings("halatsyn_zakhar", "book_reader")

        # Загрузка настроек
        self.bookmarks_book = self.settings.value("bookmarks_book", {})
        self.bookmarks_song = self.settings.value("bookmarks_song", {})
        self.active_mode = self.settings.value("active_mode", "book")
        self.last_book = self.settings.value("last_book", "")
        self.last_song = self.settings.value("last_song", "")
        self.fontSize = self.settings.value("fontSize", 20)
        self.audio_enabled = self.settings.value("audio_enabled", False)
        self.slow_reading = self.settings.value("slow_reading", False)
        self.view_current_page = self.settings.value("view_current_page", True)
        self.view_all_pages = self.settings.value("view_all_pages", False)
        self.night_toggle = self.settings.value("night_toggle", "fusion")
        self.window_geometry_x = self.settings.value("window_geometry_x", 800)
        self.window_geometry_y = self.settings.value("window_geometry_y", 600)
        self.window_geometry_width = self.settings.value("window_geometry_width", 800)
        self.window_geometry_height = self.settings.value("window_geometry_height", 600)

        # Преобразование типов данных
        self.fontSize = int(self.fontSize)
        self.window_geometry_x = int(self.window_geometry_x)
        self.window_geometry_y = int(self.window_geometry_y)
        self.window_geometry_width = int(self.window_geometry_width)
        self.window_geometry_height = int(self.window_geometry_height)

        self.audio_enabled = True if self.audio_enabled.lower() == "true" else False
        self.slow_reading = True if self.slow_reading.lower() == "true" else False
        self.view_current_page = True if self.view_current_page.lower() == "true" else False
        self.view_all_pages = True if self.view_all_pages.lower() == "true" else False

        self.setGeometry(self.window_geometry_x, self.window_geometry_y, self.window_geometry_width,
                         self.window_geometry_height)

    def read_txt(self):
        self.text = ""
        try:
            with open(self.last_book, encoding='windows-1251') as f:
                self.text = f.read()
        except:
            pass

        self.bookmark, self.count = self.bookmarks_book.get(self.last_book, (0, 0))

        if self.text == "":
            self.text += r"The path to the file is missing, or the file is invalid. Please enter a valid relative or " \
                         r"absolute path in the input below. Exemples: Cambias James. A Darkling Sea - " \
                         r"royallib.com.txt or C:\Users\halat\PycharmProjects\book_reader\Cambias James. A Darkling " \
                         r"Sea - royallib.com.txt"
            self.count = 0
            self.bookmark = 0
        else:
            self.input_path_to_file.clear()
        self.list_paragraph = self.text.split("\n\n")
        self.list_paragraph = [x for x in self.list_paragraph if x]
        self.formint_output_text()

    def handle_editing_path(self):
        self.active_mode = "book"
        path = self.input_path_to_file.text()
        absolute_path = os.path.abspath(path)
        if absolute_path != "":
            if absolute_path in self.bookmarks_book:
                """Книга существует, загрузить существующие данные"""
                self.bookmark, self.count = self.bookmarks_book[absolute_path]
            else:
                """Книга новая"""
                self.bookmark = 0
                self.count = 0
            self.last_book = absolute_path

        self.input_path_to_file.setPlaceholderText("{}".format(self.last_book))
        self.setWindowTitle("{}".format(self.last_book))

        self.input_path_to_file.clearFocus()

        self.read_txt()

    def handle_editing_finished(self):
        # обработчик событий, который будет вызываться при изменении поля
        self.count = 0
        self.bookmark = int(self.input_field.text())

        self.input_field.clearFocus()
        self.input_field.clear()

        self.formint_output_text()

    def hide_curren_and_all_page(self):
        if self.switch_Hide_current_page.isChecked():
            self.current_page_label.setText(str(self.bookmark))
            if self.switch_Hide_all_pages.isChecked():
                self.all_pages_label.setText(str(len(self.list_paragraph) - 1))
                self.input_field.setPlaceholderText("{} / {}".format(self.bookmark, len(self.list_paragraph) - 1))
            else:
                self.all_pages_label.setText("?")
                self.input_field.setPlaceholderText("{} / ?".format(self.bookmark))
        else:
            self.current_page_label.setText(("?"))
            if self.switch_Hide_all_pages.isChecked():
                self.all_pages_label.setText(str(len(self.list_paragraph) - 1))
                self.input_field.setPlaceholderText("? / {}".format(len(self.list_paragraph) - 1))
            else:
                self.all_pages_label.setText("?")
                self.input_field.setPlaceholderText("? / ?")

    def hide_curren_page(self, state):
        if state == Qt.Checked:
            self.current_page_label.setText(str(self.bookmark))
            if self.switch_Hide_all_pages.isChecked():
                self.input_field.setPlaceholderText("{} / {}".format(self.bookmark, len(self.list_paragraph) - 1))
            else:
                self.input_field.setPlaceholderText("{} / ?".format(self.bookmark))
        else:
            self.current_page_label.setText(("?"))
            if self.switch_Hide_all_pages.isChecked():
                self.input_field.setPlaceholderText("? / {}".format(len(self.list_paragraph) - 1))
            else:
                self.input_field.setPlaceholderText("? / ?")

    def hide_all_pages(self, state):
        if state == Qt.Checked:
            self.all_pages_label.setText(str(len(self.list_paragraph) - 1))
            if self.switch_Hide_current_page.isChecked():
                self.input_field.setPlaceholderText("{} / {}".format(self.bookmark, len(self.list_paragraph) - 1))
            else:
                self.input_field.setPlaceholderText("? / {}".format(len(self.list_paragraph) - 1))
        else:
            self.all_pages_label.setText(("?"))
            if self.switch_Hide_current_page.isChecked():
                self.input_field.setPlaceholderText("{} / ?".format(self.bookmark))
            else:
                self.input_field.setPlaceholderText("? / ?")

    def event(self, event):
        # Проверяем, что произошло событие колеса мыши с зажатой клавишей Ctrl
        if event.type() == QEvent.Wheel and event.modifiers() == Qt.ControlModifier:
            font = self.text_browser.font()
            font_size = font.pointSize()
            self.spin_box.setValue(font_size)  # Устанавливаем новое значение для spinBox

        return super().event(event)

    def repeat(self):
        pygame.quit()
        pygame.init()
        tts = gTTS(self.list_sentences[self.count], slow=self.switch_audio_slow.isChecked())
        tts.save('sentence.mp3')
        song = pygame.mixer.Sound('sentence.mp3')
        song.play()

    def audio_switch(self, state):
        if state == Qt.Checked:
            self.repeat()
        else:
            # Выключить аудио
            pygame.quit()

    def google_Translate(self, text):
        translator = Translator()
        text_res = translator.translate(text, dest="ru")
        return text_res.text

    def next_button(self):
        self.count += 1
        n = len(self.list_sentences)
        # если счетчик достиг конца книги и направление вперед, то переводим его в начало
        if self.count == n:
            self.count = 0
            if self.bookmark != len(self.list_paragraph) - 1:
                self.bookmark += 1

        self.formint_output_text()

    def next_next_button(self):
        if self.bookmark != len(self.list_paragraph) - 1:
            self.count = 0
            self.bookmark += 1

        self.formint_output_text()

    def prev_button(self):
        if self.count == 0:
            if self.bookmark != 0:
                self.bookmark -= 1

            self.count = len(self.scan_sentence(self.list_paragraph[self.bookmark])) - 1
        else:
            self.count -= 1

        self.formint_output_text()

    def prev_prev_button(self):
        self.count = 0
        if self.bookmark != 0:
            self.bookmark -= 1

        self.formint_output_text()

    def toggle_theme(self):
        # определяем текущую тему
        if self.style().objectName() == "fusion":
            # переключаем на светлую тему
            QApplication.setStyle("windows")
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.WindowText, QColor(27, 27, 27))
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(27, 27, 27))
            palette.setColor(QPalette.Text, QColor(27, 27, 27))
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, QColor(27, 27, 27))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(0, 122, 255))
            palette.setColor(QPalette.Highlight, QColor(0, 122, 255))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
            QApplication.setPalette(palette)
        else:
            # переключаем на темную тему, как в предыдущем примере
            QApplication.setStyle('fusion')
            palette = QPalette()
            palette.setColor(palette.Window, QColor(53, 53, 53))
            palette.setColor(palette.WindowText, Qt.white)
            palette.setColor(palette.Base, QColor(25, 25, 25))
            palette.setColor(palette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(palette.ToolTipBase, Qt.white)
            palette.setColor(palette.ToolTipText, Qt.white)
            palette.setColor(palette.Text, Qt.white)
            palette.setColor(palette.Button, QColor(53, 53, 53))
            palette.setColor(palette.ButtonText, Qt.white)
            palette.setColor(palette.BrightText, Qt.red)
            palette.setColor(palette.Link, QColor(42, 130, 218))
            palette.setColor(palette.Highlight, QColor(42, 130, 218))
            palette.setColor(palette.HighlightedText, Qt.black)
            QApplication.setPalette(palette)

        self.text_browser.setText("")  # clean output
        self.output_paragraph()

    def changeFont_update(self, event):
        if event.modifiers() == Qt.ControlModifier:  # Проверяем, что зажата клавиша Ctrl
            font = self.text_browser.font()
            font_size = font.pointSize()
            self.spin_box.setValue(font_size)  # Устанавливаем новое значение для spinBox

    def changeFont(self):
        font_size = self.spin_box.value()  # Получаем текущее значение spinBox
        font = self.text_browser.font()  # Получаем текущий шрифт text_browser
        font.setPointSize(font_size)  # Устанавливаем новый размер шрифта
        self.text_browser.setFont(font)  # Устанавливаем новый шрифт для text_browser

    def filter_text(self, text):
        # заменяем спецсимволы на их HTML-эквиваленты
        text = html.escape(text)
        # заменяем символы переноса строки на тег <br>
        text = text.replace('\n', '<br>')
        # заменяем символы табуляции на тег <pre>
        text = text.replace('\t', '<pre>')
        # заменяем пробелы в конце предложений

        return text

    def out_red(self, text, end="\n"):
        self.text_browser.insertHtml('<span style="color: #ff0000;">{}</span>'.format(self.filter_text(text + end)))

    def out(self, text, end="\n"):
        self.text_browser.insertHtml(self.filter_text(text + end))

    def out_marker1(self, text, end="\n"):
        if self.style().objectName() == "fusion":
            self.text_browser.insertHtml('<span style="color: #ffff00;">{}</span>'.format(self.filter_text(text + end)))
        else:
            self.text_browser.insertHtml('<span style="color: #0000ff;">{}</span>'.format(self.filter_text(text + end)))

    def out_marker2(self, text, end="\n"):
        if self.style().objectName() == "fusion":
            self.text_browser.insertHtml('<span style="color: #0000ff;">{}</span>'.format(self.filter_text(text + end)))
        else:
            self.text_browser.insertHtml('<span style="color: #ffff00;">{}</span>'.format(self.filter_text(text + end)))

    def scan_sentence(self, text):
        sentences = nltk.sent_tokenize(text)
        return sentences

    def formint_output_text(self):
        self.text_browser.setText("")  # clean output

        self.currentParagraph = self.list_paragraph[self.bookmark]

        if self.currentParagraph[0] == "\n":
            """Обработка исключения, когда вначале лишний перевод строки
            Указывает на смену темы"""
            self.currentParagraph = self.currentParagraph[1::]
            self.out_marker2("***")

        self.list_sentences = self.scan_sentence(self.currentParagraph)

        self.text_trans = self.google_Translate(self.currentParagraph)

        self.list_sentences_trans = self.scan_sentence(self.text_trans)

        self.output_paragraph()

    def output_paragraph(self):
        if self.bookmark == 0:
            self.out_marker2("BEGIN\n")

        """Вывод параграфа и перевода, с выделением предложения"""

        for i in range(len(self.list_sentences)):
            if self.count == i:
                self.out_marker1(self.list_sentences[i], end=" ")
            else:
                self.out(self.list_sentences[i], end=" ")

        self.out("")
        self.out("")

        for i in range(len(self.list_sentences_trans)):
            if self.count == i:
                self.out_marker1(self.list_sentences_trans[i], end=" ")
            else:
                self.out(self.list_sentences_trans[i], end=" ")

        if self.bookmark == len(self.list_paragraph) - 1:
            self.out_marker2("\n\nTHE END")

        if self.switch_audio.isChecked():
            self.repeat()

        self.hide_curren_and_all_page()

        if self.active_mode == "book":
            self.bookmarks_book[self.last_book] = (self.bookmark, self.count)
        elif self.active_mode == "song":
            self.bookmarks_song[self.last_song] = (self.bookmark, self.count)
        self.save_settings()

        # устанавливаем валидатор для ограничения ввода только целых чисел
        validator = QIntValidator(0, len(self.list_paragraph) - 1, self)
        self.input_field.setValidator(validator)

    def save_settings(self):
        # Сохранение настроек

        self.settings.setValue("bookmarks_book", self.bookmarks_book)
        self.settings.setValue("bookmarks_song", self.bookmarks_song)
        self.settings.setValue("active_mode", self.active_mode)
        self.settings.setValue("last_book", self.last_book)
        self.settings.setValue("last_song", self.last_song)
        self.settings.setValue("fontSize", self.text_browser.font().pointSize())
        self.settings.setValue("audio_enabled", self.switch_audio.isChecked())
        self.settings.setValue("slow_reading", self.switch_audio_slow.isChecked())
        self.settings.setValue("view_current_page", self.switch_Hide_current_page.isChecked())
        self.settings.setValue("view_all_pages", self.switch_Hide_all_pages.isChecked())
        self.settings.setValue("night_toggle", self.style().objectName())
        self.settings.setValue("window_geometry_x", self.geometry().x())
        self.settings.setValue("window_geometry_y", self.geometry().y())
        self.settings.setValue("window_geometry_width", self.geometry().width())
        self.settings.setValue("window_geometry_height", self.geometry().height())

    def closeEvent(self, event):
        # вызываем метод save() перед закрытием окна
        self.save_settings()
        # вызываем родительский метод closeEvent()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()

    window.show()
    sys.exit(app.exec_())
