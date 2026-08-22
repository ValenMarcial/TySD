from node import Node
import time

class Ping(Node):
    def __init__(self):
        self.msgs_sent = 0
        super().__init__("ping")

    def start(self):
        self.send_ping()

    def send_ping(self):
        print("Sending PING to pong node...")
        self.send({"to": "pong", "data": "PING"})
        self.msgs_sent += 1
        time.sleep(1)

    def receive(self, msg):
        print(f"Received {msg}")
        if self.msgs_sent < 5:
            self.send_ping()
        else:
            self.finish()

if __name__ == "__main__":
    Ping()
