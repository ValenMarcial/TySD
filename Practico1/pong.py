from node import Node

class Pong(Node):
    def __init__(self):
        super().__init__("pong")

    def receive(self, msg):
        print(f"Message {msg} received!")
        print("Responding PONG...")
        self.send({"to": "ping", "data": "PONG"})

if __name__ == "__main__":
    Pong()
