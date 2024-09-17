# from relay_node_client import RelayNodeClient

# if __name__ == "__main__":
#     server_name = input("Enter server name: ")
#     server_port = int(input("Enter server port: "))

#     client = RelayNodeClient(server_name, server_port)

#     while True:
#         message = input("Enter action: ")
#         if message == "exit":
#             break

#         client.send_message(message)
#         received_message = client.receive_message()
#         print(f"Received message: {received_message} from {server_name}:{server_port}")

from relay_node_client import RelayNodeClient
import json

if __name__ == "__main__":
    server_name = input("Enter server name: ")
    server_port = int(input("Enter server port: "))

    client = RelayNodeClient(server_name, server_port)

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
            action = input("Enter action: ")

            if action == "exit":
                break

            data = {
                "player_id": player_id,
                "action": action
            }

            client.send_message(json.dumps(data))
            print(f"Sent message for player {player_id}: {action}")
            print("###############################################")
            true_game_state = client.receive_message()
            print(f"True game state: {true_game_state}")
            print("###############################################")
        
        if action == "logout" or action == "exit":
            break