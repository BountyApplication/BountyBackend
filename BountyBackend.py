from flask import Flask
from flask import request
import BountyDatabase
import json

app = Flask("BountyBackend")
DB = BountyDatabase.DBStorage("bounty")

@app.route("/")
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
        dbJSONString = DB.add_account(request.headers['accountId'],request.headers['fname'],request.headers['lname'],request.headers['balance'])
        return dbJSONString
    else:
        dbJSONString = DB.get_accounts()
        return dbJSONString

@app.route('/bounty/accounts/<userID>', methods=['GET', 'PUT', 'POST'])
def userid():
    if request.method == 'POST':
        return 'POST UserID'
    elif request.method == 'PUT':
        return 'PUT UserID'
    else:
        return 'GET UserID'

@app.route('/bounty/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        return 'POST Products'
    else:
        f = open("dummyProducts.json")
        products = json.load(f)
        f.close()
        return json.dumps(products)

@app.route('/bounty/products/<productID>', methods=['PUT'])
def productid():
    if request.method == 'PUT':
        return 'PUT Product'
    else:
        return 'Invalid method'
