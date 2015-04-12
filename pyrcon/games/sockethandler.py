import socket

class SocketHandler:
    def __init__(self, ip, port, log):
        self.socketIp = ip
        self.socketPort = port
        self.log = log
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1)
            self.socket.connect((self.socketIp, self.socketPort))
            self.socket.setblocking(1)

            return self.socket
        except socket.error as err:
            self.log.error('[{}:{}] Unable to connect ({})'.format(self.socketIp, self.socketPort, err))
            return None

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            self.log.info('[{}:{}] has been disconnected'.format(self.socketIp, self.socketPort))

    def send_packet(self, data):
        if self.socket:
            self.socket.send(data)
        #do something if not connected?

    def receive_packet(self, receiveBuffer=""):
        if self.socket:
            receiveBuffer = self.socket.recv(4096)
            return receiveBuffer
        else:
            return receiveBuffer

    def send_and_receive(self, data, receiveBuffer=""):
        if self.socket:
            self.socket.send(data)
            receiveBuffer = self.socket.recv(4096)

            return receiveBuffer
        else:
            return receiveBuffer
