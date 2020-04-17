from datetime import datetime
from database.db import MysqlClient
from PySide2.QtGui import QColor, QIcon
from PySide2.QtWidgets import QMainWindow, QTableView, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QAbstractItemView
from PySide2.QtCore import QAbstractTableModel, Qt
from operator import itemgetter

import sys


class TableModel(QAbstractTableModel):
    """ Az AbstractModel közvetlenül nem példányosítható. Elöször saját class-t származtatunk, majd ezt tudjuk példányosítani.
    Ennél a view típusnál minimum 3 metódust kell újradefiniálni:
    data: Honnan, és hogyan veszi az adatokat
    rowCount: Hány sora lesz a táblázatnak (az adatok alapján)
    columnCount: Hány oszlopa lesz a táblázatnak (az adatok alapján)"""
    def __init__(self, table):
        super(TableModel, self).__init__()
        self.table = table
        self.client = MysqlClient()
        self.load_data(self.table)

    def load_data(self, table):
        self.adatok = self.client.get_all(table)
        self._data = self.adatok[0]
        self.fejlec = self.adatok[1]

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        if order == Qt.SortOrder.AscendingOrder:
            self._data = sorted(self._data, key=itemgetter(column), reverse=False)
        else:
            self._data = sorted(self._data, key=itemgetter(column), reverse=True)
        self.layoutChanged.emit()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.fejlec[section])

    def data(self, index, role):
        """ index: melyik adatról van szó.
            role: milyen feladatot kezelünk le. Lehetséges:
                DisplayRole
                BackgoundRole
                CheckStateRole
                DecorationRole
                FontRole
                TextAligmentRole
                ForegrounfRole"""
        COLORS = ['#053061', '#2166ac', '#4393c3', '#92c5de', '#d1e5f0', '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d', '#b2182b', '#67001f']
        value = self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            # if isinstance(value, datetime):
            #     return value.strftime("%Y-%m-%d")
            #
            # if isinstance(value, float):
            #     return "%.2f" % value
            #
            # if isinstance(value, str):
            #     return'"%s"' % value

            return value

        # if role == Qt.BackgroundRole and index.column() == 1:
        #     return QColor('lightblue')
        #
        # if role == Qt.TextAlignmentRole:
        #     if isinstance(value, int) or isinstance(value, float):
        #         return Qt.AlignVCenter and Qt.AlignCenter
        #
        # if role == Qt.ForegroundRole:
        #     if (isinstance(value, int) or isinstance(value, float)) and value < 0:
        #         return QColor('red')
        #
        # # if role == Qt.BackgroundRole:
        # #     if (isinstance(value, int) or isinstance(value, float)):
        # #         value = int(value)  # Convert to integer for indexing.
        # #
        # #         # Limit to range -5 ... +5, then convert to 0..10
        # #         value = max(-5, value)  # values < -5 become -5
        # #         value = min(5, value)  # valaues > +5 become +5
        # #         value = value + 5  # -5 becomes 0, +5 becomes + 10
        # #
        # #         return QColor(COLORS[value])
        #
        # if role == Qt.DecorationRole:
        #     if isinstance(value, datetime):
        #         return QIcon('calendar.png')
        #
        #     if isinstance(value, bool):
        #         if value:
        #             return QIcon('tick.png')
        #
        #         return QIcon('cross.png')
        #
        #     if (isinstance(value, int) or isinstance(value, float)):
        #         value = int(value)  # Convert to integer for indexing.
        #         # Limit to range -5 ... +5, then convert to 0..10
        #         value = max(-5, value)  # values < -5 become -5
        #         value = min(5, value)  # valaues > +5 become +5
        #         value = value + 5  # -5 becomes 0, +5 becomes + 10
        #         return QColor(COLORS[value])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def rekord_torles(self, unique_value):
        self.unique_value = unique_value
        self.client.delete_rekord(self.table, self.unique_value)


class MainWindow(QMainWindow):
    """ Példányosítunk egy view-t.
        Pépldányosítunk egy model-t.
        Hozzárendeljük a model-t a view-hoz (setModel)"""
    def __init__(self):
        super(MainWindow, self).__init__()
        widget = QWidget()
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.client = MysqlClient()
        self.table = QTableView()
        # todo: a megjelenített tábla neve
        self.table_name = "teszt2"

        main_layout.addWidget(self.table)
        self.model = TableModel(self.table_name)

        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)

        gomb_layout = QHBoxLayout()
        main_layout.addLayout(gomb_layout)

        self.delete_button = QPushButton("Delete Record")
        gomb_layout.addWidget(self.delete_button)

        self.add_button = QPushButton("Add New Record")
        gomb_layout.addWidget(self.add_button)

        self.modify_button = QPushButton("Modify Record")
        gomb_layout.addWidget(self.modify_button)

        self.delete_button.pressed.connect(self.delete)
        self.add_button.pressed.connect(self.add)
        self.modify_button.pressed.connect(self.modify)

    def delete(self):
        index = self.table.selectedIndexes()[0]

        self.client.cursor.execute(f"describe {self.table_name}")
        all_rows2 = self.client.cursor.fetchall()
        for row in all_rows2:
            if 'PRI' in row:
                self.id_name = row[0]
                for i in range(0, len(self.model.fejlec)):
                    if self.id_name == self.model.fejlec[i]:
                        torlendo_ertek = self.model._data[index.row()][i]

        del self.model._data[index.row()]
        self.model.layoutChanged.emit()
        self.model.rekord_torles(torlendo_ertek)

    def add(self):
        pass

    def modify(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()