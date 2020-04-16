from PySide2.QtSql import *
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import *
import site
import sys

def dbconn():
    dblist = QSqlDatabase.drivers()
    print(dblist)

    result = QSqlDatabase.isDriverAvailable('QMYSQL')
    print(f"Postgresql driver létezik? {result}")
    print(QLibraryInfo.location(QLibraryInfo.PluginsPath))
    db = QSqlDatabase.addDatabase("QPSQL", 'haha')
    db.setDatabaseName('qsqldb')
    db.setHostName('localhost')
    db.setUserName('qsqluser')
    db.setPassword('qsqlpassword')
    # db.setPort(5432)
    ok = db.open()
    if db.lastError().isValid():
        print(db.lastError())
    print(f"Adatbázist sikerült megnyitni?{ok}")
    # if not db.open():
    #     QMessageBox.critical(None, "Cannot open database",
    #                                "Unable to establish a database connection.\n"
    #                                             "Click Cancel to exit.",
    #                                QMessageBox.Cancel)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dbconn()
    app.exec_()