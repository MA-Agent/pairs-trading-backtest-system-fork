from models.realtime import Realtime

class TradePlacementProcess:
    def run(self, pairs):
        Realtime().run(pairs[0], pairs[1])
