import os
from random import randint
from time import sleep

#import pyttsx3
# simple tts, poor quality

from googletrans import Translator
# pip install googletrans==3.1.0a0

from gtts import gTTS
# https://github.com/pndurette/gTTS

from playsound import playsound
# pip install playsound==1.2.2

import pygame

def out_red(text):
    print("\033[31m{}\033[37m".format(text), end="")


def out_yellow(text):
    print("\033[33m{}\033[37m".format(text), end="")


def out_blue(text):
    print("\033[34m{}\033[37m".format(text), end="")


#engine = pyttsx3.init()
tts_play = True


# чтение файла (указан путь к примеру файлу txt)
with open('Cambias James. A Darkling Sea - royallib.com.txt', encoding='windows-1251') as f:
    text = f.read()

list_paragraph = text.split("\n\n")
list_paragraph = [x for x in list_paragraph if x]
with open('bookmark.txt', encoding='windows-1251') as f:
    bookmark = int(f.read())

os.system('cls||clear')


while True:
    if bookmark == len(list_paragraph):
        break

    currentParagraph = list_paragraph[bookmark]
    translator = Translator()
    transParagraph = translator.translate(currentParagraph, dest="ru")
    text_trans = transParagraph.text


    index_sentence = []
    for i in range(len(currentParagraph)):
        if currentParagraph[i]=="." or currentParagraph[i]=="?" or currentParagraph[i]=="!":
            index_sentence.append(i)

    index_sentence_trans = []
    for i in range(len(text_trans)):
        if text_trans[i]=="." or text_trans[i]=="?" or text_trans[i]=="!":
            index_sentence_trans.append(i)

    for i in range(len(index_sentence)):
        """Вывод параграфа и перевода, с выделением предложения"""

        if i==0:
            out_yellow(currentParagraph[0:index_sentence[i]+1])
            print(currentParagraph[index_sentence[i]+1::], end="")
        else:
            print(currentParagraph[0:index_sentence[i-1]+1], end="")
            out_yellow(currentParagraph[index_sentence[i-1]+1:index_sentence[i]+1])
            print(currentParagraph[index_sentence[i]+1::], end="")

        print("\n")

        if i==0:
            out_yellow(text_trans[0:index_sentence_trans[i]+1])
            print(text_trans[index_sentence_trans[i]+1::], end="")
        else:
            try:
                print(text_trans[0:index_sentence_trans[i-1]+1], end="")
                out_yellow(text_trans[index_sentence_trans[i-1]+1:index_sentence_trans[i]+1])
                print(text_trans[index_sentence_trans[i]+1::], end="")
            except:
                pass

        print("\n")

        if tts_play:
            if i==0:
                #engine.say(currentParagraph[0:index_sentence[i]+1])
                tts = gTTS(currentParagraph[0:index_sentence[i]+1])
            else:
                #engine.say(currentParagraph[index_sentence[i-1]+1:index_sentence[i]+1])
                tts = gTTS(currentParagraph[index_sentence[i-1]+1:index_sentence[i]+1])
            tts.save('sentence.mp3')
            #engine.runAndWait()

            pygame.init()
            song = pygame.mixer.Sound('sentence.mp3')
            song.play()

        inpExit = input("")

        if tts_play:
            pygame.quit()

        os.system('cls||clear')
        with open('bookmark.txt', 'w') as file:
            file.write(str(bookmark))
        if inpExit != "":
            try:
                bookmark+=int(inpExit)
            except:
                exit()

    bookmark += 1