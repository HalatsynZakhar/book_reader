class MyTextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_font_size = 1
        self.max_font_size = 999

    def wheelEvent(self, event):
        if event.modifiers() & QtCore.Qt.ControlModifier:
            font = self.currentFont()
            font_size = font.pointSize()
            if event.angleDelta().y() > 0:
                font_size += 1
            else:
                font_size -= 1
            font_size = max(self.min_font_size, min(self.max_font_size, font_size))
            font.setPointSize(font_size)
            self.setFont(font)
        else:
            super().wheelEvent(event)
