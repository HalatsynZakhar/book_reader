import threading
import pygame
from gtts import gTTS

class AudioThread(threading.Thread):
    def __init__(self, sentence, slow, lang, stop_flag, lock):
        threading.Thread.__init__(self)
        self.sentence = sentence
        self.stop_flag = stop_flag
        self.slow = slow
        self.lang = lang
        self.lock = lock
    def run(self):
        tts = gTTS(self.sentence, slow=self.slow, lang=self.lang, )
        self.lock.acquire() # запрос блокировки
        tts.save('sentence.mp3')
        song = pygame.mixer.Sound('sentence.mp3')
        song.play()
        self.lock.release() # освобождение блокировки
        while not (not pygame.mixer.get_busy() or self.stop_flag.is_set()):
            pass
        pygame.mixer.stop()