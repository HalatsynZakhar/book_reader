import html
import inspect
import os
import sys
import threading
import chardet
import requests
from bs4 import BeautifulSoup

import nltk

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QSettings, QEvent
from PyQt5.QtGui import QPalette, QColor, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QSpinBox, QLineEdit, QCheckBox, QFileDialog, QComboBox, QDialog, QColorDialog, QDoubleSpinBox
from lxml import etree

from AudioThread import AudioThread
from CachedTranslator import CachedTranslator
from MyTextBrowser import MyTextBrowser


class MyWindow(QWidget):
    def __init__(self):
        print(inspect.currentframe().f_code.co_name)

        super().__init__()

        self.lock = threading.Lock()

        self.stop_flag = None

        # Создание экземпляра CachedTranslator
        self.translator = CachedTranslator()

        self.download_settings()

        self.create_GUI()

        self.toggle_theme(False)
        # чтение файла (указан путь к примеру файлу txt) и генерация страницы далее
        if self.active_mode == "book":
            self.read_txt()
        elif self.active_mode == "song":
            self.read_song()



    def create_GUI(self):
        print(inspect.currentframe().f_code.co_name)
        # создаем главный вертикальный лейаут
        main_layout = QVBoxLayout()

        # создаем textBrowser и добавляем его в вертикальный лейаут
        self.text_browser = MyTextBrowser()
        main_layout.addWidget(self.text_browser)
        font = QtGui.QFont()
        font.setPointSize(self.fontSize)
        self.text_browser.setFont(font)

        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_browser.toPlainText())

        # создаем горизонтальный лейаут
        horizontal_layout = QHBoxLayout()

        # создаем маленький вертикальный лейаут
        prev_buttons_layout = QVBoxLayout()
        horizontal_layout.addLayout(prev_buttons_layout)

        # создаем кнопку "prev prev" и добавляем ее в горизонтальный лейаут
        self.prev_prev_button = QPushButton(self.google_Translate_init("Previous paragraph") + " (Ctrl+Left)")
        self.prev_prev_button.setShortcut("Ctrl+Left")
        prev_buttons_layout.addWidget(self.prev_prev_button)

        # создаем кнопку "previous" и добавляем ее в горизонтальный лейаут
        self.previous_button = QPushButton(self.google_Translate_init("Previous") + " (Left)")
        self.previous_button.setShortcut("Left")
        prev_buttons_layout.addWidget(self.previous_button)

        choice_lang_and_font_layout = QVBoxLayout()
        horizontal_layout.addLayout(choice_lang_and_font_layout)

        # создаем маленький горизонтальный лейаут
        original_lang_layout = QHBoxLayout()
        choice_lang_and_font_layout.addLayout(original_lang_layout)

        self.lang_of_study_label = QLabel(self.google_Translate_init("Language of study: "))
        original_lang_layout.addWidget(self.lang_of_study_label)

        self.language_combo_original = QComboBox()
        for language, code in self.languages.items():
            self.language_combo_original.addItem(language, code)

        original_lang_layout.addWidget(self.language_combo_original)

        index = self.language_combo_original.findData(self.default_language_orig)
        self.language_combo_original.setCurrentIndex(index)

        # создаем маленький горизонтальный лейаут
        translate_lang_layout = QHBoxLayout()
        choice_lang_and_font_layout.addLayout(translate_lang_layout)

        self.choice_trans_lang_label = QLabel(self.google_Translate_init("Native language: "))
        translate_lang_layout.addWidget(self.choice_trans_lang_label)

        self.language_combo_translate = QComboBox()
        for language, code in self.languages.items():
            self.language_combo_translate.addItem(language, code)
        translate_lang_layout.addWidget(self.language_combo_translate)

        index = self.language_combo_translate.findData(self.default_language_trans)
        self.language_combo_translate.setCurrentIndex(index)

        font_layout = QHBoxLayout()
        choice_lang_and_font_layout.addLayout(font_layout)

        # создаем label "Font size" и добавляем его в горизонтальный лейаут
        self.font_size_label = QLabel(self.google_Translate_init("Font size"))
        font_layout.addWidget(self.font_size_label)
        self.font_size_label.setAlignment(QtCore.Qt.AlignCenter)

        # создаем spinBox и добавляем его в горизонтальный лейаут
        self.spin_box = QSpinBox()
        self.spin_box.setValue(self.text_browser.font().pointSize())
        font_layout.addWidget(self.spin_box)

        # создаем маленький вертикальный лейаут для аудио
        audio_setting_layout = QVBoxLayout()
        horizontal_layout.addLayout(audio_setting_layout)

        # создаем кнопку "Repeat" и добавляем ее в вертикальний аудио лейаут
        self.repeat_button = QPushButton(self.google_Translate_init("Repeat playback") + " (R)")
        audio_setting_layout.addWidget(self.repeat_button)
        self.repeat_button.setShortcut("R")

        self.switch_audio = QCheckBox(self.google_Translate_init("Audio") + " (V)", self)
        audio_setting_layout.addWidget(self.switch_audio)
        self.switch_audio.setShortcut("V")
        if self.audio_enabled:
            self.switch_audio.toggle()

        self.switch_auto_play = QCheckBox(self.google_Translate_init("Autoplay"), self)
        audio_setting_layout.addWidget(self.switch_auto_play)
        if self.auto_play:
            self.switch_auto_play.toggle()

        playback_speed_layout = QHBoxLayout()
        audio_setting_layout.addLayout(playback_speed_layout)

        self.playback_speed_label = QLabel(self.google_Translate_init("Playback speed"))
        playback_speed_layout.addWidget(self.playback_speed_label)


        self.spin_box_playback_speed = QDoubleSpinBox()
        playback_speed_layout.addWidget(self.spin_box_playback_speed)
        self.spin_box_playback_speed.setMinimum(0.25)
        self.spin_box_playback_speed.setMaximum(4.0)
        self.spin_box_playback_speed.setSingleStep(0.1)
        self.spin_box_playback_speed.setValue(self.playback_speed)
        playback_speed_layout.addWidget(self.spin_box_playback_speed)

        # создаем маленький вертикальный лейаут
        go_to_page_layout = QVBoxLayout()
        horizontal_layout.addLayout(go_to_page_layout)

        # создаем кнопку "go to page" и добавляем ее в горизонтальный лейаут
        self.go_to_page_label = QLabel(self.google_Translate_init("Go to page:"))
        go_to_page_layout.addWidget(self.go_to_page_label)
        self.go_to_page_label.setMinimumWidth(80)
        self.go_to_page_label.setAlignment(Qt.AlignCenter)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_field = QLineEdit()
        go_to_page_layout.addWidget(self.input_field)
        self.input_field.setMinimumWidth(80)
        self.input_field.setMaximumWidth(120)
        self.input_field.setAlignment(QtCore.Qt.AlignCenter)

        # создаем маленький вертикальный лейаут
        pages_layout = QVBoxLayout()
        horizontal_layout.addLayout(pages_layout)

        self.switch_Hide_current_page = QCheckBox(self.google_Translate_init("View current page"), self)
        pages_layout.addWidget(self.switch_Hide_current_page)
        if self.view_current_page:
            self.switch_Hide_current_page.toggle()

        self.switch_Hide_all_pages = QCheckBox(self.google_Translate_init("View all pages"), self)
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

        # создаем маленький вертикальный лейаут
        toggle_and_aljust_layout = QVBoxLayout()
        horizontal_layout.addLayout(toggle_and_aljust_layout)

        self.switch_center = QCheckBox(self.google_Translate_init("Center alignment") + " (E)", self)
        toggle_and_aljust_layout.addWidget(self.switch_center)
        self.switch_center.setShortcut("E")
        if self.center_setting:
            self.switch_center.toggle()

        self.switch_night_mode = QCheckBox(self.google_Translate_init("Night mode") + " (N)", self)
        toggle_and_aljust_layout.addWidget(self.switch_night_mode)
        self.switch_night_mode.setShortcut("N")
        if self.night_mode:
            self.switch_night_mode.toggle()

        # Создаем кнопку настроек интерфейса
        self.settings_button = QPushButton(self.google_Translate_init("Interface settings"), self)
        toggle_and_aljust_layout.addWidget(self.settings_button)

        # создаем маленький вертикальный лейаут
        next_next_layout = QVBoxLayout()
        horizontal_layout.addLayout(next_next_layout)

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        self.next_next_button = QPushButton(self.google_Translate_init("next paragraph") + " (Ctrl+Right)")
        self.next_next_button.setShortcut("Ctrl+Right")
        next_next_layout.addWidget(self.next_next_button)

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        self.next_button = QPushButton(self.google_Translate_init("next sentence") + " (Right)")
        self.next_button.setShortcut("Right")
        next_next_layout.addWidget(self.next_button)

        # добавляем горизонтальный лейаут в вертикальный лейаут
        main_layout.addLayout(horizontal_layout)

        # создаем маленький горизонтальный лейаут
        path_to_file_layout = QHBoxLayout()
        main_layout.addLayout(path_to_file_layout)

        # создаем label
        self.path_to_file_label = QLabel(self.google_Translate_init("Path to file: "))
        path_to_file_layout.addWidget(self.path_to_file_label)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_path_to_file = QLineEdit()
        path_to_file_layout.addWidget(self.input_path_to_file)
        self.input_path_to_file.setAlignment(QtCore.Qt.AlignCenter)
        self.input_path_to_file.setMaxLength(999)

        # создаем кнопку
        self.button_navigator = QPushButton(self.google_Translate_init("Open file") + " (O)")
        self.button_navigator.setShortcut("O")
        path_to_file_layout.addWidget(self.button_navigator)

        self.select_bookmark_button = QPushButton(self.google_Translate_init("search history"), self)
        path_to_file_layout.addWidget(self.select_bookmark_button)

        # создаем маленький горизонтальный лейаут
        find_song_layout = QHBoxLayout()
        main_layout.addLayout(find_song_layout)

        # создаем label
        self.find_song_label = QLabel(self.google_Translate_init("Find song: "))
        find_song_layout.addWidget(self.find_song_label)

        # создаем input поле и добавляем его в горизонтальный лейаут
        self.input_find_songs = QLineEdit()
        find_song_layout.addWidget(self.input_find_songs)
        self.input_find_songs.setAlignment(QtCore.Qt.AlignCenter)
        self.input_find_songs.setMaxLength(100)

        self.select_bookmark_song_button = QPushButton(self.google_Translate_init("search history"), self)
        find_song_layout.addWidget(self.select_bookmark_song_button)

        # устанавливаем вертикальный лейаут в качестве главного лейаута окна
        self.setLayout(main_layout)

        # связываем кнопку со слотом

        self.language_combo_original.currentIndexChanged.connect(self.language_changed_original)
        self.language_combo_translate.currentIndexChanged.connect(self.language_changed_translate)

        self.select_bookmark_song_button.clicked.connect(self.select_bookmark_song)
        self.select_bookmark_button.clicked.connect(self.select_bookmark)
        self.next_button.clicked.connect(self.next_button_clicked)
        self.next_next_button.clicked.connect(self.next_next_button_clicked)
        self.previous_button.clicked.connect(self.prev_button_clicked)
        self.prev_prev_button.clicked.connect(self.prev_prev_button_clicked)


        self.switch_night_mode.stateChanged.connect(lambda: self.toggle_theme())
        self.switch_center.stateChanged.connect(self.center)
        self.switch_auto_play.stateChanged.connect(self.auto_play_func)
        self.switch_audio.stateChanged.connect(self.audio_switch)
        self.repeat_button.clicked.connect(self.play_audio)
        self.settings_button.clicked.connect(self.open_settings_dialog)

        # Соединение событий прокрутки колесика мыши и изменения размера шрифта в text_browser
        self.spin_box.valueChanged.connect(self.changeFont_valueChanged)
        self.spin_box_playback_speed.valueChanged.connect(self.spin_box_playback_speed_func)

        self.switch_Hide_all_pages.stateChanged.connect(self.hide_all_pages)
        self.switch_Hide_current_page.stateChanged.connect(self.hide_curren_page)
        self.spin_box.setMaximumWidth(40)
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(999)

        # устанавливаем обработчик событий для поля input_field
        self.input_field.editingFinished.connect(self.handle_editing_finished)
        self.input_path_to_file.editingFinished.connect(self.handle_editing_path)
        self.input_find_songs.editingFinished.connect(self.handle_editing_song)

        self.button_navigator.clicked.connect(self.select_file)

        self.input_path_to_file.setPlaceholderText("{}".format(self.last_book))
        self.input_find_songs.setPlaceholderText(" ".join(self.last_song))

        if self.active_mode == "book":
            self.setWindowTitle("{}".format(self.last_book))
        if self.active_mode == "song":
            self.setWindowTitle(" ".join(self.last_song))

    def spin_box_playback_speed_func(self):
        self.settings.setValue("playback_speed", self.spin_box_playback_speed.value())
    def auto_go_next(self):
        print(inspect.currentframe().f_code.co_name)

        if self.switch_audio.isChecked() and self.switch_auto_play.isChecked():
            self.next_button_clicked()
        pass

    def select_bookmark_song(self):
        print(inspect.currentframe().f_code.co_name)

        bookmarks_list_song = QComboBox(self)
        history_sort = sorted(list([" ".join(i) for i in self.bookmarks_song.keys()]))
        bookmarks_list_song.addItems(history_sort)

        if self.active_mode == "song":
            index = bookmarks_list_song.findText(" ".join(self.last_song))
            bookmarks_list_song.setCurrentIndex(index)
        else:
            bookmarks_list_song.setCurrentIndex(-1)

        bookmarks_list_song.currentIndexChanged.connect(lambda: self.handle_bookmark_selection_song(bookmarks_list_song))
        bookmarks_list_song.showPopup()

    def handle_bookmark_selection_song(self, bookmark_list_song):
        print(inspect.currentframe().f_code.co_name)

        selected_bookmark_song = bookmark_list_song.currentText()
        self.input_find_songs.setText(selected_bookmark_song)
        self.handle_editing_song()

    def select_bookmark(self):
        print(inspect.currentframe().f_code.co_name)

        bookmarks_list = QComboBox(self)
        history_sort = sorted(list(self.bookmarks_book.keys()))
        bookmarks_list.addItems(history_sort)

        if self.active_mode == "book":
            index = bookmarks_list.findText(self.last_book)
            bookmarks_list.setCurrentIndex(index)
        else:
            bookmarks_list.setCurrentIndex(-1)

        bookmarks_list.currentIndexChanged.connect(lambda: self.handle_bookmark_selection(bookmarks_list))
        bookmarks_list.showPopup()

    def handle_bookmark_selection(self, bookmark_list):
        print(inspect.currentframe().f_code.co_name)

        selected_bookmark = bookmark_list.currentText()
        self.input_path_to_file.setText(selected_bookmark)
        self.handle_editing_path()

    def open_settings_dialog(self):
        print(inspect.currentframe().f_code.co_name)

        # Создаем диалоговое окно настроек интерфейса
        self.settings_dialog = QDialog(self)

        if self.switch_night_mode.isChecked():
            self.settings_dialog.setWindowTitle(self.translate_dialog_windows[0])
        else:
            self.settings_dialog.setWindowTitle(self.translate_dialog_windows[1])

        main_layout = QVBoxLayout()

        choose_color_name = self.translate_dialog_windows[2]

        self.color_buttons = []
        for i in range(len(self.translate_dialog_windows)-2):
            if i>=len(self.translate_dialog_windows)-2-2:
                break
            hor_layout = QHBoxLayout()
            color_label = QLabel(self.translate_dialog_windows[3 + i])
            color_label.setMinimumWidth(250)

            hor_layout.addWidget(color_label)

            color_button = QPushButton(choose_color_name)
            color_button.clicked.connect(lambda _, index=i: self.show_color_dialog(index))
            if self.switch_night_mode.isChecked():
                color_button.setStyleSheet("background-color: {}".format(self.night_mod_colors[i].name()))
            else:
                color_button.setStyleSheet("background-color: {}".format(self.day_mode_colors[i].name()))

            self.color_buttons.append(color_button)

            hor_layout.addWidget(color_button)

            main_layout.addLayout(hor_layout)

        default_button = QPushButton(self.translate_dialog_windows[-1])
        default_button.clicked.connect(self.reset_theme)

        main_layout.addWidget(default_button)

        self.settings_dialog.setLayout(main_layout)

        self.settings_dialog.exec_()

    def reset_theme(self):
        print(inspect.currentframe().f_code.co_name)

        if self.switch_night_mode.isChecked():
            self.night_mod_colors = [i for i in self.night_mode_default]
        else:
            self.day_mode_colors = [i for i in self.day_mode_default]

        self.toggle_theme()

        for i in range(len(self.color_buttons)):
            if self.switch_night_mode.isChecked():
                self.color_buttons[i].setStyleSheet("background-color: {}".format(self.night_mod_colors[i].name()))
            else:
                self.color_buttons[i].setStyleSheet("background-color: {}".format(self.day_mode_colors[i].name()))

    def show_color_dialog(self, index):
        print(inspect.currentframe().f_code.co_name)

        # Создаем диалог выбора цвета
        color = QColorDialog.getColor()
        if self.switch_night_mode.isChecked():
            self.night_mod_colors[index] = color
        else:
            self.day_mode_colors[index] = color
        self.color_buttons[index].setStyleSheet("background-color: {}".format(color.name()))

        self.toggle_theme()
        # Если цвет был выбран, то устанавливаем его для кнопки

    def language_changed_original(self, index):
        print(inspect.currentframe().f_code.co_name)

        if self.active_mode == "book":
            self.read_txt()
        elif self.active_mode == "song":
            self.read_song()

        self.settings.setValue("default_language_orig", self.language_combo_original.currentData())

    def change_language(self):
        print(inspect.currentframe().f_code.co_name)

        """Эта функция выполняется отдельным потоком при изменении языка интерфейса"""
        previous_button_text = self.google_Translate_to_trans_with_eng("Previous paragraph") + " (Ctrl+Left)"
        prev_prev_button_text = self.google_Translate_to_trans_with_eng("Previous") + " (Left)"
        lang_of_study_label_text = self.google_Translate_to_trans_with_eng("Language of study: ")
        choice_trans_lang_label_text = self.google_Translate_to_trans_with_eng("Native language: ")
        font_size_label_text = self.google_Translate_to_trans_with_eng("Font size")
        repaet_button_text = self.google_Translate_to_trans_with_eng("Repeat playback") + " (R)"
        switch_audio_text = self.google_Translate_to_trans_with_eng("Audio") + " (V)"
        switch_audio_text_slow_text = self.google_Translate_to_trans_with_eng("Slow playback")
        go_to_page_label_text = self.google_Translate_to_trans_with_eng("Go to page:")
        switch_hide_current_page_text = self.google_Translate_to_trans_with_eng("View current page")
        switch_hide_all_pages_text = self.google_Translate_to_trans_with_eng("View all pages")
        switch_center_text = self.google_Translate_to_trans_with_eng("Center alignment") + " (E)"
        switch_night_mode_text = self.google_Translate_to_trans_with_eng("Night mode") + " (N)"
        settings_button_text = self.google_Translate_to_trans_with_eng("Interface settings")
        next_button_text = self.google_Translate_to_trans_with_eng("next paragraph") + " (Ctrl+Right)"
        next_next_button_text = self.google_Translate_to_trans_with_eng("next sentence") + " (Right)"
        path_to_file_label_text = self.google_Translate_to_trans_with_eng("Path to file: ")
        find_song_label_text = self.google_Translate_to_trans_with_eng("Find song: ")
        button_navigator_text = self.google_Translate_to_trans_with_eng("Open file") + " (O)"
        select_bookmark = self.google_Translate_to_trans_with_eng("Search history")
        select_bookmark_song = self.google_Translate_to_trans_with_eng("Search history")
        swith_autoplay = self.google_Translate_to_trans_with_eng("Autoplay")
        playback_speed = self.google_Translate_to_trans_with_eng("Playback speed")

        self.spin_box_playback_speed.setText(playback_speed)
        self.previous_button.setText(previous_button_text)
        self.prev_prev_button.setText(prev_prev_button_text)
        self.lang_of_study_label.setText(lang_of_study_label_text)
        self.choice_trans_lang_label.setText(choice_trans_lang_label_text)
        self.font_size_label.setText(font_size_label_text)
        self.repeat_button.setText(repaet_button_text)
        self.switch_audio.setText(switch_audio_text)
        self.switch_auto_play.setText(swith_autoplay)
        self.spin_box_playback_speed.setText(switch_audio_text_slow_text)
        self.go_to_page_label.setText(go_to_page_label_text)
        self.switch_Hide_current_page.setText(switch_hide_current_page_text)
        self.switch_Hide_all_pages.setText(switch_hide_all_pages_text)
        self.switch_center.setText(switch_center_text)
        self.switch_night_mode.setText(switch_night_mode_text)
        self.settings_button.setText(settings_button_text)
        self.next_button.setText(next_button_text)
        self.next_next_button.setText(next_next_button_text)
        self.path_to_file_label.setText(path_to_file_label_text)
        self.find_song_label.setText(find_song_label_text)
        self.button_navigator.setText(button_navigator_text)
        self.select_bookmark_button.setText(select_bookmark)
        self.select_bookmark_song_button.setText(select_bookmark_song)

        self.translate_dialog_windows = [self.google_Translate_to_trans_with_eng(i) for i in
                                         self.orgignal_dialog_window]

    def language_changed_translate(self, index):
        print(inspect.currentframe().f_code.co_name)

        thread = threading.Thread(target=self.change_language)
        thread.start()

        self.formint_output_text()
        # сохраняем язык перевода в конфигурационный файл
        # и обновляем настройки в вашем приложении

        self.settings.setValue("default_language_trans", self.language_combo_translate.currentData())


    def select_file(self):
        print(inspect.currentframe().f_code.co_name)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, self.google_Translate_to_trans_with_eng("Open File"), "",
                                                  "Text files (*.txt);;FB2 files (*.fb2)", options=options)
        if fileName:
            self.input_path_to_file.setText(fileName)
            self.handle_editing_path()



    def get_musinfo(self, lyrict_title_list):
        print(inspect.currentframe().f_code.co_name + ": ", end=" ")

        # Проверяем, есть ли данные в кеше
        if lyrict_title_list in self.cache_Music:
            print("cache")
            return self.cache_Music[lyrict_title_list]

        try:
            index_of_dash = lyrict_title_list.index("-")
            group_and_music = ("-".join(lyrict_title_list[:index_of_dash]), "-".join(
            lyrict_title_list[index_of_dash + 1:]))

            # URL страницы с текстом песни
            url = 'https://ru.musinfo.net/lyrics/{}'.format("/".join(group_and_music))

            # Отправляем GET-запрос на сервер
            response = requests.get(url)

            # Парсим HTML-страницу с помощью BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим элемент с текстом песни
            lyrics = soup.find('td', {'id': 'lyric-src'})

            text = lyrics.find_all('div', {'class': 'line'})
            text_result = ""
            for i in text:
                if i.text[0] == "[":
                    continue
                text_result += i.text + "\n"

            # Сохраняем данные в кеше
            self.cache_Music[lyrict_title_list] = text_result
        except:
            return ""
        print("musinfo")
        return text_result


    def get_muztext(self, lyrict_title_list):
        print(inspect.currentframe().f_code.co_name + ": ", end=" ")

        # Проверяем, есть ли данные в кеше
        if lyrict_title_list in self.cache_Music:
            print("cache")
            return self.cache_Music[lyrict_title_list]
        try:
            index_of_dash = lyrict_title_list.index("-")
            lyrict_title_and_song = lyrict_title_list[:index_of_dash] + lyrict_title_list[index_of_dash + 1:]

            # URL страницы с текстом песни
            url = 'https://muztext.com/lyrics/{}'.format("-".join(lyrict_title_and_song))

            # Отправляем GET-запрос на сервер
            response = requests.get(url)

            # Парсим HTML-страницу с помощью BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим элемент с текстом песни
            lyrics = soup.find('table', {'class': 'orig'})

            # Сохраняем данные в кеше
            self.cache_Music[lyrict_title_list] = lyrics.text
        except:
            return ""
        print("lyrics.text")
        return lyrics.text

    def read_song(self):
        print(inspect.currentframe().f_code.co_name)

        self.text = self.get_muztext(self.last_song)
        if self.text == "":
            self.text = self.get_musinfo(self.last_song)

        if self.last_song in self.bookmarks_song:
            self.bookmark, self.count = self.bookmarks_song[self.last_song]
        else:
            """Песня новая"""
            if self.text != "":
                """если песня существует, добавляем запись, создаем закладки"""
                self.bookmarks_song[self.last_song] = (0, 0)
                self.bookmark, self.count = self.bookmarks_song[self.last_song]
            else:
                """за данным запросом книги не существует"""
                self.bookmark = 0
                self.count = 0


        if self.text == "":
            self.text += self.google_Translate_to_orig_with_Eng(
                "The song was not found. Try again. Input format: <artist> - <title>. Search example:") + " dynazty - waterfall"
            self.count = 0
            self.bookmark = 0
        else:
            self.input_find_songs.clear()

        temp_list = self.text.split("(оригинал)")
        self.list_paragraph = temp_list[-1].split("\n")
        self.list_paragraph = [x for x in self.list_paragraph if x]

        # устанавливаем валидатор для ограничения ввода только целых чисел
        validator = QIntValidator(1, len(self.list_paragraph), self)
        self.input_field.setValidator(validator)






        self.formint_output_text()



    def download_settings(self):
        print(inspect.currentframe().f_code.co_name)

        self.settings = QSettings("halatsyn_zakhar", "book_reader")

        # Загрузка кеша из QSettings
        self.translator.load_cache_from_settings(self)

        self.languages = {
            "Azərbaycan dili": "az",
            "Bahasa Indonesia": "id",
            "Bosanski": "bs",
            "Català": "ca",
            "Čeština": "cs",
            "Dansk": "da",
            "Deutsch": "de",
            "Eesti": "et",
            "English": "en",
            "Español": "es",
            "Filipino": "tl",
            "Français": "fr",
            "Galego": "gl",
            "Greek": "el",
            "Hrvatski": "hr",
            "Italiano": "it",
            "Kiswahili": "sw",
            "Latviešu": "lv",
            "Lietuvių": "lt",
            "Magyar": "hu",
            "Македонски": "mk",
            "Nederlands": "nl",
            "Norsk": "no",
            "Polski": "pl",
            "Português": "pt",
            "Română": "ro",
            "Русский": "ru",
            "Serbian": "sr",
            "Slovenčina": "sk",
            "Slovenščina": "sl",
            "Suomi": "fi",
            "Svenska": "sv",
            "Tiếng Việt": "vi",
            "Türkçe": "tr",
            "Українська": "uk"
        }

        self.night_mode_default = (QColor(53, 53, 53),
                                   QColor(255, 255, 255),
                                   QColor(25, 25, 25),
                                   QColor(53, 53, 53),
                                   QColor(255, 255, 255),
                                   QColor(255, 255, 255),
                                   QColor(255, 255, 255),
                                   QColor(53, 53, 53),
                                   QColor(255, 255, 255),
                                   QColor(255, 0, 0),
                                   QColor(42, 130, 218),
                                   QColor(42, 130, 218),
                                   QColor(0, 0, 0),
                                   QColor(255, 255, 0),
                                   QColor(255, 0, 0),
                                   QColor(0, 0, 0)
                                   )

        self.day_mode_default = (QColor(255, 255, 255),
                                 QColor(27, 27, 27),
                                 QColor(240, 240, 240),
                                 QColor(255, 255, 255),
                                 QColor(255, 255, 255),
                                 QColor(27, 27, 27),
                                 QColor(27, 27, 27),
                                 QColor(240, 240, 240),
                                 QColor(27, 27, 27),
                                 QColor(255, 0, 0),
                                 QColor(0, 122, 255),
                                 QColor(0, 122, 255),
                                 QColor(255, 255, 255),
                                 QColor(128, 64, 48),
                                 QColor(255, 0, 0),
                                 QColor(255, 255, 255)
                                 )

        # Загрузка настроек
        self.auto_play = self.settings.value("auto_play", "false")
        self.cache_Music = self.settings.value("cache_Music", {})
        self.night_mod_colors = self.settings.value('night_mod_colors',
                                                    [color.name() for color in self.night_mode_default])
        self.day_mode_colors = self.settings.value('day_mode_colors', [color.name() for color in self.day_mode_default])
        self.default_language_orig = self.settings.value('default_language_orig', 'en')
        self.default_language_trans = self.settings.value('default_language_trans', 'en')
        self.bookmarks_book = self.settings.value("bookmarks_book", {})
        self.bookmarks_song = self.settings.value("bookmarks_song", {})
        self.active_mode = self.settings.value("active_mode", "book")
        self.last_book = self.settings.value("last_book", "")
        self.last_song = self.settings.value("last_song", "")
        self.fontSize = self.settings.value("fontSize", 20)
        self.center_setting = self.settings.value("center_setting", "false")
        self.audio_enabled = self.settings.value("audio_enabled", "false")


        self.playback_speed = self.settings.value("playback_speed", 1.0)
        self.view_current_page = self.settings.value("view_current_page", "true")
        self.view_all_pages = self.settings.value("view_all_pages", "false")
        self.night_mode = self.settings.value("night_mode", "true")
        self.window_geometry_x = self.settings.value("window_geometry_x", 800)
        self.window_geometry_y = self.settings.value("window_geometry_y", 600)
        self.window_geometry_width = self.settings.value("window_geometry_width", 800)
        self.window_geometry_height = self.settings.value("window_geometry_height", 600)

        # Преобразование типов данных
        self.playback_speed = float(self.playback_speed)
        self.fontSize = int(self.fontSize)
        self.window_geometry_x = int(self.window_geometry_x)
        self.window_geometry_y = int(self.window_geometry_y)
        self.window_geometry_width = int(self.window_geometry_width)
        self.window_geometry_height = int(self.window_geometry_height)

        self.auto_play = True if self.auto_play.lower() == "true" else False
        self.night_mode = True if self.night_mode.lower() == "true" else False
        self.center_setting = True if self.center_setting.lower() == "true" else False
        self.audio_enabled = True if self.audio_enabled.lower() == "true" else False
        self.view_current_page = True if self.view_current_page.lower() == "true" else False
        self.view_all_pages = True if self.view_all_pages.lower() == "true" else False

        self.setGeometry(self.window_geometry_x, self.window_geometry_y, self.window_geometry_width,
                         self.window_geometry_height)

        self.orgignal_dialog_window = ["Settings for the current theme: night", "Settings for the current theme: day", "Choose color",
                                       "Window background color", "Window text color", "Base color",
                                       "Alternate base color", "Tooltip base color",
                                       "Tooltip text color", "Text color", "Button color", "Button text color",
                                       "Bright text color", "Link color", "Highlight color", "Highlighted text color", "Highlighting a sentence", "Header highlighting", "Unselected text", "default settings"]
        self.translate_dialog_windows = [self.google_Translate_init(i) for i in self.orgignal_dialog_window]

    def read_txt(self):
        print(inspect.currentframe().f_code.co_name)

        self.text = ""

        encodings = ['utf-8', 'windows-1251', 'iso-8859-1']
        try:
            # Определяем кодировку файла
            with open(self.last_book, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
                encodings.insert(0, encoding)
        except:
            pass

        for encoding in encodings:
            try:
                # Load text based on file extension
                if self.last_book.endswith('.txt'):
                    with open(self.last_book, 'r', encoding=encoding) as f:
                        self.text = f.read()
                elif self.last_book.endswith('.fb2'):
                    # Открываем файл
                    with open(self.last_book, 'rb') as file:
                        # Читаем содержимое файла
                        fb2_data = file.read()

                    # Парсим содержимое файла
                    root = etree.fromstring(fb2_data)

                    # Получаем текст книги
                    text = ''
                    for paragraph in root.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                        if paragraph.text is not None:
                            text += paragraph.text.strip() + ' '
                        text += "\n\n"
                    self.text = text
                break
            except:
                pass

        if self.last_book in self.bookmarks_book:
            self.bookmark, self.count = self.bookmarks_book[self.last_book]
        else:
            """Книга новая"""
            if self.text != "":
                """если книга существует, добавляем запись, создаем закладки"""
                self.bookmarks_book[self.last_book] = (0, 0)
                self.bookmark, self.count = self.bookmarks_book[self.last_book]
            else:
                """за данным запросом книги не существует"""
                self.bookmark = 0
                self.count = 0


        if self.text == "":
            self.text += self.google_Translate_to_orig_with_Eng(
                r"The path to the file is missing, or the file is invalid. Please enter a valid relative or " \
                r"absolute path in the input below. Format data: .txt or .fb2. Valid input example: ") + r" Cambias James. A Darkling Sea - " \
                                                                                                         r"royallib.com.txt or C:\Users\halat\PycharmProjects\book_reader\Cambias James. A Darkling " \
                                                                                                         r"Sea - royallib.com.txt"
            self.count = 0
            self.bookmark = 0
        else:
            self.input_path_to_file.clear()
        self.list_paragraph = self.text.split("\n\n")
        self.list_paragraph = [x for x in self.list_paragraph if x]

        # устанавливаем валидатор для ограничения ввода только целых чисел
        validator = QIntValidator(1, len(self.list_paragraph), self)
        self.input_field.setValidator(validator)

        self.formint_output_text()
    def handle_editing_song(self):
        print(inspect.currentframe().f_code.co_name)

        self.active_mode = "song"
        if self.input_find_songs.text() != "":
            text_fil = self.input_find_songs.text().replace("'", " ")
            find_text_filtered = tuple(filter(lambda x: x != '', map(str.lower, text_fil.split())))
            self.last_song = find_text_filtered
            self.settings.setValue("last_song", self.last_song)

        self.input_find_songs.setPlaceholderText("{}".format(" ".join(self.last_song)))
        self.setWindowTitle("{}".format(" ".join(self.last_song)))

        self.input_find_songs.clearFocus()

        self.read_song()
        self.settings.setValue("active_mode", self.active_mode)
    def handle_editing_path(self):
        print(inspect.currentframe().f_code.co_name)

        self.active_mode = "book"
        if self.input_path_to_file.text() != "":
            path = self.input_path_to_file.text()
            path = path.strip()
            absolute_path = os.path.abspath(path)

            self.last_book = absolute_path
            self.settings.setValue("last_book", self.last_book)
        self.input_path_to_file.setPlaceholderText("{}".format(self.last_book))
        self.setWindowTitle("{}".format(self.last_book))

        self.input_path_to_file.clearFocus()

        self.read_txt()
        self.settings.setValue("active_mode", self.active_mode)

    def handle_editing_finished(self):
        print(inspect.currentframe().f_code.co_name)

        # обработчик событий, который будет вызываться при изменении поля
        self.count = 0
        self.bookmark = int(self.input_field.text()) - 1

        self.input_field.clearFocus()
        self.input_field.clear()

        self.formint_output_text()

    def hide_curren_and_all_page(self):
        print(inspect.currentframe().f_code.co_name)

        if self.switch_Hide_current_page.isChecked():
            self.current_page_label.setText(str(self.bookmark + 1))
            if self.switch_Hide_all_pages.isChecked():
                self.all_pages_label.setText(str(len(self.list_paragraph)))
                self.input_field.setPlaceholderText("{} / {}".format(self.bookmark + 1, len(self.list_paragraph)))
            else:
                self.all_pages_label.setText("?")
                self.input_field.setPlaceholderText("{} / ?".format(self.bookmark + 1))
        else:
            self.current_page_label.setText(("?"))
            if self.switch_Hide_all_pages.isChecked():
                self.all_pages_label.setText(str(len(self.list_paragraph)))
                self.input_field.setPlaceholderText("? / {}".format(len(self.list_paragraph)))
            else:
                self.all_pages_label.setText("?")
                self.input_field.setPlaceholderText("? / ?")

    def hide_curren_page(self, state):
        print(inspect.currentframe().f_code.co_name)

        if state == Qt.Checked:
            self.current_page_label.setText(str(self.bookmark + 1))
            if self.switch_Hide_all_pages.isChecked():
                self.input_field.setPlaceholderText("{} / {}".format(self.bookmark + 1, len(self.list_paragraph)))
            else:
                self.input_field.setPlaceholderText("{} / ?".format(self.bookmark + 1))
        else:
            self.current_page_label.setText(("?"))
            if self.switch_Hide_all_pages.isChecked():
                self.input_field.setPlaceholderText("? / {}".format(len(self.list_paragraph)))
            else:
                self.input_field.setPlaceholderText("? / ?")

        self.settings.setValue("view_current_page", self.switch_Hide_current_page.isChecked())
    def hide_all_pages(self, state):
        print(inspect.currentframe().f_code.co_name)

        if state == Qt.Checked:
            self.all_pages_label.setText(str(len(self.list_paragraph)))
            if self.switch_Hide_current_page.isChecked():
                self.input_field.setPlaceholderText("{} / {}".format(self.bookmark + 1, len(self.list_paragraph)))
            else:
                self.input_field.setPlaceholderText("? / {}".format(len(self.list_paragraph)))
        else:
            self.all_pages_label.setText(("?"))
            if self.switch_Hide_current_page.isChecked():
                self.input_field.setPlaceholderText("{} / ?".format(self.bookmark + 1))
            else:
                self.input_field.setPlaceholderText("? / ?")

        self.settings.setValue("view_all_pages", self.switch_Hide_all_pages.isChecked())
    def event(self, event):
        # Проверяем, что произошло событие колеса мыши с зажатой клавишей Ctrl
        if event.type() == QEvent.Wheel and event.modifiers() == Qt.ControlModifier:
            font = self.text_browser.font()
            font_size = font.pointSize()
            self.spin_box.setValue(font_size)  # Устанавливаем новое значение для spinBox

        return super().event(event)

    def play_audio(self):
        print(inspect.currentframe().f_code.co_name)

        if self.stop_flag != None:
            # остановка генерации аудиофайла при переключении на следующее предложение
            self.stop_flag.set()

        self.stop_flag = threading.Event()
        thread = AudioThread(self.list_sentences[self.count], self.spin_box_playback_speed.value(), self.language_combo_original.currentData(), self.stop_flag, self.lock)
        thread.finished.connect(self.auto_go_next)
        thread.start()

    def center(self, state):
        print(inspect.currentframe().f_code.co_name)
        if state == Qt.Checked:
            self.text_browser.setAlignment(QtCore.Qt.AlignCenter)
        else:
            self.text_browser.setAlignment(QtCore.Qt.AlignLeft)

        self.output_paragraph()
        self.settings.setValue("center_setting", self.switch_center.isChecked())

        self.settings.setValue("slow_reading", self.spin_box_playback_speed.isChecked())
    def auto_play_func(self, state):
        print(inspect.currentframe().f_code.co_name)
        if state == Qt.Checked:
            if self.switch_audio.isChecked():
                self.play_audio()
        else:
            # Выключить аудио
            self.stop_flag.set()

        self.settings.setValue("auto_play", self.switch_auto_play.isChecked())
    def audio_switch(self, state):
        print(inspect.currentframe().f_code.co_name)

        if state == Qt.Checked:
            self.play_audio()
        else:
            # Выключить аудио
            self.stop_flag.set()

        self.settings.setValue("audio_enabled", self.switch_audio.isChecked())

    def google_Translate_to_trans_with_random_lang(self, text):
        """Переводит реальные абзацы, исходный язык неизвестен, реузльтат тоже
        Исходный - неизвестно, выход - родной
        """
        if self.language_combo_translate.currentData() == self.language_combo_translate:
            return text
        text_res = self.translator.translate(text, dest=self.language_combo_translate.currentData())
        return text_res

    def google_Translate_to_trans_with_eng(self, text):
        """функция используется для перевода с английского на родной"""
        if self.language_combo_translate.currentData() == "en":
            return text
        text_res = self.translator.translate(text, dest=self.language_combo_translate.currentData())
        return text_res

    def google_Translate_to_orig_with_Eng(self, text):
        """для перевода с английского на язык изучения"""
        if self.language_combo_original == "en":
            return text
        text_res = self.translator.translate(text, dest=self.language_combo_original.currentData())
        return text_res

    def google_Translate_init(self, text):
        """функция используется для перевода с английского на родной, что используется ТОЛЬКО ПРИ ЗАПУСКЕ"""
        if self.default_language_trans == "en":
            return text
        """Use default settings"""
        text_res = self.translator.translate(text, dest=self.default_language_trans)
        return text_res

    def next_button_clicked(self):
        print(inspect.currentframe().f_code.co_name)

        self.count += 1
        n = len(self.list_sentences)
        # если счетчик достиг конца книги и направление вперед, то переводим его в начало
        if self.count == n:
            self.count = 0
            if self.bookmark != len(self.list_paragraph) - 1:
                self.bookmark += 1
            self.formint_output_text()
        else:
            self.output_paragraph()


    def next_next_button_clicked(self):
        print(inspect.currentframe().f_code.co_name)

        if self.bookmark != len(self.list_paragraph) - 1:
            self.count = 0
            self.bookmark += 1

        self.formint_output_text()

    def prev_button_clicked(self):
        print(inspect.currentframe().f_code.co_name)

        if self.count == 0:
            if self.bookmark != 0:
                self.bookmark -= 1
            self.count = len(nltk.sent_tokenize(self.list_paragraph[self.bookmark])) - 1
            self.formint_output_text()
        else:
            self.count -= 1
            self.output_paragraph()

    def prev_prev_button_clicked(self):
        print(inspect.currentframe().f_code.co_name)

        self.count = 0
        if self.bookmark != 0:
            self.bookmark -= 1

        self.formint_output_text()

    def toggle_theme(self, output=True):
        print(inspect.currentframe().f_code.co_name)

        # определяем текущую тему
        if self.switch_night_mode.isChecked():
            # переключаем на темную тему, как в предыдущем примере
            QApplication.setStyle('fusion')
            palette = QPalette()

            palette.setColor(palette.Window, self.night_mod_colors[0])
            palette.setColor(palette.WindowText, self.night_mod_colors[1])
            palette.setColor(palette.Base, self.night_mod_colors[2])
            palette.setColor(palette.AlternateBase, self.night_mod_colors[3])
            palette.setColor(palette.ToolTipBase, self.night_mod_colors[4])
            palette.setColor(palette.ToolTipText, self.night_mod_colors[5])
            palette.setColor(palette.Text, self.night_mod_colors[6])
            palette.setColor(palette.Button, self.night_mod_colors[7])
            palette.setColor(palette.ButtonText, self.night_mod_colors[8])
            palette.setColor(palette.BrightText, self.night_mod_colors[9])
            palette.setColor(palette.Link, self.night_mod_colors[10])
            palette.setColor(palette.Highlight, self.night_mod_colors[11])
            palette.setColor(palette.HighlightedText, self.night_mod_colors[12])
            QApplication.setPalette(palette)

            self.settings.setValue("night_mod_colors", self.night_mod_colors)
        else:
            # переключаем на светлую тему
            QApplication.setStyle("windows")
            palette = QPalette()
            palette.setColor(palette.Window, self.day_mode_colors[0])
            palette.setColor(palette.WindowText, self.day_mode_colors[1])
            palette.setColor(palette.Base, self.day_mode_colors[2])
            palette.setColor(palette.AlternateBase, self.day_mode_colors[3])
            palette.setColor(palette.ToolTipBase, self.day_mode_colors[4])
            palette.setColor(palette.ToolTipText, self.day_mode_colors[5])
            palette.setColor(palette.Text, self.day_mode_colors[6])
            palette.setColor(palette.Button, self.day_mode_colors[7])
            palette.setColor(palette.ButtonText, self.day_mode_colors[8])
            palette.setColor(palette.BrightText, self.day_mode_colors[9])
            palette.setColor(palette.Link, self.day_mode_colors[10])
            palette.setColor(palette.Highlight, self.day_mode_colors[11])
            palette.setColor(palette.HighlightedText, self.day_mode_colors[12])
            QApplication.setPalette(palette)

            self.settings.setValue("day_mode_colors", self.day_mode_colors)
        if output:
            self.text_browser.setText("")  # clean output
            self.output_paragraph()

        self.settings.setValue("night_mode", self.switch_night_mode.isChecked())
    def changeFont_update(self, event):
        print(inspect.currentframe().f_code.co_name)

        if event.modifiers() == Qt.ControlModifier:  # Проверяем, что зажата клавиша Ctrl
            font = self.text_browser.font()
            font_size = font.pointSize()
            self.spin_box.setValue(font_size)  # Устанавливаем новое значение для spinBox

    def changeFont_valueChanged(self):
        print(inspect.currentframe().f_code.co_name)

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
        text = text.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
        # заменяем пробелы в конце предложений

        return text

    def out(self, text, end_space="\n"):
        if self.switch_night_mode.isChecked():
            self.text_browser.insertHtml('<span style="color: {};">{}</span>'.format(self.night_mod_colors[15].name(), self.filter_text(text + end_space)))
        else:
            self.text_browser.insertHtml('<span style="color: {};">{}</span>'.format(self.night_mod_colors[15].name(), self.filter_text(text + end_space)))
    def out_marker1(self, text, end_space="\n"):
        if self.switch_night_mode.isChecked():
            self.text_browser.insertHtml('<span style="color: {};">{}</span>'.format(self.night_mod_colors[13].name(), self.filter_text(text + end_space)))
        else:
            self.text_browser.insertHtml('<span style="color: {};">{}</span>'.format(self.day_mode_colors[13].name(), self.filter_text(text + end_space)))

    def out_marker2(self, text, end_space="\n"):
        if self.switch_night_mode.isChecked():
            self.text_browser.insertHtml('<span style="color: {};">{}</span>'.format(self.night_mod_colors[14].name(), self.filter_text(text + end_space)))
        else:
            self.text_browser.insertHtml('<span style="color: {};">{}</span>'.format(self.day_mode_colors[14].name(), self.filter_text(text + end_space)))

    def formint_output_text(self):
        print(inspect.currentframe().f_code.co_name)

        self.hide_curren_and_all_page()

        self.currentParagraph = self.list_paragraph[self.bookmark]

        self.list_sentences = nltk.sent_tokenize(self.currentParagraph)

        self.text_trans = self.google_Translate_to_trans_with_random_lang(self.currentParagraph)

        self.list_sentences_trans = nltk.sent_tokenize(self.text_trans)

        self.output_paragraph()

    def output_paragraph(self):
        print(inspect.currentframe().f_code.co_name)

        self.text_browser.setText("")  # clean output

        if self.currentParagraph[0] == "\n":
            """Обработка исключения, когда вначале лишний перевод строки
            Указывает на смену темы"""
            if not self.switch_center.isChecked():
                self.out("\t", end_space="")
            self.out_marker2("***", "\n\n")

        if self.bookmark == 0:
            if not self.switch_center.isChecked():
                self.out("\t", "")
            self.out_marker2(self.google_Translate_to_orig_with_Eng("Beginning of text"))

        """Вывод параграфа и перевода, с выделением предложения"""

        if not self.switch_center.isChecked():
            self.out("\t", "")

        for i in range(len(self.list_sentences)):
            if self.list_sentences[i][0] == "\n":
                self.list_sentences[i] = self.list_sentences[i][1::]

            if self.count == i:
                self.out_marker1(self.list_sentences[i], " ")
            else:
                self.out(self.list_sentences[i], " ")

        self.out("\n")

        if not self.switch_center.isChecked():
            self.out("\t", "")

        for i in range(len(self.list_sentences_trans)):
            if self.count == i:
                self.out_marker1(self.list_sentences_trans[i], " ")
            else:
                self.out(self.list_sentences_trans[i], " ")



        if self.bookmark == len(self.list_paragraph) - 1:
            self.out("\n")

            if not self.switch_center.isChecked():
                self.out("\t", "")
            self.out_marker2(self.google_Translate_to_orig_with_Eng("End of text"))

        if self.switch_audio.isChecked():
            self.play_audio()

        if self.active_mode == "book" and self.last_book in self.bookmarks_book:
            self.bookmarks_book[self.last_book] = (self.bookmark, self.count)
            self.settings.setValue("bookmarks_book", self.bookmarks_book)

        elif self.active_mode == "song" and self.last_song in self.bookmarks_song:
            self.bookmarks_song[self.last_song] = (self.bookmark, self.count)
            self.settings.setValue("bookmarks_song", self.bookmarks_song)

        if self.switch_center.isChecked():
            self.text_browser.setAlignment(QtCore.Qt.AlignCenter)
        else:
            self.text_browser.setAlignment(QtCore.Qt.AlignLeft)

    def save_settings(self):
        print(inspect.currentframe().f_code.co_name)

        # Сохранение настроек
        self.settings.setValue("cache_Music", self.cache_Music),
        self.settings.setValue("fontSize", self.text_browser.font().pointSize())
        self.settings.setValue("window_geometry_x", self.geometry().x())
        self.settings.setValue("window_geometry_y", self.geometry().y())
        self.settings.setValue("window_geometry_width", self.geometry().width())
        self.settings.setValue("window_geometry_height", self.geometry().height())

    def closeEvent(self, event):
        print(inspect.currentframe().f_code.co_name)

        # вызываем метод save() перед закрытием окна
        self.save_settings()
        self.translator.save_cache_to_settings(self)

        # вызываем родительский метод closeEvent()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    my_program = MyWindow()

    my_program.show()
    sys.exit(app.exec_())
