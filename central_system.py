
stops = ['Centraal Station', 'Station Heyendaal-1', 'Huygensgebouw', 'Erasmus', 'Spinozegebouw', 'Radboud/UMC', 'HAN', 'Station Heyendaal-2']
stop_ids = ['ad', 'bd', 'cd', 'ed', 'fd', 'gf', 'hd', 'xd']
to_stop = len(stops) * [0]

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    while True:
        station_id = ''
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                station_id += data.decode('utf8')
                if not data:
                    break
                if station_id[-2:] == '\n\n':
                    station_id = station_id[:-2]
                    break
                print(station_id)

            got_off = 0
            if station_id[:11] == 'SHUTTLE_AT_':
                station_id = station_id[11:]
                got_off = 1
            if (station_id not in stop_ids):
                conn.sendall('NOT_FOUND'.encode('utf-8'))
            else:
                if got_off == 0:
                    to_stop[stop_ids.index(station_id)] = 1
                else:
                    to_stop[stop_ids.index(station_id)] = 0
                conn.sendall('ADDED'.encode('utf-8'))

        print(station_id)
        print(to_stop)
