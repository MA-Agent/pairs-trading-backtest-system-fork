import numpy as np
from binance.client import Client
from  helpers.model_helper import send_telegram
import settings
import time

class Wallet:
    # all values are in Bitcoin
    def __init__(self, pair1='a', pair2='b', paper=True):
        self.fee = 0.075/100
        self.paper = paper
        self.holdings = {
            'btc': 2.0,
        }
        self.holdings[pair1] = 0
        self.holdings[pair2] = 0
        self.loan = None

    def prepare_quantity(self, quantity, precision):
            return "{:.0{}f}".format(quantity, precision)

    def buy(self, asset, quantity, price):
        # print(price * quantity * (1+self.fee))
        self.holdings['btc'] -= price * quantity * (1+self.fee) 
        self.holdings[asset] += quantity
        
        if not self.paper:
            send_telegram("Buy {:.2f} {} @ {:.8f}".format(quantity, asset, price)) 
            #buy
            order = self.client().create_margin_order(
                symbol=asset + 'BTC',
                side='BUY',
                type='MARKET',
                quantity=self.prepare_quantity(quantity * (1+self.fee) , 0))
            print(order)
    
            if self.loan:
                transaction = self.client().repay_margin_loan(asset=asset, amount=self.prepare_quantity(quantity, 0) )
                print(transaction)

            return

    def sell(self, asset, quantity, price):
        # print(price * quantity * (1+self.fee))
        self.holdings['btc'] += price * quantity * (1-self.fee)
        self.holdings[asset] -= quantity

        if not self.paper:
            send_telegram("Sell {:.2f} {} @ {:.8f}".format(quantity, asset, price)) 
            # sell
            if self.holdings[asset] < 0:
                transaction = self.client().create_margin_loan(asset=asset, amount=self.prepare_quantity(quantity, 0))
                print(transaction)
                self.loan = transaction['tranId']

            order = self.client().create_margin_order(
                symbol=asset + 'BTC',
                side='SELL',
                type='MARKET',
                quantity=self.prepare_quantity(quantity, 0))
            print(order)

            return

    def client(self):
        return Client(
            settings.KEY,
            settings.TOKEN
        )

