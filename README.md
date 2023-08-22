# Redis Implementation

This project demonstrates a simplified implementation of a Redis-like key-value store using Python's socket programming. It consists of a Redis server, a Redis client, and a service manager to facilitate running the server.

## Table of Contents

- [Introduction](#introduction)
- [Challenges and Approaches](#challenges-and-approaches)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Starting the Server](#starting-the-server)
  - [Running the Client](#running-the-client)
  - [Managing the Service](#managing-the-service)
- [Command List](#command-list)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Redis is an in-memory data structure store that can be used as a cache, message broker, and more. This project provides a basic version of Redis that demonstrates the client-server interaction and key-value storage. The server stores data in-memory and supports commands like `SET`, `GET`, and `KEYS`.

## Challenges and Approaches

- **Client-Server Communication:** The project establishes communication between the Redis server and multiple clients. The server listens for incoming connections and processes commands from clients.

- **Concurrency:** To handle multiple client connections, multithreading is used. Each client connection is handled in a separate thread.

- **Command Parsing:** The server parses commands received from clients, processes them, and sends back responses.

- **In-Memory Storage:** Data is stored using an in-memory dictionary within the server.

- **Service Management:** The `service.py` script provides a convenient way to start and stop the Redis server process.

- **Error Handling:** The code includes error handling to gracefully manage client disconnections and exceptions.

## Features

- Basic Redis-like functionality:
  - `SET` command to store a key-value pair.
  - `GET` command to retrieve a value by key.
  - `KEYS` command to retrieve a list of all keys stored.
  - Graceful client-server communication and error handling.
  - Service manager to start and stop the Redis server process.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/puryabzp/RedisImplementation.git
   cd redis-implementation
   ```

## Usage

### Starting the Server

1. Open a terminal and navigate to the project directory.

2. In redis_server directory run the following command to start the Redis server:

   ```bash
   python server.py
   ```

   The server will start and listen for incoming connections on `127.0.0.1:8006`.

### Running the Client

1. Open another terminal window and navigate to the project directory.

2. In redis_client directory run the following command to start the Redis client:

   ```bash
   python client.py
   ```

3. Follow the prompts to interact with the Redis server using commands such as `SET`, `GET`, `KEYS` and `EXIT`.

### Managing the Service

The `service.py` script provides a convenient way to manage the Redis server process.

1. Open a terminal and navigate to the project directory.

2. Run the following command to start the Redis service manager:

   ```bash
   python service.py
   ```

3. The service manager will start the Redis server process.

4. To stop the Redis server process, press `Ctrl + C` in the terminal running `service.py`.

## Command List

- `SET key value`: Store a key-value pair in the server.
- `GET key`: Retrieve the value associated with the given key.
- `KEYS`: Retrieve a list of all keys stored in the server.
- `EXIT`: Exit the Redis client.

## Error Handling

The implementation includes error handling to manage various scenarios gracefully, including client disconnections, invalid inputs, and exceptions.

## Contributing

Contributions are welcome! If you find any issues or have ideas for enhancements, feel free to open an issue or submit a pull request.
