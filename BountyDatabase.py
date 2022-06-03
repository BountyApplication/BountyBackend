import sqlite3
import json

def open_or_create_db():
    # connecting to database
    connection = sqlite3.connect('bounty.db')

    f = open("configDatabase.json")
    tables = json.load(f)
    f.close()

    # cursor
    cursor = connection.cursor()
    for table in tables:
        sql_command = """CREATE TABLE IF NOT EXISTS %s ("""%table
        columns = tables[table]['columns']
        
        for column in columns.keys():
            sql_command += """%s """%column
            sql_command += """%s, """%columns[column]
        sql_command = sql_command[:-2]
        sql_command += """) """

        print(sql_command)
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