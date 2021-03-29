import socket

class Station:

    def __init__(self, name, id_code):
        self.name = name
        self.id_code = id_code

    def callshuttle(self):
        print("Beep boop. Dialing... Hi, it's %s! Come over, please!" % self.name)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 65432))
                s.sendall((self.id_code+'\n\n').encode('utf-8'))
                data = s.recv(1024)
        print(repr(data))
        pass
    
    def shuttle_is_here(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 65432))
                s.sendall((('SHUTTLE_AT_%s'+'\n\n')%self.id_code).encode('utf-8'))
                data = s.recv(1024)


stat = Station('Station Heyendaal', 'xd')
stat.shuttle_is_here()