from relay_node_client import RelayNodeClient

if __name__ == "__main__":
    server_name = input("Enter server name: ")
    server_port = int(input("Enter server port: "))

    client = RelayNodeClient(server_name, server_port)

    while True:
        message = input("Enter action: ")
        if message == "exit":
            break

        client.send_message(message)
        received_message = client.receive_message()
        print(f"Received message: {received_message} from {server_name}:{server_port}")