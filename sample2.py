from PySide2.QtWidgets import QDialog, QPushButton, QLineEdit, QListView, QVBoxLayout, QHBoxLayout, QApplication
from PySide2.QtCore import QAbstractListModel, Qt
from PySide2.QtGui import QImage

import sys
import json

tick = QImage('tick.png')

class TodoWindow(QDialog):
    def __init__(self):
        super(TodoWindow, self).__init__()

        main_layout = QVBoxLayout(self)

        self.view = QListView()
        main_layout.addWidget(self.view)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        self.delete_button = QPushButton("Delete")
        self.complete_button = QPushButton("Complete")
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.complete_button)

        self.add_todo_field = QLineEdit()
        main_layout.addWidget(self.add_todo_field)

        self.add_todo_button = QPushButton("Add Todo")
        main_layout.addWidget(self.add_todo_button)
        # Idáig csak a widget elemek vannak definiálva

        # model példányosítása
        self.model = TodoModel(todos=[])
        # model hozzárendelése a view-hoz
        self.view.setModel(self.model)
        self.add_todo_button.pressed.connect(self.add)
        self.delete_button.pressed.connect(self.delete)
        self.complete_button.pressed.connect(self.complete)

    def add(self):
        text = self.add_todo_field.text()
        if text:
            self.model.todos.append((False, text))
            self.model.layoutChanged.emit()
            self.add_todo_field.setText("")

        self.model.save()

    def delete(self):
        indexes = self.view.selectedIndexes()
        if indexes:
            index = indexes[0]
            # print(index.row())
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            self.view.clearSelection()

        self.model.save()

    def complete(self):
        indexes = self.view.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            if not status:
                self.model.todos[row] = (True, text)
            else:
                self.model.todos[row] = (False, text)
            self.model.dataChanged.emit(index, index)
            self.view.clearSelection()

            self.model.save()


# Saját model leszármaztatása
class TodoModel(QAbstractListModel):
    def __init__(self, *args, todos=None, **kvargs):
        super(TodoModel, self).__init__(*args, **kvargs)
        self.todos = todos or []
        self.load()

    # Adatok: listából kivesszük az elemeket (status, text). A return a megjelenített érték, jelen esetben a text
    def data(self, index, role):
        if role == Qt.DisplayRole:
            # print(index.row())
            _, text = self.todos[index.row()]
            return text

        if role == Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return tick
    # Visszaadja az elemek számát (ha pl. -1, akkor egyel kevesebbet jelenít meg
    def rowCount(self, index):
        return len(self.todos)

    def save(self):
        with open('data.db', 'w') as f:
            data = json.dump(self.todos, f)

    def load(self):
        try:
            with open('data.db', 'r') as f:
                self.todos = json.load(f)
        except Exception:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TodoWindow()
    win.show()
    app.exec_()