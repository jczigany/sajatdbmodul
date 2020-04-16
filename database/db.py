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

    def delete_rekord(self, table, value):
        """ Az átadott rekord_id-ú rekord törlése a table táblából. A táblából meg kell
            határozni az elsődleges kulcsot (egyedi azonosító) és annak típusától függően
            (int vagy str) kell az sql parancsot paraméterezni.  Amikor a view meghívja ezt a metódust,
            akkor átadja az elsődleges kulcsnak megfelelő mező értékét. Ennek vizsgálatával (type() )
            dönthető el, hogy az sql-ben int-ként vagy str-ként kell kezelni."""
        self.table = table
        # A tábla elsődleges kulcsának meghatározása
        self.cursor.execute(f"describe {table}")
        all_rows2 = self.cursor.fetchall()
        for row in all_rows2:
            if 'PRI' in row:
                self.id_name =  row[0]
        self.value = value
        # Az elsődleges kulcs típusától függően (int vagy str) a törlés végrahajtása
        if type(self.value) == 'int':
            self.cursor.execute(f"DELETE FROM {self.table} WHERE {self.id_name}={self.value}")
        else:
            self.cursor.execute(f"DELETE FROM {self.table} WHERE {self.id_name}='{self.value}'")
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