import sqlite3

def open_or_create_db():
    # connecting to database
    connection = sqlite3.connect('bounty.db')

    # cursor
    cursor = connection.cursor()

    # SQL command to create a table in the database
    sql_command = """CREATE TABLE IF NOT EXISTS accounts ( 
    number INTEGER PRIMARY KEY UNIQUE NOT NULL, 
    fname VARCHAR(20), 
    lname VARCHAR(30), 
    balance FLOAT, 
    joining DATE);"""
    # execute the statement
    cursor.execute(sql_command)
    # close the connection
    connection.close()

def add_account(fname, lname, balance):
    # connecting to database
    connection = sqlite3.connect('bounty.db')
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO accounts (fname,lname,balance) VALUES (?,?,?);""", (fname,lname,balance))
    sql_command = """SELECT * FROM accounts;"""
    cursor.execute(sql_command)
    answer = cursor.fetchall()
    print(answer)
    # close the connection
    connection.close()
    return answer

def get_accounts():
    # connecting to database
    connection = sqlite3.connect('bounty.db')
    cursor = connection.cursor()
    sql_command = """SELECT fname,lname,balance FROM accounts;"""
    cursor.execute(sql_command)
    answer = cursor.fetchall()
    # close the connection
    connection.close()
    return answer