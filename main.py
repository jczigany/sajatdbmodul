import sys
from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication, QTableView, QMessageBox
from PySide2.QtSql import QSqlDatabase, QSqlTableModel
from PySide2 import QtCore
import MySQLdb as mdb


class SportsmenView(QTableView):
    def __init__(self):
        super(SportsmenView, self).__init__()

        self.setSortingEnabled(True)
        self.model = QSqlTableModel()

        self.initializeModel()
        self.setModel(self.model)

    def rowCountChanged(self, oldCount:int, newCount:int):
        print(f'Eredeti sorok száma: {oldCount}, ús sorok száma: {newCount}')


    def initializeModel(self):
        self.model.setTable('teszt')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Azonosító")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Vezetéknév")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Utónév")


class SportsmenDialog(QDialog):
    def __init__(self):
        super(SportsmenDialog, self).__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Database Demo")

        self.view1 = SportsmenView()
        layout.addWidget(self.view1)
        button = QPushButton("Add a row")
        button.clicked.connect(self.addrow)
        layout.addWidget(button)

        btn1 = QPushButton("del a row")
        # todo meg kell nézni, hogy működik a QSqlTableModel.removeRow !!!
        btn1.clicked.connect(lambda: self.view1.model.removeRow(self.view1.currentIndex().row()))
        layout.addWidget(btn1)

    def addrow(self):
        # self.view1.model.rowCount()
        # todo meg kell nézni, hogy működik a QSqlTableModel.insertRows !!!
        ret = self.view1.model.insertRows(self.view1.model.rowCount(), 1)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # db = QSqlDatabase.addDatabase('QSQLITE')
    # db.setDatabaseName('sports.db')

    try:
        db = mdb.connect('localhost', 'qsqldb', 'qsqlpassword', 'qsqldb')
        QMessageBox.about(None, 'Connection', 'Database Connected Successfully')

    except mdb.Error as e:
        QMessageBox.about(None, 'Connection', 'Failed To Connect Database')
        sys.exit(1)

    dlg = SportsmenDialog()
    dlg.show()
    sys.exit(app.exec_())