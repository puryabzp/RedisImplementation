import subprocess
import atexit
import threading
import signal


class RedisService:
    """A simple Redis service manager that starts and stops the Redis server."""

    def __init__(self, process=None):
        """Initialize the RedisService with a process."""
        self.process = process

    def start(self):
        """Start the Redis server process."""
        if not self.process:
            self.process = subprocess.Popen(['python', 'redis_server/server.py'],
                                            stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, text=True)
            print("Redis service started.")

    def stop(self):
        """Stop the Redis server process."""
        if self.process:
            self.process.send_signal(signal.SIGINT)
            self.process.wait()
            self.process = None
            print("Redis service stopped.")


def main():
    """Run the Redis service management."""
    redis_service = RedisService()

    atexit.register(redis_service.stop)

    try:
        redis_service.start()
        threading.Event().wait()  # Keep the main thread alive
    except KeyboardInterrupt:
        pass
    finally:
        redis_service.stop()


if __name__ == "__main__":
    main()
