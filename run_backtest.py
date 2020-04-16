from services.pair_selection_service import PairSelectionService
from models.backtest import Backtest
import pickle

with open("30_days_BTC_assets_1m.pickle","rb") as f:
# with open("30_days_USDT_assets_1m.pickle","rb") as f:
    all_pairs = pickle.load(f)

pairs = PairSelectionService().from_pickled_candles(all_pairs)


# pairs = PairSelectionService().from_live_candles(30, '1m')

Backtest().run(pairs)
