import os
import sys

import pygame
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLabel, QSpinBox, QLineEdit
from googletrans import Translator
from gtts import gTTS


class MyWindow(QWidget):
    def __init__(self, path_to_book, tts_play):
        super().__init__()

        # создаем главный вертикальный лейаут
        main_layout = QVBoxLayout()

        # создаем textBrowser и добавляем его в вертикальный лейаут
        self.text_browser = QTextBrowser()
        main_layout.addWidget(self.text_browser)

        # создаем горизонтальный лейаут
        horizontal_layout = QHBoxLayout()

        # создаем кнопку "previous" и добавляем ее в горизонтальный лейаут
        previous_button = QPushButton("previous")
        horizontal_layout.addWidget(previous_button)

        # создаем label "Font size" и добавляем его в горизонтальный лейаут
        font_size_label = QLabel("Font size")
        horizontal_layout.addWidget(font_size_label)

        # создаем spinBox и добавляем его в горизонтальный лейаут
        self.spin_box = QSpinBox()
        self.spin_box.setValue(36)
        horizontal_layout.addWidget(self.spin_box)

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

        # создаем кнопку "next" и добавляем ее в горизонтальный лейаут
        next_button = QPushButton("next")
        horizontal_layout.addWidget(next_button)

        # добавляем горизонтальный лейаут в вертикальный лейаут
        main_layout.addLayout(horizontal_layout)

        # устанавливаем вертикальный лейаут в качестве главного лейаута окна
        self.setLayout(main_layout)


        # чтение файла (указан путь к примеру файлу txt)
        with open(path_to_book, encoding='windows-1251') as f:
            text = f.read()

        list_paragraph = text.split("\n\n")
        list_paragraph = [x for x in list_paragraph if x]
        with open('bookmark.txt', encoding='windows-1251') as f:
            bookmark = int(f.read())
        self.count = 0
        self.bookmark = bookmark
        self.tts_play = tts_play
        self.text = text
        self.list_paragraph = list_paragraph
        self.translator = Translator()

        if self.tts_play:
            pygame.init()


        next_button.clicked.connect(self.formint_output_text)
        self.spin_box.valueChanged.connect(self.changeFont)


        if self.tts_play:
            pygame.quit()

        self.formint_output_text()

    def changeFont(self):
        num = self.spinBox.value()
        font = QFont()
        font.setPointSize(num)
        self.text_browser.setFont(font)
    def out_red(self, text):
        self.text_browser.append('<span style="color: #ff0000;">{}</span>'.format(text))

    def out(self, text):
        self.text_browser.append(text)

    def out_yellow(self, text):
        self.text_browser.append('<span style="color: #ffff00;">{}</span>'.format(text))


    def out_blue(self, text):
        self.text_browser.append('<span style="color: #0000ff;">{}</span>'.format(text))

    def formint_output_text(self):


        if self.tts_play:
            pygame.quit()

        if self.bookmark == len(self.list_paragraph):
            exit()

        currentParagraph = self.list_paragraph[self.bookmark]

        self.text_browser.setText("") # clean output

        if currentParagraph[0] == "\n":
            """Обработка исключения, когда вначале лишний перевод строки
            Указывает на смену темы"""
            currentParagraph = currentParagraph[1::]
            self.out_blue("***\n")

        transParagraph = self.translator.translate(currentParagraph, dest="ru")
        text_trans = transParagraph.text

        index_sentence = []
        for i in range(len(currentParagraph)):
            if currentParagraph[i] in [".", "?", "!", "…"]:
                if i >= 2:
                    if currentParagraph[i - 2:i] == "Dr":
                        """
                        точка обозначает сокращение, не конец предложения. В переводе данная точка отсутствует.
                        Из-за этого несовпадение количества предложений и неккоректная синхронизация
                        """
                        continue
                if i >= 1:
                    if currentParagraph[i - 1] == ".":
                        continue
                index_sentence.append(i)

        if len(index_sentence) == 0:
            """обработка параграфов в несколько слов (Заголовков), когда отсутствуют разделители впринципе"""
            index_sentence.append(len(currentParagraph) - 1)
        elif (len(currentParagraph) - 1) - (index_sentence[-1]) >= 2:
            """Обработка исключения, когда строка кончается не данными символами .?!... 
            В таком случае окончание фиксируется по последнему симвлу """
            index_sentence.append(len(currentParagraph) - 1)

        index_sentence_trans = []
        for i in range(len(text_trans)):
            if text_trans[i] in [".", "?", "!", "…"]:
                if i >= 1:
                    if text_trans[i - 1] == ".":
                        continue
                index_sentence_trans.append(i)

        if len(index_sentence_trans) == 0:
            """обработка параграфов в несколько слов (Заголовков), когда отсутствуют разделители впринципе"""
            index_sentence_trans.append(len(text_trans) - 1)
        if (len(text_trans) - 1) - (index_sentence_trans[-1]) >= 2:
            """Обработка исключения, когда строка кончается не данными символами .?!... 
            В таком случае окончание фиксируется по последнему симвлу """
            index_sentence_trans.append(len(text_trans) - 1)


        if self.count>=len(index_sentence):
            self.count = 0
            self.bookmark += 1
        else:
            self.output_paragraph(self.count, currentParagraph, index_sentence, text_trans,
                                  index_sentence_trans)
            self.count += 1




    def output_paragraph(self, i, currentParagraph, index_sentence, text_trans, index_sentence_trans):

        """Вывод параграфа и перевода, с выделением предложения"""

        if i == 0:
            self.out_yellow(currentParagraph[0:index_sentence[i] + 1])
            self.out(currentParagraph[index_sentence[i] + 1::])
        else:
            self.out(currentParagraph[0:index_sentence[i - 1] + 1])
            self.out_yellow(currentParagraph[index_sentence[i - 1] + 1:index_sentence[i] + 1])
            self.out(currentParagraph[index_sentence[i] + 1::])

        self.out("\n")

        if i == 0:
            self.out_yellow(text_trans[0:index_sentence_trans[i] + 1])
            self.out(text_trans[index_sentence_trans[i] + 1::])
        else:
            try:
                text1 = text_trans[0:index_sentence_trans[i - 1] + 1]
                text2 = text_trans[index_sentence_trans[i - 1] + 1:index_sentence_trans[i] + 1]
                text3 = text_trans[index_sentence_trans[i] + 1::]

                self.out(text1)
                self.out_yellow(text2)
                self.out(text3)
            except:
                self.out(text_trans)

        self.out("\n")

        if self.tts_play:
            pygame.init()
        if self.tts_play:
            if i == 0:
                # engine.say(currentParagraph[0:index_sentence[i]+1])
                tts = gTTS(currentParagraph[0:index_sentence[i] + 1], slow=True)
            else:
                # engine.say(currentParagraph[index_sentence[i-1]+1:index_sentence[i]+1])
                tts = gTTS(currentParagraph[index_sentence[i - 1] + 1:index_sentence[i] + 1], slow=True)
            tts.save('sentence.mp3')
            # engine.runAndWait()


            song = pygame.mixer.Sound('sentence.mp3')
            song.play()


        os.system('cls||clear')
        with open('bookmark.txt', 'w') as file:
            file.write(str(self.bookmark))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle('Fusion')  # задаем стиль приложения
    window = MyWindow("Cambias James. A Darkling Sea - royallib.com.txt", True)

    # добавляем настройки для темной темы
    palette = window.palette()
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
    app.setPalette(palette)



    window.show()
    sys.exit(app.exec_())