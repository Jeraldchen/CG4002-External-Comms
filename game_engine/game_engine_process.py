from game_engine.game_state import GameState
import json
from multiprocessing import Queue

def game_engine_process(mqtt_publish_queue: Queue, mqtt_subscribe_queue: Queue, ai_action_queue: Queue, ai_game_state_send_to_eval_server_queue: Queue, send_to_relay_node_queue: Queue, true_game_state_from_eval_server_queue: Queue, shoot_action_queue: Queue, got_shot_queue: Queue):
    game_state = GameState()
    while True:
        can_see = False
        shoot_action = None
        got_shot = None
        try: # non shoot actions
            can_see = mqtt_subscribe_queue.get() # get the can_see from the visualiser
            ai_message = ai_action_queue.get()
            ai_message_json = json.loads(ai_message)
            player_id = ai_message_json['player_id']
            action = ai_message_json['action']
            if action == "no action":
                continue
            game_state.perform_action(action, player_id, can_see)

            ai_predicted_data = {
                "player_id": player_id,
                "action": action,
                "game_state": game_state.get_dict()
            }

            ai_game_state_send_to_eval_server_queue.put(json.dumps(ai_predicted_data)) # send the predicted game state to the eval server
            mqtt_publish_queue.put(json.dumps(ai_predicted_data)) # send the predicted game data to the visualiser first
            true_game_state = true_game_state_from_eval_server_queue.get() # get the true game state from the eval server
            true_game_state_json = json.loads(true_game_state)
            game_state.player_1.set_state(true_game_state_json['p1']['bullets'], true_game_state_json['p1']['bombs'], true_game_state_json['p1']['hp'], true_game_state_json['p1']['deaths'], true_game_state_json['p1']['shields'], true_game_state_json['p1']['shield_hp']) # update the true game state for player 1
            game_state.player_2.set_state(true_game_state_json['p2']['bullets'], true_game_state_json['p2']['bombs'], true_game_state_json['p2']['hp'], true_game_state_json['p2']['deaths'], true_game_state_json['p2']['shields'], true_game_state_json['p2']['shield_hp']) # update the true game state for player 2

            true_data = {
                "player_id": player_id,
                "action": action,
                "game_state": game_state.get_dict()
            }

            send_to_relay_node_queue.put(json.dumps(true_data)) # send the true game state to the relay node (hardware side)
            mqtt_publish_queue.put(json.dumps(true_data))

            if action == "logout":
                break

        except Exception as e:
            print(f"Error in game engine process: {e}")

        try:
            shoot_action = shoot_action_queue.get()
        except Exception as e:
            print(f"Error while getting shoot action: {e}")
        
        try:
            got_shot = got_shot_queue.get()
        except Exception as e:
            print(f"Error while getting got shot: {e}")

        if shoot_action: # packet T
            shoot_action_json = json.loads(shoot_action)
            player_id = shoot_action_json['player_id']
            if player_id == 1:
                player = game_state.player_1
            else:
                player = game_state.player_2
            
            player.num_bullets = shoot_action_json['ammoCount']
        
        if got_shot: # packet I
            got_shot_json = json.loads(got_shot)
            player_id = got_shot_json['player_id']
            if player_id == 1:
                player = game_state.player_1
            else:
                player = game_state.player_2
            
            player.hp = got_shot_json['hp']
            player.num_shield = got_shot_json['numShield']
            player.hp_shield = got_shot_json['shieldHp']

        
        ai_predicted_data = {
            "player_id": player_id,
            "action": "shoot",
            "game_state": game_state.get_dict()
        }

        ai_game_state_send_to_eval_server_queue.put(json.dumps(ai_predicted_data)) # send the predicted game state to the eval server
        mqtt_publish_queue.put(json.dumps(ai_predicted_data)) # send the predicted game data to the visualiser first
        true_game_state = true_game_state_from_eval_server_queue.get() # get the true game state from the eval server
        true_game_state_json = json.loads(true_game_state)
        game_state.player_1.set_state(true_game_state_json['p1']['bullets'], true_game_state_json['p1']['bombs'], true_game_state_json['p1']['hp'], true_game_state_json['p1']['deaths'], true_game_state_json['p1']['shields'], true_game_state_json['p1']['shield_hp']) # update the true game state for player 1
        game_state.player_2.set_state(true_game_state_json['p2']['bullets'], true_game_state_json['p2']['bombs'], true_game_state_json['p2']['hp'], true_game_state_json['p2']['deaths'], true_game_state_json['p2']['shields'], true_game_state_json['p2']['shield_hp']) # update the true game state for player 2

        true_data = {
            "player_id": player_id,
            "action": action,
            "game_state": game_state.get_dict()
        }

        send_to_relay_node_queue.put(json.dumps(true_data)) # send the true game state to the relay node (hardware side)
        mqtt_publish_queue.put(json.dumps(true_data))



        

        

        
