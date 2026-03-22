import socket
import pickle

class Network:
    def __init__(self, ip="127.0.0.1", port=5555, is_host=False):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)
        self.is_host = is_host

        if self.is_host:
            print("Server is started. Waiting for player connection")
            self.client.bind(self.addr)
            self.client.listen(1)
            self.conn, addr = self.client.accept()
            print(f"Player connected: {addr}")
        else:
            print("Trying to connect to server")
            self.client.connect(self.addr)
            self.conn = self.client
            print("Connected to server")

    def send(self, data):
        try:
            self.conn.send(pickle.dumps(data))
            return pickle.loads(self.conn.recv(2048))
        except Exception as e:
            print(f"Network error: {e}")
            return None