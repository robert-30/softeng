
stops = ['Centraal Station', 'Station Heyendaal-1', 'Huygensgebouw', 'Erasmus', 'Spinozegebouw', 'Radboud/UMC', 'HAN', 'Station Heyendaal-2']
stop_ids = ['ad', 'bd', 'cd', 'ed', 'fd', 'gf', 'hd', 'xd']

# keep track of location for each pod
to_stop_pods = {}
current_loc = {}

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

next_id = 0
def gen_id():
    rand_ids = ['asdsahudiah', 'btuirebfewlfk ewl', 'dsdsadew']
    next_id += 1
    return rand_ids[next_id-1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    while True:
        res = ''
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                res += data.decode('utf8')
                if not data:
                    break
                if res[-2:] == '\n\n':
                    res = res[:-2]
                    break
                print(station_id)
            
            if res[:7] == 'ASK_ID ':
                # new POD asks for ID, send ID and register POD
                # the rest of the request should be the ID of the next stop the POD will arrive at

                ID = gen_id()
                
                next_stop = -1
                if res[7:] not in stop_ids:
                    next_stop = -1
                else:
                    next_stop = stop_ids.find(res[7:])
                
                if next_stop == -1:
                    # bus stop not found
                    conn.sendall('ERR_LOCATION_NOT_FOUND'.encode('UTF-8'))
                else:
                    to_stop_pods[ID] = [0]*len(stops)
                    current_loc[ID] = next_stop
                    
                    # success
                    conn.sendall('REGISTRATION_SUCCESSFUL')

            else:
                # otherwise: request from bus stop
                got_off = 0
                if res[:11] == 'SHUTTLE_AT_':
                    station_id = res[11:]
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
