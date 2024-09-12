from game_engine.player import Player
from multiprocessing import Queue
import json

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
        true_game_state_json = json.loads(true_game_state)

        self.p1.hp = true_game_state_json['p1']['hp']
        self.p1.num_bullets = true_game_state_json['p1']['bullets']
        self.p1.num_bombs = true_game_state_json['p1']['bombs']
        self.p1.hp_shield = true_game_state_json['p1']['shield_hp']
        self.p1.num_deaths = true_game_state_json['p1']['deaths']
        self.p1.num_shield = true_game_state_json['p1']['shields']
        
        self.p2.hp = true_game_state_json['p2']['hp']
        self.p2.num_bullets = true_game_state_json['p2']['bullets']
        self.p2.num_bombs = true_game_state_json['p2']['bombs']
        self.p2.hp_shield = true_game_state_json['p2']['shield_hp']
        self.p2.num_deaths = true_game_state_json['p2']['deaths']
        self.p2.num_shield = true_game_state_json['p2']['shields']

        updated_game_state = {
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
        return updated_game_state