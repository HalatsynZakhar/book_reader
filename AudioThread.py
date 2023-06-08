import threading
import vlc
from PyQt5.QtCore import pyqtSignal, QObject
from gtts import gTTS


class AudioThread(threading.Thread, QObject):
    finished = pyqtSignal()

    def __init__(self, instance, sentence, speed, lang, stop_flag, lock):
        super(AudioThread, self).__init__()
        QObject.__init__(self)
        self.instance = instance
        self.sentence = sentence
        self.stop_flag = stop_flag
        self.speed = speed
        self.lang = lang
        self.lock = lock

    def run(self):
        tts = gTTS(self.sentence, slow=True, lang=self.lang)
        self.lock.acquire()  # запрос блокировки
        tts.save('sentence.mp3')
        p = self.instance.MediaPlayer("sentence.mp3")
        p.set_rate(self.speed)
        p.play()
        self.lock.release()  # освобождение блокировки
        # Ожидаем, пока медиа-контент не закончится или не будет установлен флаг остановки
        while not (p.get_state() == vlc.State.Ended or self.stop_flag.is_set()):
            pass
        p.stop()
        if not self.stop_flag.is_set():
            self.finished.emit()
