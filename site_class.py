import main.py

class Site():
    def __init__(self, accounts = {},houses = []):
        self.accounts = accounts
        self.houses = houses

    def addAccount(self,username,password):
        newaccount = main.User(username,password)
        self.accounts[username] = password

    def checklogin(self,username,password):
        if username in self.accounts:
            if password == self.accounts[username][0]:
                return True
        return False

    def selectType()
