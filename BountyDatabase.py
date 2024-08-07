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
from flask import render_template
from pathlib import Path
import threading
import csv
from datetime import datetime;

lock = threading.Lock()

class DBStorage:
    def __init__(self, name):
        
        print(sqlite3.sqlite_version)
        self.name = name
        self.isCreated = self.open_db()
        # Define the lock globally

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

            if False: # not self.dbAlreadyExists:
                if table == "products":
                    self.f = open("dummyProducts.json")
                    products = json.load(self.f)
                    self.f.close()
                    for product in products["products"]:
                        self.cursor.execute("""INSERT INTO products(name,price,active) VALUES(?,?,?);""", (product["name"],product["price"],product["active"]))
                        self.connection.commit()
                if table == "accounts":
                    self.f = open("dummyAccounts.json")
                    accounts = json.load(self.f)
                    self.f.close()
                    for account in accounts["accounts"]:
                        self.cursor.execute("""INSERT INTO accounts(firstname,lastname,balance,joining,active) VALUES(?,?,?,datetime('now'),?);""", (account["firstname"], account["lastname"],account["balance"],account["active"]))
                        self.connection.commit()
        self.close_db()

    def db_to_csv(self, dbData, table):
        columns = self.tables[table]['columns']
        csvStructure = []
        if len(dbData) > 1 or table != "accounts": # for table accounts we want to have only a single user replied, not a list
            for x in range(0, len(dbData)):
                csvStructure.append([])
                columnidx = 0
                for column in columns:
                    csvStructure[x].append(str(dbData[x][columnidx]))
                    columnidx += 1
        elif len(dbData) == 1:
            csvStructure.append([])
            columnidx = 0
            for column in columns:
                    csvStructure[0].append(dbData[0][columnidx])
                    columnidx += 1
        return csvStructure

    def db_to_json(self, dbData, table):
        columns = self.tables[table]['columns']
        jsonObject = []
        if len(dbData) > 1 or table != "accounts": # for table accounts we want to have only a single user replied, not a list
            for x in range(0,len(dbData)):
                jsonObject.append({})
                columnidx = 0
                for column in columns:
                    jsonObject[x][column] = dbData[x][columnidx]
                    columnidx += 1
        elif len(dbData) == 1:
            jsonObject = {}
            columnidx = 0
            for column in columns:
                    jsonObject[column] = dbData[0][columnidx]
                    columnidx += 1
        
        jsonString = json.dumps(jsonObject)
        return jsonString

    def add_account(self, firstname, lastname, balance, cardId):
        self.open_db()
        self.cursor.execute("""INSERT INTO accounts(firstname,lastname,balance,joining,cardId) VALUES(?,?,?,datetime('now'),?);""", (firstname, lastname, balance, cardId))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM accounts WHERE firstname=? LIMIT 1;""", (firstname, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, "accounts")
        return dbJSONString

    def get_all_accounts(self):
        self.open_db()
        self.cursor.execute("""SELECT * FROM accounts;""")
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
        return dbJSONString
    
    def export_non_empty_accounts(self):
        self.open_db()
        self.cursor.execute("""SELECT * FROM accounts WHERE balance != 0;""")
        answer = self.cursor.fetchall()
        self.close_db()
        dbCSVObject = self.db_to_csv(answer, 'accounts')
        csv_file_path = Path('./open_accounts.csv')
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for line in dbCSVObject:
                writer.writerow(line)
        return csv_file_path.resolve()

    def get_account_by_userId(self, accountId):
        self.open_db()
        self.cursor.execute("""SELECT * FROM accounts WHERE userId=?;""", (accountId, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
        return dbJSONString

    def get_account_by_cardId(self, cardId):
        self.open_db()
        self.cursor.execute("""SELECT * FROM accounts WHERE cardId=?;""", (cardId, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
        return dbJSONString

    def modify_account(self,accountId,firstname,lastname,balance,cardId,active):
        self.open_db()
        if cardId == 0:
            self.cursor.execute("""SELECT cardId FROM accounts WHERE accountId=?""", (accountId, ))
            cardId = int(self.cursor.fetchall())
        self.cursor.execute("""UPDATE accounts SET firstname=?, lastname=?, balance=?, cardId=?, active=? WHERE userId=?;""", (firstname, lastname, balance, cardId, active, accountId))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM accounts WHERE userId=?;""", (accountId, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
        return dbJSONString

    def add_new_accounting(self, accountId, total, products, correction, cashPayment, productSum):
        self.open_db()
        self.cursor.execute("""SELECT balance FROM accounts WHERE userId=?;""", (accountId, ))
        answer = self.cursor.fetchall()
        oldBalance = float(answer[0][0])
        newBalance = round(oldBalance - float(total), 2)
        if newBalance >= 0.0:
            self.cursor.execute("""UPDATE accounts SET balance=? WHERE userId=?""", (newBalance, accountId))
            now = datetime.now()
            self.cursor.execute("""INSERT INTO history (userId,date,oldBalance,newBalance,total,correction,cashPayment,productSum,products) VALUES (?,?,?,?,?,?,?,?,?);""", (accountId, now, oldBalance, newBalance, total, correction, cashPayment, productSum, products))
            self.connection.commit()
        self.cursor.execute("""SELECT * FROM accounts WHERE userId=?;""", (accountId, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
        return dbJSONString

    def remove_last_accounting(self, accountId):
        self.open_db()
        self.cursor.execute("""SELECT * FROM history WHERE userId=? LIMIT 1;""", (accountId, ))
        answer = self.cursor.fetchall()
        balance = answer['oldBalance']
        #self.cursor.execute("""UPDATE accounts SET balance=? WHERE userId==?""", (balance, accountId))
        self.cursor.execute("""SELECT * FROM accounts;""")
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'accounts')
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
        self.cursor.execute("""SELECT * FROM products;""")
        answer = self.cursor.fetchall()
        print(len(answer))
        self.cursor.execute("""INSERT INTO products(name,price,place) VALUES(?,?,?);""", (name, price, len(answer)))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM products WHERE name=? LIMIT 1;""", (name, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'products')
        return dbJSONString

    def get_products(self):
        self.open_db()
        self.cursor.execute("""SELECT * FROM products;""")
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'products')
        return dbJSONString

    def modify_product(self, id, name, price, place, active):
        self.open_db()
        self.cursor.execute("""UPDATE products SET name=?, price=?, place=?, active=? WHERE productId=?;""", (name, price, place, active, id))
        self.connection.commit()
        self.cursor.execute("""SELECT * FROM products WHERE productId=?;""", (id, ))
        answer = self.cursor.fetchall()
        self.close_db()
        dbJSONString = self.db_to_json(answer, 'products')
        return dbJSONString

    def open_db(self):
        lock.acquire(True)
        db_path = Path(self.name + '.db')
        self.dbAlreadyExists = Path.exists(db_path)
        # connecting to database
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def close_db(self):
        # close the connection
        self.connection.close()
        lock.release()
