from random import seed
from random import randint

# class sessionID(): # TODO pretty sure this can be removed
#     def __init__(self, ID):
#         self.ID = ID
#         self.auth = False
#         self.authCustomerNum = None

class user():
    def __init__(self, name, surname, password, registeredAccounts):
        self.name = name
        self.surname = surname
        self.customerNum = randint(1,9999)
        self.password = password
        self.account = account(self.customerNum, registeredAccounts)
        self.accountNum = self.account.accountNum

    def deposit(self):
        valid = 0
        while valid == 0:
            deposit = int(input("How much would you like to deposit? "))

            if deposit < 0:
                print("Please enter a valid number!")
            else:
                self.account.balance = self.account.balance + deposit
                print("Deposit complete!\n")
                valid = 1

    def payment(self, registeredAccounts):
        accountExists = 0
        payeeAccount = int(input("Please enter a payee account number: "))

        for item in registeredAccounts:
            if item.accountNum == payeeAccount:
                payee = item
                accountExists = 1

        if accountExists == 1:
            valid = 0

            while valid == 0:
                payment = int(input("How much would you like to pay? "))

                if payment < 0:
                    print("Please enter a valid amount!\n")
                else:
                    self.account.balance = self.account.balance - payment
                    payee.balance = payee.balance + payment
                    print("Payment complete!\n")
                    valid = 1

        else:
            print("Account not found!\n")

        return None

    def checkBalance(self):
        print("\nAccount Number:",self.account.accountNum)
        print("Account Balance: $",self.account.balance)

        return None

class account():
    def __init__(self, customerNum, registeredAccounts):
        self.accountNum = randint(10000,20000)
        self.customerNum = customerNum
        self.balance = 1000000
        registeredAccounts.append(self)
