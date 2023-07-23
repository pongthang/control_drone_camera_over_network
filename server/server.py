import socket
import cv2
import protocol.image_uav as img_pro
import threading
import time
# import multiprocessing as mp
import _thread
import argparse
from datetime import datetime

## Argument for ip address and port of the server
parser = argparse.ArgumentParser(description = 'Server side .Send images and command to remote server and client . Control drone , rover,etc remoetley')


parser.add_argument('--ip_s', type=str, help='ip address of server for streaming video',default="localhost")

parser.add_argument('--port_sv', type=int, help='port of server for receiving video',default=8435)

parser.add_argument('--port_sc', type=int, help='port of server for chat server ',default=8080)

parser.add_argument('--port_send', type=int, help='port of server for sending the video ',default=8542)

argus = parser.parse_args()
print()
print("The values of different parameters used")
print()
print("Parameters  Values")
print()
for key,value in argus.__dict__.items():
    print(f'{key: <10}{value}')


Lock = threading.Lock()

frame = ""
metadata=""


def socket_server(host,port):
    HOST=host
    PORT=port
    global frame
    global metadata
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST,PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    data = b""
    conn,addr=s.accept()

    while True:
        
        metadata,image,data = img_pro.get_msg(data,conn)

        # print(image.shape)
        Lock.acquire()
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # print(frame.shape)
        Lock.release()
        # print(metadata)
        
        time.sleep(0.00001)


def socket_server_send(host,port):
    HOST=host
    PORT=port
    global frame
    global metadata
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST,PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    # data = b""
    conn,addr=s.accept()
    while True:
        Lock.acquire()
        result, frame_com = cv2.imencode('.jpg', frame, encode_param)
        Lock.release()

        conn.sendall(img_pro.send_msg(metadata,frame_com))
        
        # cv2.imshow('Server Side -- receiving - TCP',frame)
        # cv2.waitKey(1)
        time.sleep(0.00001)




class Server():

    def __init__(self):

        # For remembering users
        self.users_table = {}

        # Create a TCP/IP socket and bind it the Socket to the port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (argus.ip_s, argus.port_sc)  ### Ip address and port of chat server
        self.socket.bind(self.server_address)
        self.socket.setblocking(1)
        self.socket.listen(10)
        print('Starting up on {} port {}'.format(*self.server_address))
        self._wait_for_new_connections()

    def _wait_for_new_connections(self):
        while True:
            connection, _ = self.socket.accept()
            _thread.start_new_thread(self._on_new_client, (connection,))

    def _on_new_client(self, connection):
        try:
            # Declare the client's name
            client_name = connection.recv(64).decode('utf-8')
            self.users_table[connection] = client_name
            print(f'{self._get_current_time()} {client_name} joined the room !!')

            while True:
                data = connection.recv(64).decode('utf-8')
                if data != '':
                    self.multicast(data, owner=connection)
                else:
                    return 
        except:
            print(f'{self._get_current_time()} {client_name} left the room !!')
            self.users_table.pop(connection)
            connection.close()

    def _get_current_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def multicast(self, message, owner=None):
        for conn in self.users_table:
            data = f'{self._get_current_time()} {self.users_table[owner]}: {message}'
            conn.sendall(bytes(data, encoding='utf-8'))  
            




if __name__ == "__main__":
    port1 = 8542#int(input("Enter a port number: "))
    # socket_server(port1)
    server1 = threading.Thread(target=socket_server,args=(argus.ip_s,argus.port_sv,))
    server2 = threading.Thread(target=socket_server_send,args=(argus.ip_s,argus.port_send))
    server1.start()
    server2.start()
    Server()