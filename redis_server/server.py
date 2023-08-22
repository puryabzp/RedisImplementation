import json
import socket
import logging
import threading

logging.basicConfig(level=logging.INFO, filename="server.log", format="%(asctime)s - %(message)s")

with open('../config.json') as config_file:
    config = json.load(config_file)

server_host = config["server"]["host"]
server_port = config["server"]["port"]


class RedisServer:
    """A simple Redis server implementation that handles client connections and commands."""

    def __init__(self, host, port):
        """Initialize the RedisServer with host and port."""
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.redis = {}  # Store data in-memory dictionary
        self.client_threads = []

    def handle_client(self, client_socket, client_address):
        """Handle client connections and process commands."""
        logging.info(f"Client connected from {client_address}")

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                request = json.loads(data.decode())
                command = request["command"]
                args = request.get("args", [])

                logging.info(f"Client {client_address}: Command received: {command} {args}")

                if command == 'set':
                    key, value = args
                    self.redis[key] = value
                    response = "OK"
                elif command == 'get':
                    key = args[0]
                    response = self.redis.get(key, "Key not found")
                elif command == 'keys':
                    response = list(self.redis.keys())
                else:
                    response = "Unknown command"

                serialized_response = json.dumps(response).encode()
                client_socket.send(serialized_response)
                logging.info(f"Client {client_address}: Response sent: {response}")

            except Exception as e:
                logging.error(f"Error handling client {client_address}: {e}")
                break

        client_socket.close()
        logging.info(f"Client {client_address} disconnected.")

    def run(self):
        """Start the Redis server and listen for client connections."""
        print("Redis service started. Listening for connections...")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                logging.info(f"Connection accepted from {client_address}")
                client_thread = threading.Thread(target=self.handle_client,
                                                 args=(client_socket, client_address))
                self.client_threads.append(client_thread)
                client_thread.start()

        except KeyboardInterrupt:
            print("Shutting down server...")
            for thread in self.client_threads:
                thread.join()

            self.server_socket.close()
            print("Server stopped.")


if __name__ == "__main__":
    server = RedisServer(server_host, server_port)
    server.run()
