from PySide2.QtWidgets import QMessageBox, QApplication
from PySide2.QtCore import QObject
from mysql import connector

import sys


class MysqlClient(QObject):
    def __init__(self):
        super(MysqlClient, self).__init__()

        self.db = connector.connect(
            host="localhost",
            user="qsqldb",
            passwd="qsqlpassword",
            database="qsqldb"
        )
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()

    def get_all(self, table):
        """ Tábla tartalmának lekérése ( select * from table)
            Visszaadott érték:
            ha a tábla nem üres: tuple-k listája
            ha a tábla üres: üres lista []
            Ha a tábla nem létezik: None
            """
        self.table = table
        self.data = []
        if self.exist_table(self.table):
            self.cursor.execute(f"SELECT * FROM {self.table}")
            field_names = [i[0] for i in self.cursor.description]
            self.data.append(self.cursor.fetchall())
            self.data.append(field_names)
            return self.data

        return None

    def delete_rekord(self, table, id):
        """ Az átadott rekord_id-ú rekord törlése a table táblából"""
        self.table = table
        self.cursor.execute(f"describe {table}")
        all_rows2 = self.cursor.fetchall()
        for row in all_rows2:
            if 'PRI' in row:
                self.id_name =  row[0]
        self.rekord_id = id

        if type(self.rekord_id) == 'int':
            self.cursor.execute(f"DELETE FROM {self.table} WHERE {self.id_name}={self.rekord_id}")
        else:
            self.cursor.execute(f"DELETE FROM {self.table} WHERE {self.id_name}='{self.rekord_id}'")
        self.db.commit()

    def exist_table(self, table):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        for tables in rows:
            if table in tables:
                return True

        QMessageBox.about(None, 'Adatok lekérése', 'A megadott tábla nem létezik')
        sys.exit(1)

        # return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = MysqlClient()
    # print(client.exist_table("teszt3"))
    print(client.get_all("teszt2")[0])
    client.close()
    app.exec_()