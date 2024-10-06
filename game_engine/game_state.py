from game_engine.player import Player
from multiprocessing import Queue
import json
import random

class GameState:
    def __init__(self):
        self.player_1 = Player()
        self.player_2 = Player()

    def __str__(self):
        return str(self.get_dict())

    def get_dict(self):
        data = {'p1': self.player_1.get_dict(), 'p2': self.player_2.get_dict()}
        return data

    def difference(self, received_game_state):
        """Find the difference between the current game_state and received"""
        try:
            recv_p1_dict = received_game_state["p1"]
            recv_p2_dict = received_game_state["p2"]

            p1 = self.player_1.get_difference(recv_p1_dict)
            p2 = self.player_2.get_difference(recv_p2_dict)

            diff = {'p1': p1, 'p2': p2}

            message = "Game state difference : " + str(diff)
        except KeyError:
            message = "Key error in the received Json"
        return message

    def init_players_random(self):
        """ Helper function to randomize the game state"""
        for player_id in [1, 2]:
            hp = random.randint(10, 90)
            bullets_remaining   = random.randint(0, 6)
            bombs_remaining     = random.randint(0, 2)
            shield_health       = random.randint(0, 30)
            num_unused_shield   = random.randint(0, 3)
            num_deaths          = random.randint(0, 3)

            self._init_player(player_id, bullets_remaining, bombs_remaining, hp,
                              num_deaths, num_unused_shield,
                              shield_health)

    def _init_player (self, player_id, bullets_remaining, bombs_remaining, hp,
                      num_deaths, num_unused_shield, shield_health):
        if player_id == 1:
            player = self.player_1
        else:
            player = self.player_2
        player.set_state(bullets_remaining, bombs_remaining, hp, num_deaths,
                         num_unused_shield, shield_health)

    def perform_action(self, action, player_id, is_visible):
        """use the user sent action to alter the game state"""

        if player_id == 1:
            attacker            = self.player_1
            opponent            = self.player_2
            # opponent_position   = position_2
        else:
            attacker            = self.player_2
            opponent            = self.player_1
            # opponent_position   = position_1

        # check if the players can see each other
        # can_see = self._can_see (position_1, position_2)

        # reduce the health of the opponent based on rain started by the attacker, in the previous moves
        # NOTE:
        # 1) Eval_server reduce the health of an opponent due to rain only if the attacker action is sent to eval server
        # 2) e.g. if P_1 walks into a rain started by P_2, if P_2 action timeout, P_1 will not have HP reduction
        # if does_not_have_visualizer:
        #     # this team has no concept of a rain damage
        #     pass
        # else:
        #     attacker.rain_damage(opponent, opponent_position, can_see)

        # if does_not_have_visualizer:
        #     # for bomb and AI actions we assume the opponent is always visible
        #     if action in {"basket", "soccer", "volley", "bowl", "bomb"}:
        #         can_see = True

        # perform the actual action
        if action == "gun":
            attacker.shoot(opponent, is_visible)
        elif action == "shield":
            attacker.shield()
        elif action == "reload":
            attacker.reload()
        elif action == "bomb":
            attacker.bomb(opponent, is_visible)
        elif action == "rain_damage":
            attacker.rain_damage(opponent, is_visible)
        elif action in {"basket", "soccer", "volley", "bowl"}:
            # all these have the same behaviour
            attacker.harm_AI(opponent, is_visible)
        elif action == "logout":
            # has no change in game state
            pass
        else:
            # invalid action we do nothing
            pass

    @staticmethod
    def _can_see(position_1, position_2):
        """check if the players can see each other"""
        can_see = True
        # the players cannot see each other only if one is quadrant 4 and other is in any other quadrant
        if position_1 == 4 and position_2 != 4:
            can_see = False
        elif position_1 != 4 and position_2 == 4:
            can_see = False
        return can_see


    # def __init__(self):
    #     self.p1 = Player()
    #     self.p2 = Player()

    # def get_dict(self):
    #     data = {
    #         "p1": {
    #             'hp': self.p1.hp,
    #             'bullets': self.p1.num_bullets,
    #             'bombs': self.p1.num_bombs,
    #             'shield_hp': self.p1.hp_shield,
    #             'deaths': self.p1.num_deaths,
    #             'shields': self.p1.num_shield
    #         },
    #         "p2": {
    #             'hp': self.p2.hp,
    #             'bullets': self.p2.num_bullets,
    #             'bombs': self.p2.num_bombs,
    #             'shield_hp': self.p2.hp_shield,
    #             'deaths': self.p2.num_deaths,
    #             'shields': self.p2.num_shield
    #         }
    #     }

    #     return data
    
    # def update_game_state(self, from_eval_server_queue: Queue):
    #     true_game_state = from_eval_server_queue.get()
    #     true_game_state_json = json.loads(true_game_state)

    #     self.p1.hp = true_game_state_json['p1']['hp']
    #     self.p1.num_bullets = true_game_state_json['p1']['bullets']
    #     self.p1.num_bombs = true_game_state_json['p1']['bombs']
    #     self.p1.hp_shield = true_game_state_json['p1']['shield_hp']
    #     self.p1.num_deaths = true_game_state_json['p1']['deaths']
    #     self.p1.num_shield = true_game_state_json['p1']['shields']
        
    #     self.p2.hp = true_game_state_json['p2']['hp']
    #     self.p2.num_bullets = true_game_state_json['p2']['bullets']
    #     self.p2.num_bombs = true_game_state_json['p2']['bombs']
    #     self.p2.hp_shield = true_game_state_json['p2']['shield_hp']
    #     self.p2.num_deaths = true_game_state_json['p2']['deaths']
    #     self.p2.num_shield = true_game_state_json['p2']['shields']

    #     updated_game_state = {
    #         "p1": {
    #             'hp': self.p1.hp,
    #             'bullets': self.p1.num_bullets,
    #             'bombs': self.p1.num_bombs,
    #             'shield_hp': self.p1.hp_shield,
    #             'deaths': self.p1.num_deaths,
    #             'shields': self.p1.num_shield
    #         },
    #         "p2": {
    #             'hp': self.p2.hp,
    #             'bullets': self.p2.num_bullets,
    #             'bombs': self.p2.num_bombs,
    #             'shield_hp': self.p2.hp_shield,
    #             'deaths': self.p2.num_deaths,
    #             'shields': self.p2.num_shield
    #         }
    #     }
    #     return updated_game_state