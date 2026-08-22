import json, socket

class Node:
    """
    A network node with an actor model.
    """
    def __init__(self, name):
        self.finished = False
        self.name = name
        with open('network.json', 'r', encoding='utf-8') as file:
            self.network = json.load(file)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.node_address(name))
        self.run()

    def node_address(self, node_name):
        node = self.network[node_name]
        return (node["ip"], node["port"])

    def node_name(self, address):
        ip, port = address
        for name, addr in self.network.items():
            if addr["ip"] == ip and addr["port"] == port:
                return name
        return None

    def start(self):
        pass

    def send(self, msg):
        """
        Send a msg. The message is a dictionary {"to": "node_name", data:"payload"}
        """
        data = json.dumps(msg["data"]).encode('utf-8')
        dst = self.node_address(msg['to'])
        self.socket.sendto(data, dst)

    def receive(self, msg):
        pass

    def set_timeout(self, seconds):
        self.socket.settimeout(seconds)

    def on_timeout(self):
        pass

    def finish(self):
        self.finished = True

    def run(self):
        self.start()
        while not self.finished:
            try:
                data, peer = self.socket.recvfrom(4096)
                name = self.node_name(peer)
                msg = {'from': name, 'data': json.loads(data.decode("utf-8"))}
                self.receive(msg)
            except TimeoutError:
                self.on_timeout()
