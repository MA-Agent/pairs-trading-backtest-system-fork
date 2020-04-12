import numpy as np
import helpers.model_helper as helper
from services.cointegration_service import CointegrationService
from services.ticker_service import TickerService
from services.price_service import PriceService
import time
import pandas as pd
import matplotlib.pyplot as plt
from wallet import Wallet

class Realtime:
    def __init__(self):
        self.setup_backtest()

    def setup_backtest(self):
        self.lookback_period = 80
        self.z_upper = 1
        self.z_lower = -1
        self.p_threshold = 0.05
        self.non_coint_threshold = 60
        self.ticker_service = TickerService()
        self.price_service = PriceService()

    def setup_pass(self, asset_a, asset_b):
        self.wallet = Wallet()
        self.current_trade = {}
        self.pass_number = 1
        self.asset_a = asset_a
        self.asset_b = asset_b

    def open_trade(self, p_val, zscore, ticker_data_a, ticker_data_b, hedge):
        if helper.is_cointegrated(self.asset_a, self.asset_b):
            if zscore > self.z_upper:
                print('  - opening trade')
                # Go Short: the spread is more than the mean so we short B and long A
                price_a = ticker_data_a['ask']
                price_b = ticker_data_b['bid']

                self.current_trade = helper.build_trade(
                    price_a, price_b, hedge, 'short'
                )
                self.wallet.sell('b', self.current_trade['quantity_b'], price_b)
                self.wallet.buy('a', self.current_trade['quantity_a'], price_a)
                return

            if zscore < self.z_lower:
                print('  - opening trade')
                # Go Long: the spread is less than the mean so we short A and long B
                price_a = ticker_data_a['bid']
                price_b = ticker_data_b['ask']

                self.current_trade = helper.build_trade(
                    price_a, price_b, hedge, 'long'
                )
                self.wallet.sell('a', self.current_trade['quantity_a'], price_a)
                self.wallet.buy('b', self.current_trade['quantity_b'], price_b)
                return

    def close_trade(self, p_val, zscore, ticker_data_a, ticker_data_b, hedge):
        # if not helper.is_cointegrated(self.asset_a, self.asset_b):
        #     if self.current_trade['non_coint_count'] > self.non_coint_threshold:
        #         print('  - closing trade for notn cointegration')
        #         self.close_for_non_cointegration(
        #             p_val, zscore, ticker_data_a, ticker_data_b, hedge
        #         )
        #         self.current_trade = {}
        #         return
        #     else:
        #         self.current_trade['non_coint_count'] += 1

        if self.current_trade['type'] == 'short' and zscore < self.z_lower:
            print('  - closing trade')
            price_a = ticker_data_a['bid']
            price_b = ticker_data_b['ask']

            self.wallet.sell('a', self.current_trade['quantity_a'], price_a)
            self.wallet.buy('b', self.current_trade['quantity_b'], price_b)

            self.current_trade = {}
            return

        if self.current_trade['type'] == 'long' and zscore > self.z_upper:
            print('  - closing trade')
            price_a = ticker_data_a['ask']
            price_b = ticker_data_b['bid']

            self.wallet.sell('b', self.current_trade['quantity_b'], price_b)
            self.wallet.buy('a', self.current_trade['quantity_a'], price_a)


            self.current_trade = {}
            return

    # def close_for_non_cointegration(self, p_val, zscore, ticker_data_a, ticker_data_b, hedge):
    #     if self.current_trade['type'] == 'short':
    #         print('  - closing trade')
    #         price_a = ticker_data_a['bid']
    #         price_b = ticker_data_b['ask']
    #
    #         self.balance += helper.calculate_wallet_delta(
    #             price_a, price_b, hedge, 'long'
    #         )
    #     else:
    #         print('  - closing trade')
    #         price_a = ticker_data_a['ask']
    #         price_b = ticker_data_b['bid']
    #
    #         self.balance += helper.calculate_wallet_delta(
    #             price_a, price_b, hedge, 'short'
    #         )

    def run(self, asset_a, asset_b):
        self.setup_pass(asset_a, asset_b)

        while True:
            # try:
                historic_prices = self.price_service.historic_prices(1, '5m', [asset_a, asset_b])
                historic_prices_a = historic_prices[asset_a][-80:]
                historic_prices_b = historic_prices[asset_b][-80:]

                ticker_data_a = self.ticker_service.ticker_for(asset_a)
                ticker_data_b = self.ticker_service.ticker_for(asset_b)

                historic_prices_a = pd.Series(np.append(historic_prices_a.values, ticker_data_a['avg_price']), name='subset_prices_a')
                historic_prices_b = pd.Series(np.append(historic_prices_b.values, ticker_data_b['avg_price']), name='subset_prices_b')

                hedge = helper.simple_hedge(historic_prices_a, historic_prices_b)
                spreads = helper.simple_spreads(historic_prices_a, historic_prices_b, 0)
                zscore = helper.simple_zscore(spreads)

                p_val = CointegrationService().p_value(
                    historic_prices_a, historic_prices_b
                )

                if not helper.currently_trading(self.current_trade):
                    self.open_trade(
                        p_val,
                        zscore,
                        ticker_data_a,
                        ticker_data_b,
                        hedge
                    )
                else:
                    self.close_trade(
                        p_val,
                        zscore,
                        ticker_data_a,
                        ticker_data_b,
                        hedge
                    )

                self.pass_number += 1

                print('pass ' + str(self.pass_number))
                print('holdings (BTC): ', self.wallet.holdings['btc'])
                print('holidings (Asset A): ', self.wallet.holdings['a'])
                print('holidings (Asset B): ', self.wallet.holdings['b'])
                print('zscore:', zscore)
                print('hedge:', hedge)
                print('-'*20)
                print()

                time.sleep(60*5)
            # except:
            #     time.sleep(60)
            #     continue
