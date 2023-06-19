from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout

class BookmarkDialog(QDialog):
    def __init__(self, myWindow, current_mode):
        super().__init__()
        self.myWindow = myWindow
        self.current_mode = current_mode
        if current_mode=="book":
            self.last = self.myWindow.last_book
            self.bookmarks = self.myWindow.bookmarks_book
        if current_mode=="song":
            self.last = self.myWindow.last_song
            self.bookmarks = self.myWindow.bookmarks_song

        if self.current_mode == "book":
            self.setWindowTitle(self.myWindow.translate_history_dialog[3])
        if self.current_mode == "song":
            self.setWindowTitle(self.myWindow.translate_history_dialog[4])

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([self.myWindow.translate_history_dialog[0], self.myWindow.translate_history_dialog[1]])
        self.table.setRowCount(len(self.bookmarks) + 1)
        for i, bookmark in enumerate(sorted(self.bookmarks.keys())):
            if self.current_mode == "book":
                item = QTableWidgetItem(bookmark)
            if self.current_mode == "song":
                item = QTableWidgetItem(" ".join(bookmark))
            self.table.setItem(i, 0, item)

            if bookmark != self.last:
                delete_button = QPushButton(self.myWindow.translate_history_dialog[1])
                delete_button.clicked.connect(lambda _, row=i: self.delete_bookmark(row))
                self.table.setCellWidget(i, 1, delete_button)
        delete_button = QPushButton(self.myWindow.translate_history_dialog[2])
        delete_button.clicked.connect(self.delete_all)
        self.table.setCellWidget(len(self.bookmarks), 1, delete_button)

        self.table.resizeColumnsToContents() # установка ширины ячеек по содержимому

        width = self.table.horizontalHeader().length() + self.table.verticalHeader().width() + 50
        height = self.table.verticalHeader().length() + self.table.horizontalHeader().height() + 50
        self.resize(width, height)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def delete_all(self):
        for key, value in list(self.bookmarks.items()):
            if key != self.last:
                self.bookmarks.pop(key)
        self.accept()
    def delete_bookmark(self, row):
        current = self.table.item(row, 0).text()
        self.table.removeRow(row)

        if self.current_mode=="book":
            if current != self.last:
                for key, value in list(self.bookmarks.items()):
                    if key == current:
                        self.bookmarks.pop(key)

        if self.current_mode=="song":
            if current != " ".join(self.last):
                for key, value in list(self.bookmarks.items()):
                    if " ".join(key) == current:
                        self.bookmarks.pop(key)
    def exec_(self):
        if self.current_mode == "book":
            for i in range(self.table.rowCount() -1):
                if self.table.item(i, 0).text() == self.last:
                    self.table.selectRow(i)
                    break
        if self.current_mode == "song":
            for i in range(self.table.rowCount() -1):
                if self.table.item(i, 0).text() == " ".join(self.last):
                    self.table.selectRow(i)
                    break


        super().exec_()