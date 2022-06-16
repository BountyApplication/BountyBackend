import requests
import BountyDatabase

class TestClass:
    #def test_new_account(self):
    #    api_url = 'http://127.0.0.1:5000/bounty/accounts'
    #    header = {'fname': 'Mister', 'lname' : 'Bounty', 'balance' : 23}
    #    response = requests.post(api_url, data = header)
    
    def test_add_account(self):
        DB = BountyDatabase.DBStorage("bounty")
        result = DB.add_account("qwed","rtz",22.4)
        DB.close_db()
        print(result) # {"accounts": [{"accountId": 1, "fname": "qwed", "lname": "rtz", "balance": 22.4, "joining": "2022-06-16 19:18:36"}]}
        assert result != ""

    def test_modify_account(self):
        DB = BountyDatabase.DBStorage("bounty")
        result = DB.add_account("qwed","rtz",22.4)
        result = DB.modify_account(1,"qwedy","rtzf")
        DB.close_db()
        assert result != ""

    def test_add_accouning(self):
        DB = BountyDatabase.DBStorage("bounty")
        result = DB.add_account("qwed","rtz",22.4)
        result = DB.add_new_accounting(1,20)
        DB.close_db()
        assert result != ""

    def test_get_history(self):
        DB = BountyDatabase.DBStorage("bounty")
        result = DB.add_account("qwed","rtz",22.4)
        result = DB.add_new_accounting(1,20)
        result = DB.get_history_of_account(1)
        DB.close_db()
        assert result != ""