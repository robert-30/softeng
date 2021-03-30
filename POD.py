import socket


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class POD:

    def __init__(self, location):
        self.next_station_name = location

        self.ID = self.requestID(location)

    def requestID(self, location):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(('ASK_ID ' + location + '\n\n').encode('utf-8'))
                data = s.recv(1024).decode('utf-8')
        # print(repr(data))
        return data
    
    def send_location(self, location):
        if self.ID is None:
            self.ID = self.requestID(location)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(('SET_LOC ' + ID + ' ' + location + '\n\n').encode('utf-8'))
                data = s.recv(1024)
        print(repr(data))
        return data

