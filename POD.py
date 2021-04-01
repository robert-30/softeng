import socket


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class POD:

    def __init__(self, serial_number):
        self.next_station_name = serial_number

        self.ID = self.requestID(serial_number)

    def requestID(self, serial_number):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(('ASK_ID ' + serial_number + '\n\n').encode('utf-8'))
                data = s.recv(1024).decode('utf-8')
        # print(repr(data))
        return data
    
    def get_next_stop(self):
        if self.ID is None:
            raise NameError('This POD is not registered!')
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(('NXT_STP ' + ID + '\n\n').encode('utf-8'))
                data = s.recv(1024)
        print(data)
