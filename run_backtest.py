from services.pair_selection_service import PairSelectionService
from models.backtest import Backtest
import pickle

# with open("30_days_all_assets.pickle","rb") as f:
#     all_pairs = pickle.load(f)

from services.asset_service import AssetService

asset_service = AssetService()
all_pairs = asset_service.possible_pairs()

# pairs = PairSelectionService().selected_from_pickled_candles(all_pairs)
# Change this line:
pairs = PairSelectionService().from_live_candles(30, '1d', possible_pairs=all_pairs)

Backtest().run(pairs)
