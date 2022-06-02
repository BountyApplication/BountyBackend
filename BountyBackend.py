from flask import Flask
from flask import request
import BountyDatabase
import json

app = Flask("BountyBackend")

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
        return 'POST Accounts'
    else:
        f = open("dummyAccounts.json")
        accounts = json.load(f)
        f.close()
        return json.dumps(accounts)

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
        return 'PUT Account'
    else:
        return 'Invalid method'