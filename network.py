import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(4096).decode()

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(data.encode('utf-8'))
            reply = self.client.recv(4096).decode()
            return reply
        except socket.error as e:
            return str(e)
