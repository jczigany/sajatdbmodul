from database.db import MysqlClient

client = MysqlClient()

client.cursor.execute("select id, gyartmany, tipus, gyartasiev, futottkm from teszt2")
all_rows = client.cursor.fetchall()
print(len(all_rows))

field_names = [i for i in client.cursor.description]
print(field_names)

client.cursor.execute("describe teszt")
all_rows2 = client.cursor.fetchall()
print(all_rows2)

for row in all_rows2:
    if 'PRI' in row:
        print("Az egyedi azonosító:", row[0])