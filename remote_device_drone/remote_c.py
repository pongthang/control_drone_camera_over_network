import socket
import time
import cv2
import protocol.image_uav as img_pro
import threading
import sys
from pymavlink import mavutil
from save_images import get_data_save
import numpy as np
import argparse


parser = argparse.ArgumentParser(description = 'Client side .Send images and command to remote server and client . Control drone , rover,etc remoetley')

#### Parameters needed ###################

'''
1) ip address of drone  and port for udp connection -> --ip_d --port_d
2) ip address of server for streaming video -> --ip_sv --port_sv
3) ip address of server for chat server -> --ip_sc  --port_sc
4) Resolution of the image for saving -> --r_width --r_height  
5) Client name   -> --name
'''


parser.add_argument('--name', type=str, help='Name of the device. This is for identifying specific device',default="drone")

parser.add_argument('--ip_d', type=str, help='ip address of drone  and port for udp connection',default="localhost")

parser.add_argument('--port_d', type=int, help='port of drone  and port for udp connection',default=14550)

parser.add_argument('--ip_sv', type=str, help='ip address of server for streaming video',default="localhost")

parser.add_argument('--port_sv', type=int, help='port of server for streaming video',default=8435)

parser.add_argument('--ip_sc', type=str, help='ip address of server for chat server ',default="localhost")

parser.add_argument('--port_sc', type=int, help='port of server for chat server ',default=8080)

parser.add_argument('--r_width', type=int, help='Resolution of the image for saving . Width',default=320)
parser.add_argument('--r_height', type=int, help='Resolution of the image for saving . Height',default=240)

argus = parser.parse_args()
print()
print("The values of different parameters used")
print()
print("Parameters  Values")
print()
for key,value in argus.__dict__.items():
    print(f'{key: <10}{value}')


##### to get GPS data we need to connect to pixhawk using udp###
# Set up the connection to the Pixhawk
master = mavutil.mavlink_connection(f'udpin:{argus.ip_d}:{argus.port_d}')

# Wait for the heartbeat message to ensure the connection is ready
master.wait_heartbeat()

###### 


#### to take images after an interval of time. This will store the time interval that is given by user.
shot_time = 0

###

def send_video():
    """
    This is for video streaming. This will connect to a server with the provided ip and port
    
    """
    ##### Connection to server ##############
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((argus.ip_sv,argus.port_sv )) ##### Change the ip and port using variable.
    connection = client_socket.makefile('wb')
    ############################

    #### Connect to camera. 
    cam = cv2.VideoCapture(0)
    ### encoding parameters
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


    #### Image counter to give specific names to different images.
    count =0

    #### Default resolution of camera - width - 320 pixels and height 240 pixels.
    cam.set(3, 320)
    cam.set(4, 240)


    #### To change the camera resolution when needed. It is like toggle. 
    al_set = True
    set_change = False
    global shot_time
    reset_time = True

    ########## use calibrated parameters ###############
    ## Load the intrinsic and extrinsic parameters of the camera.
    dist = np.load("dist.npy")
    mtx = np.load("mtx.npy")
    newcameramtx = np.load("newcameramtx.npy")
    roi = np.load("roi.npy")

    while True:
        
        ### if the user give non-zero time interval for taking photos for saving "shot_time" 
        ### should be greater than zero.
        if shot_time>0:
            if reset_time:
                current_time = time.time()
                reset_time = False
            print("shot is got")

            ##### If the time interval is satified
            if int(time.time() - current_time) >= shot_time:

                print("saving the images")
                #set the desired resolution here. Take as input.  *****************************
                cam.set(3, argus.r_width)
                cam.set(4, argus.r_height)
                #current_time = time.time()
                ret, frame_array = cam.read()
                
                ########## use calibrated parameters ###############
                ## This will matigate the distortion.
                frame_array = cv2.undistort(frame_array, mtx, dist, None, newcameramtx)
                x, y, w, h = roi
                dst = frame_array[y:y+h, x:x+w]
                #### Color calibration will be added here !!

                
                ### Converting from numpy matrix or array to "jpg" image format.
                result, frame = cv2.imencode('.jpg', dst, encode_param)


                #### Save the data here.
                ### Here the drone connector "master" and the counter are given as agruments also.
                ### Here "rgb" image is set as default.
                get_data_save(frame,"rgb",count,master)


                #### Image counter
                count+=1

                #### To change the camera resolution when needed. It is like toggle.
                set_change = True
                al_set = False
                reset_time =True
                time.sleep(0.00001)
                continue
        

        ### Change the resolution to the default values and continue 
        if (not al_set and set_change):
            cam.set(3, 320)
            cam.set(4, 240)
            al_set = True


        ret, frame_array = cam.read()

        ########## use calibrated parameters ###############
        ## This will matigate the distortion.
        frame_array = cv2.undistort(frame_array, mtx, dist, None, newcameramtx)
        x, y, w, h = roi
        dst = frame_array[y:y+h, x:x+w]
        #### Color calibration will be added here !!

        
        ### Converting from numpy matrix or array to "jpg" image format.
        result, frame = cv2.imencode('.jpg', dst, encode_param)

        #result, frame = cv2.imencode('.jpg', frame_array, encode_param)
        
        #Meta data - put any data that should be sent along with images
        lat=10
        lon=10
        alt=10
        metadata={

                "lat":lat,
                'lon':lon,
                'alt':alt,
                'shot_time':shot_time

            }


        client_socket.sendall(img_pro.send_msg(metadata,frame))
        # message = client_socket.recv(1024).decode('ascii')

        # cv2.imshow('Client Side !! Sending - TCP',frame_array)
        cv2.waitKey(1)

        # time.sleep(0.3) #delay
    cam.release()


### Start a new thread for sending video stream to the server.
send_video_p = threading.Thread(target=send_video)
send_video_p.start()


message_g = ""


class Client():

    def __init__(self, client_name):

        # Create a TCP/IP socket and connect the socket to the port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (argus.ip_sc, argus.port_sc)  ### Change the ip and port the chat server.
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
        global message_g
        while True:
            try:
                message_g = self.socket.recv(1024).decode("utf-8")
                print(message_g)
            except:
                self.socket.close()
                return



#client_name = "drone"
Client(argus.name)

while True:
    ## the incoming messages and the find out commands 
    if "take_shot" in message_g:
        msg_com = message_g.strip().split(" ")
        if len(msg_com)>3:
            shot_time = int(msg_com[3])
            print(shot_time)
        # print(msg_com)
    
    time.sleep(0.2)
