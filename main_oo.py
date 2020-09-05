class Account:
    def __init__(self, name, date_range, transactions, prices):
        self.name = name
        self.date_range = date_range
        self.transactions = transactions
        self.prices = prices


p1 = Account("John", 36)

print(p1.name)
print(p1.age)
