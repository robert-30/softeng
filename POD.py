import socket

class POD:

    def __init__(self, location):
        self.next_station_name = location

        self.ID = self.requestID(location)

    def requestID(self, location):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 65432))
                s.sendall(('ASK_ID ' + location + '\n\n').encode('utf-8'))
                data = s.recv(1024)
        print(repr(data))
        return data
    
    def send_location(self, location):
        if self.ID is None:
            self.ID = self.requestID(location)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 65432))
                s.sendall(('SET_LOC ' + ID + ' ' + location + '\n\n').encode('utf-8'))
                data = s.recv(1024)
        print(repr(data))
        return data

