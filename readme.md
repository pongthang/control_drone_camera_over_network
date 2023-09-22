# Sending Images using TCP in real-time
Communicating Drone over a network for long range operation is very crucial for surveillance and mapping works. This same code or the concept can be used for other teleoperation works like controlling a robot arm from a distance, etc. Here a commandline tools is developed to do the same. 

# Features:
- It has video streaming from a remote client to ground station client.
- Can send command from ground station to remote client.
- Can save images in specified regular intervals.

# Requirements:

- pymavlink
- exif
- opencv
- numpy



# Project structure

The project is divided into three sections.

- Server 
- Remote client 
- Ground Control

## Server 

<p> This folder contains the server code.
Run the server using the following command.

```
$ cd server
$ python3 server.py --ip_sv 172.168.14.124 
```

This will start the server in the provided ip. The ip should be the ip address of the server. Change "172.168.14.124" with your server ip address. 

- Server listen a video streaming at port 8435
- Server send the same video in the port 8542
- Server host a chat at port 8080 .  This allows the QC send command to drone or remote device 

</p>

<b> Remote Client </b>

<p> This folder contains the remote client code. Run the client using the following command 
 
```
$ cd remote_device_drone
$ python3 remote_c.py --ip_sv 172.168.14.124 --ip_sc 172.168.14.124
```
This will start a client. Change "172.168.14.124" with your server ip. "--ip_sv" for your video streaming and "--ip_sc" for your chat server

- It sends the realtime video stream to the server with ip "--ip_sv 172.168.14.124" at the port 8435
- It can recieve command from a chat server at port 8080

</p>


<b> Ground Control</b>

<p>
This contains the ground control code. It can send commands and recieve video feed.

Run the ground control using the following command.
```
$ cd ground_control
$ python3 ground-c.py --ip_sv 172.168.14.124 --ip_sc 172.168.14.124
```
This will start a ground control client. Change "172.168.14.124" with your server ip. "--ip_sv" for your video streaming and "--ip_sc" for your chat server

- It recieves the realtime video stream to the server with ip "--ip_sv 172.168.14.124" at the port 8542
- It can send command from a chat server at port 8080
- Example
  ```
  take_shot 3
  ```
  This will save image for every 3 seconds.
</p>
