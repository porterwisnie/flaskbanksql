import sqlite3
'''
connection = sqlite3.connect('accounts.db')

cursor = connection.cursor()

sql_command = """
    CREATE TABLE users (
    name VARCHAR(20) unique,
    hashedpw VARCHAR(200) 
    );"""
cursor.execute(sql_command)
 
connection.commit()
'''
def adduser(name,hashedpw):
    connection = sqlite3.connect('/home/BorneAgain/Desktop/flasktest/accounts.db')

    cursor = connection.cursor()


    t = (name,hashedpw)
    sql_command = """INSERT INTO  users (name,hashedpw)
        VALUES (?,?);"""
    cursor.execute(sql_command,t)
     
    connection.commit()
def validateLogin(name):
    #returns the hashed password for the flask app to evaluate
    connection = sqlite3.connect('/home/BorneAgain/Desktop/flasktest/accounts.db')

    cursor = connection.cursor()
    
    sql_command = """select hashedpw from users where name=?;"""

    cursor.execute(sql_command,(name,))
    
    x, = cursor.fetchone()
    if x != None:

        return x 
    else:
        return "Error"
    #connection.commit()
