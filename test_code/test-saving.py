import cv2
from pymavlink import mavutil
from save_images import get_data_save
import time
# Set up the connection to the Pixhawk
master = mavutil.mavlink_connection('udpin:localhost:14540')

master.wait_heartbeat()


cam = cv2.VideoCapture(0)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

count =0
cam.set(3, 320)
cam.set(4, 240)

shot_time = 3

current_time = time.time()
while True:
    if int(time.time() - current_time) >= shot_time:
        #set the desired resolution here
        cam.set(3, 320)
        cam.set(4, 240)
        current_time = time.time()
        ret, frame_array = cam.read()
        result, frame = cv2.imencode('.jpg', frame_array, encode_param)
        get_data_save(frame,"rgb",count,master)
        count+=1
        set_change = True
        al_set = False
        time.sleep(0.00001)

