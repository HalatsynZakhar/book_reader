import os

from gtts import gTTS
# https://github.com/pndurette/gTTS

from playsound import playsound
# pip install playsound==1.2.2

tts = gTTS("""“This changes""")
tts.save('hello.mp3')

for i in range(10):
    playsound('hello.mp3')

os.remove('hello.mp3')