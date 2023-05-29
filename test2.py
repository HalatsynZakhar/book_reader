import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLabel, QSpinBox, QLineEdit


class MyWindow(QWidget):
    def __init__(self):
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





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())