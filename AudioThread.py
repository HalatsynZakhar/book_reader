import inspect
import threading
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
        self.lock.acquire()  # запрос блокировки
        tts = gTTS(self.sentence, slow=True, lang=self.lang)

        tts.save('sentence.mp3')

        p = vlc.MediaPlayer("sentence.mp3")
        p.set_rate(self.speed)

        if self.stop_flag.is_set():
            print("AudioThread: {} early finish".format(threading.current_thread()))
        else:
            p.play()
            # Ожидаем, пока медиа-контент не закончится или не будет установлен флаг остановки
            while True:
                stop = self.stop_flag.is_set()
                end = p.get_state() == vlc.State.Ended
                if stop:
                    p.stop()
                    break
                if end:
                    p.stop()
                    if self.go_next:
                        self.finished.emit()
                    break

        self.lock.release()  # освобождение блокировки
        print("AudioThread: {} finish".format(threading.current_thread()))
