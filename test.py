import sys

import uint as uint
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QIODevice
from csv import writer

import os
from random import randint
from time import sleep

from PyQt5.QtGui import QColor, QFont
# import pyttsx3
# simple tts, poor quality

from googletrans import Translator
# pip install googletrans==3.1.0a0

from gtts import gTTS
# https://github.com/pndurette/gTTS

from playsound import playsound
# pip install playsound==1.2.2

import pygame


class Window:
    def __init__(self, path_to_book, tts_play):
        super().__init__()

        self.count = 0
        self.app = QtWidgets.QApplication([])
        self.ui = uic.loadUi("design.ui")
        self.ui.setWindowTitle("SerialGUI")

        self.ui.setStyleSheet("background-color: #000000; color: #ffffff;")

        # чтение файла (указан путь к примеру файлу txt)
        with open(path_to_book, encoding='windows-1251') as f:
            text = f.read()

        list_paragraph = text.split("\n\n")
        list_paragraph = [x for x in list_paragraph if x]
        with open('bookmark.txt', encoding='windows-1251') as f:
            bookmark = int(f.read())

        self.bookmark = bookmark
        self.tts_play = tts_play
        self.text = text
        self.list_paragraph = list_paragraph
        self.translator = Translator()

        if self.tts_play:
            pygame.init()


        self.ui.nextButton.clicked.connect(self.formint_output_text)
        self.ui.spinBox.valueChanged.connect(self.changeFont)


        self.ui.show()
        self.app.exec()
        if self.tts_play:
            pygame.quit()
    def changeFont(self):
        num = self.ui.spinBox.value()
        font = QFont()
        font.setPointSize(num)
        self.ui.textBrowser.setFont(font)
    def out_red(self, text):
        self.ui.textBrowser.append('<span style="color: #ff0000;">{}</span>'.format(text))

    def out(self, text):
        self.ui.textBrowser.append(text)

    def out_yellow(self, text):
        self.ui.textBrowser.append('<span style="color: #ffff00;">{}</span>'.format(text))


    def out_blue(self, text):
        self.ui.textBrowser.append('<span style="color: #0000ff;">{}</span>'.format(text))

    def formint_output_text(self):


        if self.tts_play:
            pygame.quit()


        if self.bookmark == len(self.list_paragraph):
            exit()

        currentParagraph = self.list_paragraph[self.bookmark]

        self.ui.textBrowser.setText("") # clean output

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

a_window = Window("Cambias James. A Darkling Sea - royallib.com.txt", True)
