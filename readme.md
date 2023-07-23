# Sending Images using TCP in real-time

# How to run the program

* Install opencv  - to read images from cameras or from a folder

# Project structure

The project is divided into three sections.

- Server 
- Remote client 
- Ground Control

<b>Server </b>

<p> This folder contains the server code.
Run the server using the following command.

$ cd server

$ python3 server.py --ip_sv 172.168.14.124 

This will start the server in the provided ip. The ip should be the ip address of the server. Change "172.168.14.124" with your server ip address. 

- Server listen a video streaming at port 8435
- Server send the same video in the port 8542
- Server host a chat at port 8080 .  This allows the QC send command to drone or remote device 

</p>

<b> Remote Client </b>

<p> This folder contains the remote client code. Run the client using the following command 

$ cd remote_device_drone

$ python3 remote_c.py --ip_sv 172.168.14.124 --ip_sc 172.168.14.124 

This will start a client. Change "172.168.14.124" with your server ip. "--ip_sv" for your video streaming and "--ip_sc" for your chat server

- It sends the realtime video stream to the server with ip "--ip_sv 172.168.14.124" at the port 8435
- It can recieve command from a chat server at port 8080

</p>


<b> Ground Control</b>

<p>
This contains the ground control code. It can send commands and recieve video feed.

Run the ground control using the following command.

$ cd ground_control

$ python3 ground-c.py --ip_sv 172.168.14.124 --ip_sc 172.168.14.124

This will start a ground control client. Change "172.168.14.124" with your server ip. "--ip_sv" for your video streaming and "--ip_sc" for your chat server

- It recieves the realtime video stream to the server with ip "--ip_sv 172.168.14.124" at the port 8542
- It can send command from a chat server at port 8080
</p>
