from multiprocessing import Queue
from game_engine.game_engine import GameEngine
import json

def game_engine_process(from_vis: Queue, to_vis: Queue, p1_action: Queue, p2_action: Queue, to_eval_server: Queue, from_eval_server: Queue, to_relay_node: Queue, num_players, player_turn):
    game_engine = GameEngine(num_players)
    require_visibility_actions = ["gun","bomb","basket", "soccer", "volley", "bowl"]

    while True:
        if player_turn.value == 1:
            player_data = p1_action.get() # get action from player 1 already in json format
        elif player_turn.value == 2:
            player_data = p2_action.get()

        action = player_data["action"]
        player_id = player_data["player_id"]  
        
        num_rain_bombs = 0
        is_visible = True

        if action in require_visibility_actions: # send request to vis to check for visibility of player and number of rain bombs
            data_to_send = {
                "player_id": player_id,
                "topic": f"visibility/player{player_id}",
                "request": "check_visibility"
            }
            to_vis.put(json.dumps(data_to_send)) # send request to viz via mqtt to check for visibility
            viz_data = from_vis.get() # get visibility status from viz only after sending request
            viz_data = json.loads(viz_data)
            is_visible = viz_data["is_visible"]
            num_rain_bombs = viz_data["num_rain_bombs"]
        
        for i in range(num_rain_bombs):
            game_engine.perform_action("rain_damage", player_id, is_visible) # perform rain damage for each rain bomb

        if action == "no action": # no action from player
            ai_game_state = game_engine.game_state.get_dict()
            data_to_send = {
                "player_id": player_id,
                "action": action,
                "game_state": ai_game_state,
                "topic": "game_state"
            }
            to_vis.put(json.dumps(data_to_send))

            continue # no change in player turn
        
        game_engine.perform_action(action, player_id, is_visible)
        ai_game_state = game_engine.game_state.get_dict()
        
        data_to_send = {
            "player_id": player_id,
            "action": action,
            "game_state": ai_game_state
        }

        to_eval_server.put(json.dumps(data_to_send)) # send AI predicted game state to eval server
        true_game_state = from_eval_server.get() # get true game state from eval server
        true_game_state_json = json.loads(true_game_state)
        game_engine.game_state.player_1.set_state(true_game_state_json["p1"]["bullets"], true_game_state_json["p1"]["bombs"], true_game_state_json["p1"]["hp"], true_game_state_json["p1"]["deaths"], true_game_state_json["p1"]["shields"], true_game_state_json["p1"]["shield_hp"]) # update p1 game state with true game state
        game_engine.game_state.player_2.set_state(true_game_state_json["p2"]["bullets"], true_game_state_json["p2"]["bombs"], true_game_state_json["p2"]["hp"], true_game_state_json["p2"]["deaths"], true_game_state_json["p2"]["shields"], true_game_state_json["p2"]["shield_hp"]) # update p2 game state with true game state

        data_to_send = { 
            "player_id": player_id,
            "action": action,
            "game_state": true_game_state_json,
            "topic": "game_state"
        }

        to_vis.put(json.dumps(data_to_send)) # send true game state to viz
        to_relay_node.put(json.dumps(data_to_send)) # send true game state to relay node which sends to internal comms to show on hardware

        if player_turn == 1:
            player_turn.value = 2
        else:
            player_turn.value = 1
        

