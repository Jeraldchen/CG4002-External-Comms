from game_engine.game_state import GameState
import json
from multiprocessing import Queue

def game_engine_process(mqtt_publish_queue: Queue, mqtt_subscribe_queue: Queue, ai_action_queue: Queue, ai_game_state_send_to_eval_server_queue: Queue, send_to_relay_node_queue_player1: Queue, send_to_relay_node_queue_player2: Queue, true_game_state_from_eval_server_queue: Queue, shoot_action_queue: Queue, got_shot_queue: Queue):
    game_state = GameState()
    bomb_thrown_count = 0
    action_count = 0
    while True:
        try: # non shoot actions
            can_see = True
            shoot_action = None
            got_shot = None

            mqtt_request_detection = {
                "topic": "visualiser/request_detection",
                "request": "true"
            }
        
            try:
                ai_message = ai_action_queue.get(timeout=0.1)
                mqtt_publish_queue.put(json.dumps(mqtt_request_detection)) # request the visualiser to detect the players
                try:
                    can_see = mqtt_subscribe_queue.get(timeout=0.5) # get the can_see from the visualiser
                except Exception:
                    can_see = "true"

                if can_see == "true":
                    can_see = True
                else:
                    can_see = False
                print(ai_message)
                player_id = ai_message['player_id']
                if player_id == 1:
                    attacker = game_state.player_1
                    opponent = game_state.player_2
                else :
                    attacker = game_state.player_2
                    opponent = game_state.player_1 
                action = ai_message['action']
                attacker.rain_damage(opponent, bomb_thrown_count, can_see)
            
                if action == "no action" or (action == "logout" and action_count < 22):
                    send_to_relay_node_queue_player1.put(json.dumps(ai_message))
                    send_to_relay_node_queue_player2.put(json.dumps(ai_message))
                    continue

                
                if action == "bomb":
                    if attacker.num_bombs > 0:
                        bomb_thrown_count += 1

                game_state.perform_action(action, player_id, can_see)
                

                ai_predicted_data = {
                    "player_id": player_id,
                    "action": action,
                    "game_state": game_state.get_dict(),
                    "topic": "ai/data"
                }
                
                ai_game_state_send_to_eval_server_queue.put(json.dumps(ai_predicted_data)) # send the predicted game state to the eval server
                # mqtt_publish_queue.put(json.dumps(ai_predicted_data)) # send the predicted game data to the visualiser first
                true_game_state = true_game_state_from_eval_server_queue.get() # get the true game state from the eval server
                true_game_state_json = json.loads(true_game_state)
                game_state.player_1.set_state(true_game_state_json['p1']['bullets'], true_game_state_json['p1']['bombs'], true_game_state_json['p1']['hp'], true_game_state_json['p1']['deaths'], true_game_state_json['p1']['shields'], true_game_state_json['p1']['shield_hp']) # update the true game state for player 1
                game_state.player_2.set_state(true_game_state_json['p2']['bullets'], true_game_state_json['p2']['bombs'], true_game_state_json['p2']['hp'], true_game_state_json['p2']['deaths'], true_game_state_json['p2']['shields'], true_game_state_json['p2']['shield_hp']) # update the true game state for player 2

                true_data = {
                    "player_id": player_id,
                    "action": action,
                    "game_state": game_state.get_dict(),
                    "topic": "true/data"
                }

                print(game_state.get_dict())

                send_to_relay_node_queue_player1.put(json.dumps(true_data)) # send the true game state to the relay node (hardware side)
                send_to_relay_node_queue_player2.put(json.dumps(true_data)) # send the true game state to the relay node (hardware side)

                mqtt_publish_queue.put(json.dumps(true_data))
                action_count += 1
                if action == "logout":
                    if action_count >= 21:
                        break
                    else:
                        continue
            except:
                # print("fail")
                pass
            
            

        except Exception as e:
            print(f"Error in game engine process: {e}")

        try:
            shoot_action = shoot_action_queue.get(timeout=0.1)
        except Exception as e:
            # print(f"Error while getting shoot action: {e}")
            continue
        
        # try:
        #     got_shot = got_shot_queue.get()
        # except Exception as e:
        #     print(f"Error while getting got shot: {e}")

        if shoot_action: # packet T
            action = "gun"
            player_id = shoot_action['player_id']
            if player_id == 1:
                    attacker = game_state.player_1
                    opponent = game_state.player_2
            else :
                attacker = game_state.player_2
                opponent = game_state.player_1 
            game_state.perform_action(action, player_id, True)
            attacker.rain_damage(opponent, bomb_thrown_count, can_see)


        
        # if got_shot: # packet I
        #     got_shot_json = json.loads(got_shot)
        #     player_id = got_shot_json['player_id']
        #     if player_id == 1:
        #         player = game_state.player_1
        #     else:
        #         player = game_state.player_2
            
        #     player.hp = got_shot_json['hp']
        #     player.num_shield = got_shot_json['numShield']
        #     player.hp_shield = got_shot_json['shieldHp']

        
        ai_predicted_data = {
            "player_id": player_id,
            "action": "gun",
            "game_state": game_state.get_dict(),
            "topic": "ai/data"
        }

        print(game_state.get_dict())

        ai_game_state_send_to_eval_server_queue.put(json.dumps(ai_predicted_data)) # send the predicted game state to the eval server
        # mqtt_publish_queue.put(json.dumps(ai_predicted_data)) # send the predicted game data to the visualiser first
        true_game_state = true_game_state_from_eval_server_queue.get() # get the true game state from the eval server
        true_game_state_json = json.loads(true_game_state)
        print(true_game_state_json)
        game_state.player_1.set_state(true_game_state_json['p1']['bullets'], true_game_state_json['p1']['bombs'], true_game_state_json['p1']['hp'], true_game_state_json['p1']['deaths'], true_game_state_json['p1']['shields'], true_game_state_json['p1']['shield_hp']) # update the true game state for player 1
        game_state.player_2.set_state(true_game_state_json['p2']['bullets'], true_game_state_json['p2']['bombs'], true_game_state_json['p2']['hp'], true_game_state_json['p2']['deaths'], true_game_state_json['p2']['shields'], true_game_state_json['p2']['shield_hp']) # update the true game state for player 2

        true_data = {
            "player_id": player_id,
            "action": action,
            "game_state": game_state.get_dict(),
            "topic": "true/data"
        }

        print(game_state.get_dict())

        send_to_relay_node_queue_player1.put(json.dumps(true_data)) # send the true game state to the relay node (hardware side)
        send_to_relay_node_queue_player2.put(json.dumps(true_data)) # send the true game state to the relay node (hardware side)

        mqtt_publish_queue.put(json.dumps(true_data))
        action_count += 1



        

        

        
