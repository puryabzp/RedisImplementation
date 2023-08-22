import json
import os
import socket
import readline  # Add this import for arrow key support

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# Read configuration from config.json in the parent directory
with open('../config.json') as config_file:
    config = json.load(config_file)

server_host = config["server"]["host"]
server_port = config["server"]["port"]


class RedisClient:
    """A simple Redis client implementation that sends commands to the Redis server."""

    def __init__(self, host, port):
        """Initialize the RedisClient with host and port."""
        self.host = host
        self.port = port
        self.reconnect_socket()

        self.command_history = []  # Store command history

    def reconnect_socket(self):
        """Reconnect the client socket to the server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, command, *args):
        """Send a command to the server and receive the response."""
        request = {"command": command, "args": args}
        serialized_request = json.dumps(request).encode()
        self.client_socket.send(serialized_request)

        response = self.client_socket.recv(1024)
        self.client_socket.close()  # Close the socket after each command
        self.reconnect_socket()  # Reconnect the socket for the next command

        return json.loads(response.decode())

    def run(self):
        """Run the Redis client, allowing users to enter commands."""
        print("Redis client started.")
        while True:
            try:
                command = input("Enter command (SET/GET/KEYS/EXIT): ").upper()
                if command == "EXIT":
                    break
                elif command == "":  # Handle empty input
                    continue
                elif command in ["SET", "GET", "KEYS"]:
                    if command == "SET":
                        key = input("Enter key: ")
                        value = input("Enter value: ")
                        response = self.send_request('set', key, value)
                        print(response)
                    elif command == "GET":
                        key = input("Enter key: ")
                        response = self.send_request('get', key)
                        print(response)
                    elif command == "KEYS":
                        response = self.send_request('keys')  # No need to pass any args here
                        print(response)

                    # Add command to history
                    self.command_history.append(command)
                    # Limit history to last 10 commands
                    if len(self.command_history) > 10:
                        self.command_history.pop(0)

                else:
                    print("Invalid command.")

            except KeyboardInterrupt:  # Handle Ctrl+C gracefully
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

        self.client_socket.close()
        print("Redis client stopped.")


if __name__ == "__main__":
    client = RedisClient(server_host, server_port)
    client.run()
