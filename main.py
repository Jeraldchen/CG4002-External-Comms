import json
import sys
from encryption import AESEncryption
from evaluation_client import EvaluationClient
from player import Player

if __name__ == "__main__":
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    
    client = EvaluationClient(server_name, server_port)
    client.hello()

    player = Player(1, 100, 6, 2, 30, 0, 3)

    data = {
        "player_id": player.player_id,
        "action": "reload",
        "game_state": player.get_dict()
    }

    client.send_message(json.dumps(data))