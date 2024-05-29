import mysql.connector

dataBase = mysql.connector.connect(
host = 'localhost',
user = 'root',
passwd = '010405'

	)
cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE lab5")
cursorObject = dataBase.cursor()
cursorObject.execute("Keywords lab6")
print("All Done!")
