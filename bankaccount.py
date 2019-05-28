import sqlite3
import re
from datetime import datetime

class BankAccount:

    def __init__(self, name, amount=0):

        self.name = name
        
        connection = sqlite3.connect('/home/BorneAgain/Desktop/flasktest/accounts.db')

        cursor = connection.cursor() 
        
        cursor.execute("""select name from accounts where name=?""",(self.name,))

        if len(cursor.fetchall()) == 0:

            self.createNew(amount)

    def __str__(self):

        return self.name + ': $'+str(self.getBalance())
    def createNew(self,amount):

        connection = sqlite3.connect('/home/BorneAgain/Desktop/flasktest/accounts.db')
        
        cursor = connection.cursor()
        '''
        sql_command = """
            CREATE TABLE accounts (
            name VARCHAR(20),
            amount DOUBLE
            );"""
        cursor.execute(sql_command)
        '''
        t = (self.name,amount)
        sql_command = """INSERT INTO  accounts (name,amount)
            VALUES (?,?);"""
        cursor.execute(sql_command,t)
         
        connection.commit()
    def getBalance(self):
        
        connection = sqlite3.connect('/home/BorneAgain/Desktop/flasktest/accounts.db')

        cursor = connection.cursor()

        sql_command = """select amount from accounts where name=?;"""

        cursor.execute(sql_command,(self.name,))

        return round(float(re.sub(r'[\(\),]','',str(cursor.fetchone()))),2)



    def deposit(self, amount):
        connection = sqlite3.connect('/home/BorneAgain/Desktop/flasktest/accounts.db')

        cursor = connection.cursor()

        if self.getBalance() + amount > 0:
            cursor.execute("""update accounts set amount=? where name =?;""",(amount+self.getBalance(),self.name))
            cursor.execute("""insert into history (username,dt,amount) values (?,?,?);""",(self.name,datetime.utcnow(),amount))
        else:
            
            cursor.execute("""update accounts set amount=? where name =?;""",(0,self.name))

            cursor.execute("""insert into history (username,dt,amount) values (?,?,?);""",(self.name,datetime.utcnow(),amount))
        connection.commit()

    def withdraw(self, amount):

        self.deposit(-amount)


    def recents(self):

        connection = sqlite3.connect('/home/BorneAgain/Desktop/flasktest/accounts.db')

        cursor = connection.cursor()

        cursor.execute("""select * from history where username=?""",(self.name,))

        return cursor.fetchall()


    def transfer(self, amount, target):


        connection = sqlite3.connect('/home/BorneAgain/Desktop/flasktest/accounts.db')

        cursor = connection.cursor()

        cursor.execute("""select * from accounts where name=?""",(target,))

        if len(cursor.fetchall()) > 0:

            self.withdraw(amount)

            cursor.execute("""update accounts set amount=amount+? where name=?""",(amount,target))
            
            connection.commit()

            return cursor.fetchall()
            
        else:

            return None


if __name__ == "__main__":
    '''
    connection = sqlite3.connect('accounts.db')

    cursor = connection.cursor()

    sql_command = """SELECT * FROM account"""

    cursor.execute(sql_command)
    
    print(cursor.fetchall())
    '''
    acct = BankAccount('porter',100)
    
    acct.deposit(200.11)

    print(acct)
