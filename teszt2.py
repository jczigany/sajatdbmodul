import mysql.connector
from database.db import MysqlClient

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="qsqldb",
#     passwd="qsqlpassword",
#     database="qsqldb"
# )

client = MysqlClient()
print(client.get_all("teszt"))


# sql = "select * from teszt"
# cliet.cursor.execute(sql)
# # print(mycursor.column_names)
#
# # mydb.commit()
# eredmeny = cliet.cursor.fetchall()
# print(eredmeny)