import socket
 
stops = ['Centraal Station', 'Station Heyendaal-1', 'Huygensgebouw', 'Erasmus', 'Spinozegebouw', 'Radboud/UMC', 'HAN', 'Station Heyendaal-2']
stop_ids = ['ad', 'bd', 'cd', 'ed', 'fd', 'gf', 'hd', 'xd']
serial_numbers = ['ASDDEA', 'ADEFFAQ', 'XDDD']
LOCATION = {'ASDDEA': 'ad', 'ADEFFAQ': 'gf', 'XDDD': 'xd'}
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


class Central_system:
# keep track of location for each pod
	to_stop_pods = {}
	current_loc = {} 
	next_id = 0
	
	def gen_id(self):
	    rand_ids = ['asdsahudiah', 'btuirebfewlfkewl', 'dsdsadew']
	    self.next_id += 1
	    return rand_ids[self.next_id-1]

	def server(self):
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

                           ID = self.gen_id()
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
                               self.to_stop_pods[ID] = [0]*len(stops)
                               self.current_loc[ID] = next_stop
		            
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
                                cur_stop = self.current_loc[ID]
                                cur_stop_i = 0
                                for i in range(len(stop_ids)):
                                    cur_stop_i = i
                                    if cur_stop == stop_ids[i]:
                                        break 
                                    next_stop_name = 'NOWHERE_NEXT'
                                for j in range(len(stop_ids)):
                                    if self.to_stop_pods[ID][(j+cur_stop_i) % len(stop_ids)] == 1:
                                        next_stop_name = stops[j]
                                        break
		                # success
                                conn.sendall((next_stop_name).encode('UTF-8'))
		            
                       else:
		            # otherwise: request from bus stop
                           got_off = 0
                           station_id = -1
                           print(res)
                           if res[:11] == 'SHUTTLE_AT ': 
                               station_id = res[11:]
                               got_off = 1
                           elif res[:16] == 'REQUEST_SHUTTLE ':
                               station_id = res[16:]
                           if (station_id not in stop_ids):
                               print(station_id)
                               conn.sendall('ERR_STOP_NOT_FOUND'.encode('utf-8'))
                           else:
                               if got_off == 0:
                                   self.to_stop_pods[station_id] = 1
                               else:
                                   self.to_stop_pods[station_id] = 0
                               print(self.to_stop_pods)
                               conn.sendall('ADDED'.encode('utf-8'))
               

