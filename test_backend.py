import requests

class TestClass:
    def test_new_account(self):
        api_url = 'http://127.0.0.1:5000/bounty/accounts'
        header = {'fname': 'Mister', 'lname' : 'Bounty', 'balance' : 23}
        response = requests.post(api_url, data = header)
    