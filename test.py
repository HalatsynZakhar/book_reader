import html
import os
import sys

import re

import nltk as nltk
import pygame
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLabel, \
    QSpinBox, QLineEdit, QCheckBox
from googletrans import Translator
from gtts import gTTS


class MyWindow(QWidget):
    def __init__(self, path_to_book):
        super().__init__()

        # создаем главный вертикальный лейаут
        main_layout = QVBoxLayout()

        # создаем textBrowser и добавляем его в вертикальный лейаут
        self.text_browser = QTextBrowser()
        self.text_browser.setWordWrapMode(False)
        main_layout.addWidget(self.text_browser)

        # создаем горизонтальный лейаут
        horizontal_layout = QHBoxLayout()

        # создаем кнопку "prev prev" и добавляем ее в горизонтальный лейаут
        prev_prev_button = QPushButton("prev paragraph")
        prev_prev_button.setShortcut("Ctrl+Left")
        horizontal_layout.addWidget(prev_prev_button)

        # создаем кнопку "previous" и добавляем ее в горизонтальный лейаут
        prev_button = QPushButton("previous")
        prev_button.setShortcut("Left")
        horizontal_layout.addWidget(prev_button)

        # создаем label "Font size" и добавляем его в горизонтальный лейаут
        font_size_label = QLabel("Font size")
        horizontal_layout.addWidget(font_size_label)

        # создаем spinBox и добавляем его в горизонтальный лейаут
        self.spin_box = QSpinBox()
        self.spin_box.setValue(8)
        horizontal_layout.addWidget(self.spin_box)

        switch = QCheckBox("Audio", self)
        horizontal_layout.addWidget(switch)
        switch.toggle()


        # создаем кнопку "go to page" и добавляем ее в горизонтальный лейаут
        go_to_page_button = QPushButton("go to page")
        horizontal_layout.addWidget(go_to_page_button)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_field = QLineEdit()
        horizontal_layout.addWidget(self.input_field)

        # создаем кнопку "view current page" и добавляем ее в горизонтальный лейаут
        view_current_page_button = QPushButton("view current page")
        horizontal_layout.addWidget(view_current_page_button)

        # создаем label "???" и добавляем его в горизонтальный лейаут
        label1 = QLabel("???")
        horizontal_layout.addWidget(label1)

        # создаем кнопку "view pages" и добавляем ее в горизонтальный лейаут
        view_pages_button = QPushButton("view pages")
        horizontal_layout.addWidget(view_pages_button)

        # создаем label "???" и добавляем его в горизонтальный лейаут
        label2 = QLabel("???")
        horizontal_layout.addWidget(label2)

        # создаем кнопку и добавляем ее в вертикальный лейаут
        toggle_button = QPushButton("Change toggle")
        horizontal_layout.addWidget(toggle_button)

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        next_button = QPushButton("next sentence")
        next_button.setShortcut("Right")
        horizontal_layout.addWidget(next_button)

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        next_next_button = QPushButton("next paragraph")
        next_next_button.setShortcut("Ctrl+Right")
        horizontal_layout.addWidget(next_next_button)

        # добавляем горизонтальный лейаут в вертикальный лейаут
        main_layout.addLayout(horizontal_layout)

        # устанавливаем вертикальный лейаут в качестве главного лейаута окна
        self.setLayout(main_layout)

        # чтение файла (указан путь к примеру файлу txt)
        with open(path_to_book, encoding='windows-1251') as f:
            self.text = f.read()

        self.list_paragraph = self.text.split("\n\n")
        self.list_paragraph = [x for x in self.list_paragraph if x]
        with open('bookmark.txt', encoding='windows-1251') as f:
            self.bookmark = int(f.read())
        self.count = 0
        self.tts_play = True
        pygame.init()

        # связываем кнопку со слотом
        toggle_button.clicked.connect(self.toggle_theme)
        next_button.clicked.connect(self.next_button)
        next_next_button.clicked.connect(self.next_next_button)
        prev_button.clicked.connect(self.prev_button)
        prev_prev_button.clicked.connect(self.prev_prev_button)
        self.spin_box.valueChanged.connect(self.changeFont)
        switch.stateChanged.connect(self.audio_switch)

        if self.tts_play:
            pygame.quit()

        self.formint_output_text()

        QApplication.setStyle("windows")
        self.toggle_theme()

    def audio_switch(self, state):
        if state == Qt.Checked:
            # Включить аудио
            self.tts_play = True
        else:
            # Выключить аудио
            self.tts_play = False

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
            self.bookmark += 1
            with open('bookmark.txt', 'w') as file:
                file.write(str(self.bookmark))

        self.formint_output_text()

    def next_next_button(self):
        self.count = 0
        self.bookmark += 1
        with open('bookmark.txt', 'w') as file:
            file.write(str(self.bookmark))
        self.formint_output_text()

    def prev_button(self):
        if self.count == 0:
            self.bookmark -= 1
            with open('bookmark.txt', 'w') as file:
                file.write(str(self.bookmark))

            self.count = len(self.scan_sentence(self.list_paragraph[self.bookmark])) - 1
        else:
            self.count -= 1

        self.formint_output_text()

    def prev_prev_button(self):
        self.count = 0

        self.bookmark -= 1
        with open('bookmark.txt', 'w') as file:
            file.write(str(self.bookmark))

        self.formint_output_text()

    def toggle_theme(self):
        # определяем текущую тему
        print(self.style().objectName())
        if self.style().objectName() == "fusion":
            # переключаем на светлую тему
            QApplication.setStyle("windows")
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(239, 240, 241))
            palette.setColor(QPalette.WindowText, QColor(28, 28, 28))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(228, 228, 228))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 170))
            palette.setColor(QPalette.ToolTipText, QColor(28, 28, 28))
            palette.setColor(QPalette.Text, QColor(28, 28, 28))
            palette.setColor(QPalette.Button, QColor(239, 240, 241))
            palette.setColor(QPalette.ButtonText, QColor(28, 28, 28))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(0, 0, 255))
            palette.setColor(QPalette.Highlight, QColor(76, 175, 80))
            palette.setColor(QPalette.HighlightedText, Qt.white)
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

    def changeFont(self):
        num = self.spin_box.value()
        font = QFont()
        font.setPointSize(num)
        self.text_browser.setFont(font)

    def filter_text(self, text):
        # заменяем спецсимволы на их HTML-эквиваленты
        text = html.escape(text)
        # заменяем символы переноса строки на тег <br>
        text = text.replace('\n', '<br>')
        # заменяем символы табуляции на тег <pre>
        text = text.replace('\t', '<pre>')
        # экранируем пробельные символы
        text = text.replace(' ', '&nbsp;')
        return text

    def out_red(self, text):
        self.text_browser.insertHtml('<span style="color: #ff0000;">{}</span>'.format(self.filter_text(text)))

    def out(self, text):
        self.text_browser.insertHtml(self.filter_text(text))

    def out_marker1(self, text):
        print(text, end="")
        if self.style().objectName() == "fusion":
            self.text_browser.insertHtml('<span style="color: #ffff00;">{}</span>'.format(self.filter_text(text)))
        else:
            self.text_browser.insertHtml('<span style="color: #0000ff;">{}</span>'.format(self.filter_text(text)))

    def out_marker2(self, text):
        print(text, end="")
        if self.style().objectName() == "fusion":
            self.text_browser.insertHtml('<span style="color: #0000ff;">{}</span>'.format(self.filter_text(text)))
        else:
            self.text_browser.insertHtml('<span style="color: #ffff00;">{}</span>'.format(self.filter_text(text)))

    def scan_sentence(self, text):
        sentences = nltk.sent_tokenize(text)
        return sentences

    def formint_output_text(self):
        self.text_browser.setText("")  # clean output

        if self.tts_play:
            pygame.quit()

        if self.bookmark == len(self.list_paragraph):
            self.text_browser = self.out_marker2("***Конец***")
            return

        self.currentParagraph = self.list_paragraph[self.bookmark]

        if self.currentParagraph[0] == "\n":
            """Обработка исключения, когда вначале лишний перевод строки
            Указывает на смену темы"""
            self.currentParagraph = self.currentParagraph[1::]
            self.out_marker2("***\n")

        self.list_sentences = self.scan_sentence(self.currentParagraph)

        self.text_trans = self.google_Translate(self.currentParagraph)

        self.list_sentences_trans = self.scan_sentence(self.text_trans)

        self.output_paragraph()

    def output_paragraph(self):

        """Вывод параграфа и перевода, с выделением предложения"""

        for i in range(len(self.list_sentences)):
            if self.count == i:
                self.out_marker1(self.list_sentences[i])
            else:
                self.out(self.list_sentences[i])

        self.out("\n")
        self.out("\n")

        for i in range(len(self.list_sentences_trans)):
            if self.count == i:
                self.out_marker1(self.list_sentences_trans[i])
            else:
                self.out(self.list_sentences_trans[i])

        if self.tts_play:
            pygame.init()
        if self.tts_play:
            tts = gTTS(self.list_sentences[self.count], slow=True)
            tts.save('sentence.mp3')
            song = pygame.mixer.Sound('sentence.mp3')
            song.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle('fusion')  # задаем стиль приложения
    window = MyWindow("Cambias James. A Darkling Sea - royallib.com.txt")

    window.show()
    sys.exit(app.exec_())
