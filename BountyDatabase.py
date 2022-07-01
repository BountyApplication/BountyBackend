# 
# MIT License
# 
# Copyright (c) 2022 BountyApplication
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import sqlite3
import json

class DBStorage:
    def __init__(self, name):
        print(sqlite3.sqlite_version)
        self.name = name
        self.open_db()

        # read db config
        self.f = open("configDatabase.json")
        self.tables = json.load(self.f)
        self.f.close()

        # create table if it not already exists
        for table in self.tables:
            sql_command = """CREATE TABLE IF NOT EXISTS %s ("""%table
            # read columns from db config
            columns = self.tables[table]['columns']

            # build the statement
            for column in columns.keys():
                sql_command += """%s """%column
                sql_command += """%s, """%columns[column]
            sql_command = sql_command[:-2] # remove ', ' at the end 
            if self.tables[table]['additional'] != "":
                sql_command += " , " + self.tables[table]['additional']
            sql_command += """) """
            print(sql_command)
            # execute the statement
            self.cursor.execute(sql_command)

            # read columns from db
            self.cursor.execute("""PRAGMA table_info(accounts);""")
            tableinfo = self.cursor.fetchall()

            if table == "products":
                self.f = open("dummyProducts.json")
                products = json.load(self.f)
                self.f.close()
                for product in products["products"]:
                    self.cursor.execute("""INSERT INTO products(name,price) VALUES(?,?);""", (product["name"],product["price"]))
                    self.connection.commit()
            if table == "accounts":
                self.f = open("dummyAccounts.json")
                accounts = json.load(self.f)
                self.f.close()
                for account in accounts["accounts"]:
                    self.cursor.execute("""INSERT INTO accounts(firstname,lastname,balance) VALUES(?,?,?);""", (account["firstname"], account["lastname"],account["balance"]))
                    self.connection.commit()
        self.close_db()

    def db_to_json(self, dbData, table):
        columns = self.tables[table]['columns']
        jsonString = """{"""
        jsonObject = []
        for x in range(0,len(dbData)):
            jsonObject.append({})
            columnidx = 0
            for column in columns:
                jsonObject[x][column] = dbData[x][columnidx]
                columnidx += 1
        jsonString = json.dumps(jsonObject)
        return jsonString

    def add_account(self, firstname, lastname, balance):
        self.open_db()
        self.cursor.execute("""INSERT INTO accounts(firstname,lastname,balance,joining) VALUES(?,?,?,datetime('now'));""", (firstname, lastname, balance))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM accounts WHERE firstname=? LIMIT 1;""", (firstname, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, "accounts")
        return dbJSONString

    def get_accounts(self):
        self.open_db()
        self.cursor.execute("""SELECT * FROM accounts;""")
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
        return dbJSONString

    def modify_account(self,accountId,firstname,lastname):
        self.open_db()
        self.cursor.execute("""UPDATE accounts SET firstname=?, lastname=? WHERE userId=?;""", (firstname, lastname, accountId))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM accounts WHERE userId=?;""", (accountId, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
        return dbJSONString

    def add_new_accounting(self, accountId, amount):
        self.open_db()
        self.cursor.execute("""INSERT INTO history (userId,date,amount) VALUES (?,datetime('now'),?);""", (accountId, amount))
        self.cursor.execute("""SELECT balance FROM accounts WHERE userId=?;""", (accountId, ))
        answer = self.cursor.fetchall()
        balance = float(answer[0][0]) - float(amount)
        self.cursor.execute("""UPDATE accounts SET balance=? WHERE userId=?""", (balance, accountId))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM accounts WHERE userId=?;""", (accountId, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
        return dbJSONString

    def remove_last_accounting(self, accontId):
        self.open_db()
        self.cursor.execute("""INSERT INTO history (userId,balance) VALUES (?,?);""", (accountId, balance))
        self.cursor.execute("""UPDATE accounts SET balance=? WHERE userId==?""", (balance, accountId))
        sql_command = """SELECT * FROM accounts;"""
        self.cursor.execute(sql_command)
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = db_to_json(answer, 'accounts')
        return dbJSONString
    
    def get_history_of_account(self, accountId):
        self.open_db()
        self.cursor.execute("""SELECT * FROM history WHERE userId=?;""", (accountId, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'history')
        return dbJSONString

    def add_product(self, name, price):
        self.open_db()
        self.cursor.execute("""INSERT INTO products(name,price) VALUES(?,?);""", (name, price))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM products WHERE name=? LIMIT 1;""", (name, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, "products")
        return dbJSONString

    def get_products(self):
        self.open_db()
        self.cursor.execute("""SELECT * FROM products;""")
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'products')
        return dbJSONString

    def modify_product(self, id, name, price):
        self.open_db()
        self.cursor.execute("""UPDATE products SET name=?, price=? WHERE productId=?;""", (name, price, id))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM products WHERE productId=?;""", (id, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'products')
        return dbJSONString

    def open_db(self):
        # connecting to database
        self.connection = sqlite3.connect(self.name + '.db')
        self.cursor = self.connection.cursor()

    def close_db(self):
        # close the connection
        self.connection.close()