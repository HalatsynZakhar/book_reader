import inspect
import threading
from time import sleep

import vlc
from PyQt5.QtCore import pyqtSignal, QObject
from gtts import gTTS


class AudioThread(threading.Thread, QObject):
    finished = pyqtSignal()

    def __init__(self, sentence, speed, lang, stop_flag,
                 lock,
                 go_next):
        super(AudioThread, self).__init__()
        QObject.__init__(self)
        self.sentence = sentence
        self.stop_flag = stop_flag
        self.speed = speed
        self.lang = lang
        self.lock = lock
        self.go_next = go_next

    def run(self):
        print("AudioThread: {} start".format(threading.current_thread()))
        try:
            tts = gTTS(self.sentence, slow=True, lang=self.lang)

            if self.stop_flag.is_set():
                print("AudioThread: {} step1 finish".format(threading.current_thread()))
                return
        except:
            return

        self.lock.acquire()  # запрос блокировки

        tts.save('sentence.mp3')
        p = vlc.MediaPlayer("sentence.mp3")

        self.lock.release()  # освобождение блокировки

        if self.stop_flag.is_set():
            print("AudioThread: {} step2 finish".format(threading.current_thread()))
            return

        p.set_rate(self.speed)

        p.play()
        # Ожидаем, пока медиа-контент не закончится или не будет установлен флаг остановки
        while True:
            if self.stop_flag.is_set():
                p.stop()
                print("AudioThread: {} step3 finish".format(threading.current_thread()))
                return
            if p.get_state() == vlc.State.Ended:
                p.stop()
                if self.go_next:
                    self.finished.emit()
                print("AudioThread: {} step4 finish".format(threading.current_thread()))
                return
            sleep(0.1)

