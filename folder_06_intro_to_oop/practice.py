class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    # TODO: Add a deposit method
    def deposit(self, amount):
        self.balance += amount
