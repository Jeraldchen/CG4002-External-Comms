import json
import sys
from evaluation_client import EvaluationClient
from game_state import GameState

if __name__ == "__main__":
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    
    client = EvaluationClient(server_name, server_port)
    client.hello()

    game_state = GameState()

    data = {
        "player_id": game_state.p1.player_id,
        "action": "reload",
        "game_state": game_state.get_dict()
    }

    client.send_message(json.dumps(data))