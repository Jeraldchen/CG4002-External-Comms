from player import Player

class GameState:
    def __init__(self):
        self.p1 = Player(player_id=1, hp=100, num_bullets=10, num_bombs=3, hp_shield=30, num_deaths=0, num_shield=3)
        self.p2 = Player(player_id=2, hp=100, num_bullets=10, num_bombs=1, hp_shield=20, num_deaths=1, num_shield=2)

    def get_dict(self):
        data = {
            "p1": self.p1.get_dict(),
            "p2": self.p2.get_dict()
        }

        return data