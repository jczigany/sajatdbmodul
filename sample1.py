from PySide2.QtCore import QAbstractItemModel, QStringListModel, QAbstractTableModel
from PySide2.QtWidgets import QListView, QApplication, QTableView
import sys


# class StringListModel(QAbstractItemModel):
#     def __init__(self, numbers):
#         super(StringListModel, self).__init__()

class TableModel(QAbstractTableModel):
    def __init__(self, matrix):
        super(TableModel, self).__init__()

    def data(self, index, role):

        value = matrix[index.row()][index.column()]

        return value

    def rowCount(self, parent):
        return len(matrix)

    def columnCount(self, parent):
        return len(matrix[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)

    numbers = ["egy", "kettő", "három", "négy", "öt"]
    matrix = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]

    model = QStringListModel(numbers)
    model2 = TableModel(matrix)
    # model.columnCount(None)
    # view = QListView()
    # view.setModel(model)
    # view.show()
    view2 = QTableView()
    view2.setModel(model2)
    view2.show()
    app.exec_()
