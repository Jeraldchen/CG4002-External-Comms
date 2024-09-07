import json
from evaluation_client import EvaluationClient
from game_state import GameState

if __name__ == "__main__":
    server_name = input("Enter server name: ")
    server_port = int(input("Enter server port: "))
    
    client = EvaluationClient(server_name, server_port)
    client.hello()

    while True:
        try:
            num_players = int(input("Enter number of players (1 or 2): "))
            if num_players in [1, 2]:
                break
            else:
                print("Invalid number of players")
        except ValueError:
            print("Invalid input. Please enter a number (1 or 2)")

    while True:
        for player in range(num_players):
            player_id = player + 1
            game_state = GameState()
            action = input("Enter action: ")

            if action == "exit":
                break

            data = {
                "player_id": player_id,
                "action": action,
                "game_state": game_state.get_dict()
            }

            client.send_message(json.dumps(data))
            print(f"Sent message for player {player_id}: {action}")
            true_game_state = client.receive_message() 
            print(f"True game state from eval server: {true_game_state}")
        
        if action == "logout" or action == "exit":
            break