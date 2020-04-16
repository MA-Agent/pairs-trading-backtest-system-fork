import numpy as np
from binance.client import Client
from  helpers.model_helper import send_telegram
import settings

class Wallet:
    # all values are in Bitcoin
    def __init__(self, paper=True):
        self.fee = 0.075/100
        self.paper = paper
        self.holdings = {
            'btc': 2.0,
            'a': 0,
            'b': 0
        }

    def prepare_order(self, quantity, precision):
            return "{:0.0{}f}".format(quantity, precision)


    def buy(self, asset, quantity, price):
        # print(price * quantity * (1+self.fee))
        self.holdings['btc'] -= price * quantity * (1+self.fee) 
        self.holdings[asset] += quantity
        
        if not self.paper:
            send_telegram("Buy {:.2f} {} @ {:.8f}".format(quantity, asset, price)) 
            #buy
            return

    def sell(self, asset, quantity, price):
        # print(price * quantity * (1+self.fee))
        self.holdings['btc'] += price * quantity * (1-self.fee)
        self.holdings[asset] -= quantity
        
        if not self.paper:
            send_telegram("Sell {:.2f} {} @ {:.8f}".format(quantity, asset, price)) 
            # sell
            return

    def client(self):
        return Client(
            settings.KEY,
            settings.TOKEN
        )