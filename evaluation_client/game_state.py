from evaluation_client.player import Player

class GameState:
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()

    def get_dict(self):
        data = {
            "p1": self.p1.get_dict(),
            "p2": self.p2.get_dict()
        }

        return data