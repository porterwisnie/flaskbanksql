import sqlite3

connection = sqlite3.connect('accounts.db')

cursor = connection.cursor()


t = ('porter',)
sql_command = """select hashedpw from users where name=?;"""
cursor.execute(sql_command,t)

x, = cursor.fetchall()[0]

print(x)

connection.commit()

