from relay_node_server import RelayNodeServer

if __name__ == "__main__":
    server_port = int(input("Enter server port: "))
    server = RelayNodeServer(server_port)
    server.run()