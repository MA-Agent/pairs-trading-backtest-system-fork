from services.candle_service import CandleService
import pickle 
import pandas as pd

class PriceService:
    def __init__(self):
        self.candle_service = CandleService()

    def historic_prices(self, days_to_gather, interval, assets):
        candles = self.candle_service.candles(days_to_gather, interval, assets)
        
        # with open(str(days_to_gather) + '_days_all_'+  "_".join(list(map(str, assets))) + '_' + interval + '.pickle', 'wb') as f:
            # print('saving')
            # pickle.dump(candles, f)
            
        prices = {}

        for asset in assets:
            prices[asset] = pd.Series([float(c[4]) for c in candles[asset]])
        return prices

    def historic_prices_from_pickled_candles(self, assets, candles):
        prices = {}

        for asset in assets:
            prices[asset] = pd.Series([float(c[4]) for c in candles[asset]])
        return prices
