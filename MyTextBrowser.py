from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QTextBrowser
from qtpy import QtGui, QtCore


class MyTextBrowser(QTextBrowser):
    def __init__(self, parent=None, my_window=None):
        super().__init__(parent)
        self.min_font_size = 1
        self.max_font_size = 999
        self.myWindow = my_window
        self.select = False

        pixmap = QPixmap('img/left.png')
        self.left_cursor = QCursor(pixmap)

        pixmap = QPixmap('img/right.png')
        self.right_cursor = QCursor(pixmap)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            font = self.currentFont()
            font_size = font.pointSize()
            if event.angleDelta().y() > 0:
                font_size += 1
            else:
                font_size -= 1
            font_size = max(self.min_font_size, min(self.max_font_size, font_size))
            font.setPointSize(font_size)
            self.setFont(font)

        super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            font = self.currentFont()
            font_size = font.pointSize()
            if event.key() == Qt.Key_Plus:
                font_size += 1
            elif event.key() == Qt.Key_Minus:
                font_size -= 1
            font_size = max(self.min_font_size, min(self.max_font_size, font_size))
            font.setPointSize(font_size)
            self.setFont(font)

        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_button_pressed = True
            self.left_button_down_time = event.timestamp()
            self.left_button_down_pos = event.pos()
        elif event.button() == Qt.RightButton:
            self.right_button_pressed = True
            self.right_button_down_time = event.timestamp()
            self.right_button_down_pos = event.pos()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        cursor = self.myWindow.text_browser.textCursor()
        if self.myWindow.switch_use_cursor.isChecked():
            #if self.myWindow.switch_use_cursor.isChecked() and not self.textCursor().hasSelection():
            if not cursor.hasSelection():
                if self.select:
                    """Если до этого был выбран текст, то игнорировать нажатие"""
                    self.select = False
                    """Игнорирование только один раз, далее стандартно"""
                else:
                    if event.button() == Qt.LeftButton:
                        if (event.timestamp() - self.left_button_down_time) < 500 and \
                           (event.pos() - self.left_button_down_pos).manhattanLength() < 5:
                            # Short left click
                            if event.x() < self.width() / 2:
                                """Короткое нажатие ЛКМ слева"""
                                self.myWindow.prev_button_clicked()
                            else:
                                """Короткое нажатие ЛКМ справа"""
                                self.myWindow.next_button_clicked()
                        else:
                            # Long left click
                            if event.x() < self.width() / 2:
                                self.myWindow.prev_prev_button_clicked()
                            else:
                                self.myWindow.next_next_button_clicked()

                    self.left_button_pressed = False

                """
                elif event.button() == QtCore.Qt.RightButton:
                    if (event.timestamp() - self.right_button_down_time) < 500 and \
                       (event.pos() - self.right_button_down_pos).manhattanLength() < 5:
                        # Short right click
                        if event.x() < self.width() / 2:
                            print("5")
                        else:
                            print("6")
                    else:
                        # Long right click
                        if event.x() < self.width() / 2:
                            print("7")
                        else:
                            print("8")
                    self.right_button_pressed = False
                """
            else:
                """Фиксируем что было выделение текста для игнорирование короткого нажатия"""
                self.select = True
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.myWindow.switch_use_cursor.isChecked():
            if event.x() < self.width() / 2:
                self.viewport().setCursor(self.left_cursor)
            else:
                self.viewport().setCursor(self.right_cursor)
        else:
            self.viewport().setCursor(QCursor(Qt.ArrowCursor))

        super().mouseMoveEvent(event)