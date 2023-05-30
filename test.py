import html
import os
import sys
from time import sleep

from PyQt5.QtCore import QSettings
import re

import nltk as nltk
import pygame
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QEvent

from PyQt5.QtGui import QFont, QColor, QPalette, QTextOption, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLabel, \
    QSpinBox, QLineEdit, QCheckBox, QTextEdit
from googletrans import Translator
from gtts import gTTS


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("halatsyn_zakhar", "book_reader")

        # Загрузка настроек
        self.bookmark = self.settings.value("bookmark", 0)
        self.count = self.settings.value("count", 0)
        self.path_to_book = self.settings.value("path_to_book", "")
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
        self.bookmark = int(self.bookmark)
        self.count = int(self.count)
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

        # создаем spinBox и добавляем его в горизонтальный лейаут
        self.spin_box = QSpinBox()
        self.spin_box.setValue(self.text_browser.font().pointSize())
        horizontal_layout.addWidget(self.spin_box)

        # создаем маленький вертикальный лейаут для аудио
        audio_setting_layout = QVBoxLayout()
        horizontal_layout.addLayout(audio_setting_layout)

        # создаем кнопку "Repeat" и добавляем ее в вертикальний аудио лейаут
        repeat_button = QPushButton("Repeat")
        audio_setting_layout.addWidget(repeat_button)

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
        self.go_to_page_label.setMinimumWidth(60)
        self.go_to_page_label.setMaximumWidth(100)
        self.go_to_page_label.setAlignment(Qt.AlignCenter)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_field = QLineEdit()
        go_to_page_layout.addWidget(self.input_field)
        self.input_field.setMinimumWidth(40)
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
        # создаем маленький вертикальный лейаут для аудио
        next_next_layout = QVBoxLayout()
        horizontal_layout.addLayout(next_next_layout)

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        next_button = QPushButton("next sentence (Right)")
        next_button.setShortcut("Right")
        next_next_layout.addWidget(next_button)

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        next_next_button = QPushButton("next paragraph (Ctrl+Right)")
        next_next_button.setShortcut("Ctrl+Right")
        next_next_layout.addWidget(next_next_button)

        # добавляем горизонтальный лейаут в вертикальный лейаут
        main_layout.addLayout(horizontal_layout)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_path_to_file = QLineEdit()
        main_layout.addWidget(self.input_path_to_file)
        self.input_path_to_file.setAlignment(QtCore.Qt.AlignCenter)

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
        # устанавливаем обработчик событий для поля input_field
        self.input_field.editingFinished.connect(self.handle_editing_finished)
        self.input_path_to_file.editingFinished.connect(self.handle_editing_path)


        self.input_path_to_file.setPlaceholderText("{}".format(self.path_to_book))

        # чтение файла (указан путь к примеру файлу txt)
        self.read_txt()
        if self.night_toggle == "fusion":
            self.toggle_theme()

    def read_txt(self):
        self.text = ""
        try:
            with open(self.path_to_book, encoding='windows-1251') as f:
                self.text = f.read()
        except:
            pass
        if self.text == "":
            self.text += "The path to the file is missing, or the file is invalid. Please enter a valid relative or absolute path " \
            "in the input below"
            self.count = 0
            self.bookmark = 0

        self.list_paragraph = self.text.split("\n\n")
        self.list_paragraph = [x for x in self.list_paragraph if x]
        self.formint_output_text()

        # устанавливаем валидатор для ограничения ввода только целых чисел
        validator = QIntValidator(0, len(self.list_paragraph) - 1, self)
        self.input_field.setValidator(validator)


    def handle_editing_path(self):
        self.path_to_book = self.input_path_to_file.text()
        self.input_path_to_file.setPlaceholderText("{}".format(self.path_to_book))

        self.input_path_to_file.clearFocus()
        self.input_path_to_file.clear()

        self.read_txt()

    def handle_editing_finished(self):
        # обработчик событий, который будет вызываться при изменении поля
        self.bookmark = int(self.input_field.text())

        self.input_field.clear()
        self.input_field.clearFocus()


        self.formint_output_text()

    def hide_curren_page2(self):
        if self.switch_Hide_current_page.isChecked():
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
        if self.bookmark==0:
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

        if self.bookmark==len(self.list_paragraph) - 1:
            self.out_marker2("\n\nTHE END")

        if self.switch_audio.isChecked():
            self.repeat()

        self.hide_curren_page2()

        self.save_settings()
    def save_settings(self):
        # Сохранение настроек

        self.settings.setValue("bookmark", self.bookmark)
        self.settings.setValue("count", self.count)
        self.settings.setValue("path_to_book", self.path_to_book)
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
