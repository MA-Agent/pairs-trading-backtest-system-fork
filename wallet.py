import numpy as np

class Wallet:
    # all values are in Bitcoin
    def __init__(self):
        self.fee = 0.075/100
        self.holdings = {
            'btc': 100,
            'a': 0,
            'b': 0
        }

    def buy(self, asset, quantity, price):
        self.holdings['btc'] -= price * quantity * (1+self.fee) 
        self.holdings[asset] += quantity

    def sell(self, asset, quantity, price):
        self.holdings['btc'] += price * quantity * (1-self.fee)
        self.holdings[asset] -= quantity
