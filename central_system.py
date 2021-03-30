
stops = ['Centraal Station', 'Station Heyendaal-1', 'Huygensgebouw', 'Erasmus', 'Spinozegebouw', 'Radboud/UMC', 'HAN', 'Station Heyendaal-2']
stop_ids = ['ad', 'bd', 'cd', 'ed', 'fd', 'gf', 'hd', 'xd']
serial_numbers = ['ASDDEA', 'ADEFFAQ', 'XDDD']
LOCATION = {'ASDDEA': 'ad', 'ADEFFAQ': gf, 'XDDD': 'xd'}

# keep track of location for each pod
to_stop_pods = {}
current_loc = {}

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

next_id = 0
def gen_id():
    global next_id
    rand_ids = ['asdsahudiah', 'btuirebfewlfkewl', 'dsdsadew']
    next_id += 1
    return rand_ids[next_id-1]

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            res = ''
            conn, addr = s.accept()
            with conn:
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
                    
                    
                    serial_number = -1
                    if res[7:] not in serial_numbers:
                        serial_number = -1
                    else:
                        serial_number = res[7:]
                
                    if serial_number == -1:
                        # serial number not found
                        conn.sendall('ERR_SERIAL_NUMBER_NOT_FOUND'.encode('UTF-8'))
                    else:
                        next_stop = LOCATION[serial_number]
                        to_stop_pods[ID] = [0]*len(stops)
                        current_loc[ID] = next_stop
                    
                        # success
                        conn.sendall((ID).encode('UTF-8'))

                elif res[:7] == 'NXT_STP':
                    ID = -1
                    if ID[8:] not in stop_ids:
                        ID = -1
                    else:
                        ID = res[7:]
                    
                    if ID == -1:
                        # ID not found
                        conn.sendall('ERR_ID_NOT_FOUND'.encode('UTF-8'))
                    else:
                        cur_stop = current_loc[ID]
                        cur_stop_i = 0
                        for i in range(len(stop_ids)):
                            cur_stop_i = i
                            if cur_stop == stop_ids[i]:
                                break
                        next_stop_name = 'NOWHERE_NEXT'
                        for j in range(len(stop_ids)):
                            if to_stop_pods[ID][(j+cur_stop_i) % len(stop_ids)] == 1:
                                next_stop_name = stops[j]
                                break
                        # success
                        conn.sendall((next_stop_name).encode('UTF-8'))
                    
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
               

