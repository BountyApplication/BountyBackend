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

import BountyDatabase

class TestClass:
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