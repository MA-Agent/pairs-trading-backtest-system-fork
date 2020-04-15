from models.realtime import Realtime

class TradePlacementProcess:
    def run(self, pair1, pair2):
        Realtime().run(pair1, pair2)
