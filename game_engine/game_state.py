from game_engine.player import Player
from multiprocessing import Queue

class GameState:
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()

    def get_dict(self):
        data = {
            "p1": {
                'hp': self.p1.hp,
                'bullets': self.p1.num_bullets,
                'bombs': self.p1.num_bombs,
                'shield_hp': self.p1.hp_shield,
                'deaths': self.p1.num_deaths,
                'shields': self.p1.num_shield
            },
            "p2": {
                'hp': self.p2.hp,
                'bullets': self.p2.num_bullets,
                'bombs': self.p2.num_bombs,
                'shield_hp': self.p2.hp_shield,
                'deaths': self.p2.num_deaths,
                'shields': self.p2.num_shield
            }
        }

        return data
    
    def update_game_state(self, from_eval_server_queue: Queue):
        true_game_state = from_eval_server_queue.get()
        