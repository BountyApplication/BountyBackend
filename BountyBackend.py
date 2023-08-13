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

from flask import Flask
from flask import send_file
from flask_cors import CORS
from flask import request
import BountyDatabase
import json

app = Flask("BountyBackend")
CORS(app)
DB = BountyDatabase.DBStorage("bounty")

@app.route("/bounty/")
def bounty():
    string = r" <p>Welcome to the BounyBackend!</p><div class=\"border-header border-top p-3\"><pre class=\"pre\">\
        ___ __                                           \
   (_  ( . ) )__                  '.    \   :   /    .'  \
     '(___(_____)      __           '.   \  :  /   .'    \
                     /. _\            '.  \ : /  .'      \
                .--.|/_/__      -----____   _  _____-----\
_______________''.--o/___  \_______________(_)___________\
       ~        /.'o|_o  '.|  ~                   ~   ~  \
  ~            |/    |_|  ~'         ~                   \
               '  ~  |_|        ~       ~     ~     ~    \
      ~    ~          |_|O  ~                       ~    \
             ~     ___|_||_____     ~       ~    ~       \
   ~    ~      .'':. .|_|A:. ..::''.                     \
             /:.  .:::|_|.\ .:.  :.:\   ~                \
  ~         :..:. .:. .::..:  .:  ..:.       ~   ~    ~  \
             \.: |BOUNTY-ISLAND| .:./                    \
    ~      ~      ~    ~    ~         ~                  \
               ~           ~    ~   ~             ~      \
        ~         ~            ~   ~                 ~   \
   ~                  ~    ~ ~                 ~         \
   </pre><div>"
    return string

@app.route('/bounty/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        if 'cardId' in request.headers:
            cardId = request.headers['cardId']
        else:
            cardId = None
        dbJSONString = DB.add_account(request.headers['firstname'],request.headers['lastname'],request.headers['balance'], cardId)
        return dbJSONString
    else:
        dbJSONString = DB.get_all_accounts()
        return dbJSONString

@app.route('/bounty/accounts/<int:userId>', methods=['GET', 'PUT', 'POST'])
def userid(userId : int):
    if request.method == 'POST':
        dbJSONString = DB.add_new_accounting(userId, request.headers['total'], request.headers['products'] , request.headers['correction'], request.headers['cashPayment'], request.headers['productSum'])
        return dbJSONString
    elif request.method == 'PUT':
        if 'cardId' in request.headers:
            cardId = request.headers['cardId']
        else:
            cardId = 0
        dbJSONString = DB.modify_account(userId,request.headers['firstname'],request.headers['lastname'], cardId, request.headers['active'])
        return dbJSONString
    else:
        dbJSONString = DB.get_account_by_userid(userId)
        return dbJSONString

@app.route('/bounty/history/<int:userId>', methods=['GET'])
def history(userId : int):
    if request.method == 'GET':
        dbJSONString = DB.get_history_of_account(userId)
        return dbJSONString

@app.route('/bounty/products', methods=['GET', 'POST', 'PUT'])
def products():
    if request.method == 'POST':
        dbJSONString = DB.add_product(request.headers['name'],request.headers['price'])
        return dbJSONString
    elif request.method == 'PUT':
        dbJSONString = DB.modify_product(request.headers['productId'],request.headers['name'],request.headers['price'],request.headers['active'])
        return dbJSONString
    else:
        dbJSONString = DB.get_products()
        return dbJSONString

@app.route('/bounty/cards/<int:cardId>', methods=['GET'])
def cards(cardId: int):
    if request.method == 'GET':
        dbJSONString = DB.get_account_by_cardId(cardId)
        return dbJSONString
    
@app.route('/bounty/closing', methods=['GET'])
def closing():
    if request.method == 'GET':
        abs_filepath = DB.export_non_empty_accounts()
    return send_file(abs_filepath, as_attachment=False)