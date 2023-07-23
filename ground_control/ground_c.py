import socket
# import time
import cv2
import protocol.image_uav as img_pro
import threading
import sys

import argparse


parser = argparse.ArgumentParser(description = 'Ground control side .Send images and command to remote server and client . Control drone , rover,etc remoetley')

#### Parameters needed ###################

'''
1) ip address of drone  and port for udp connection -> --ip_d --port_d
2) ip address of server for streaming video -> --ip_sv --port_sv
3) ip address of server for chat server -> --ip_sc  --port_sc
4) Resolution of the image for saving -> --r_width --r_height  
5) Client name   -> --name
'''


parser.add_argument('--name', type=str, help='Name of the device. This is for identifying specific device',default="QC")

# parser.add_argument('--ip_d', type=str, help='ip address of drone  and port for udp connection',default="localhost")

# parser.add_argument('--port_d', type=int, help='port of drone  and port for udp connection',default=14550)

parser.add_argument('--ip_sv', type=str, help='ip address of server for receiving streaming video',default="localhost")

parser.add_argument('--port_sv', type=int, help='port of server for receiving streaming video',default=8542)

parser.add_argument('--ip_sc', type=str, help='ip address of server for chat server ',default="localhost")

parser.add_argument('--port_sc', type=int, help='port of server for chat server ',default=8080)

# parser.add_argument('--r_width', type=int, help='Resolution of the image for saving . Width',default=320)
# parser.add_argument('--r_height', type=int, help='Resolution of the image for saving . Height',default=240)

argus = parser.parse_args()
print()
print("The values of different parameters used")
print()
print("Parameters  Values")
print()
for key,value in argus.__dict__.items():
    print(f'{key: <10}{value}')





def get_video():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((argus.ip_sv,argus.port_sv))
    connection = client_socket.makefile('wb')
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    data = b""
    while True:
        metadata,image,data = img_pro.get_msg(data,client_socket)

        # print(image.shape)
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # print(frame.shape)
        # print(metadata)
        

        cv2.imshow('Server Side -- receiving - TCP',frame)
        cv2.waitKey(1)

video_p = threading.Thread(target=get_video)
video_p.start()


class Client():

    def __init__(self, client_name):

        # Create a TCP/IP socket and connect the socket to the port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (argus.ip_sc, argus.port_sc)
        self.socket.connect(self.server_address)
        self.socket.setblocking(1)

        self.client_name = client_name
        send = threading.Thread(target=self._client_send)
        send.start()
        receive = threading.Thread(target=self._client_receive)
        receive.start()

    def _client_send(self):
        self.socket.send(bytes(self.client_name, encoding='utf-8'))  
        while True:
            try:
                c = input()
                sys.stdout.write("\x1b[1A\x1b[2K") # Delete previous line
                self.socket.send(bytes(c, encoding='utf-8')) 
            except:
                self.socket.close()
                return

    def _client_receive(self):
        while True:
            try:
                print(self.socket.recv(1024).decode("utf-8"))
            except:
                self.socket.close()
                return

Client(argus.name)