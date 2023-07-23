import argparse

parser = argparse.ArgumentParser(description = 'Server side .Send images and command to remote server and client . Control drone , rover,etc remoetley')

#### Parameters needed ###################

'''
1) IP address of server and port
'''


parser.add_argument('--name', type=str, help='Name of the device. This is for identifying specific device',default="drone")

parser.add_argument('--ip_d', type=str, help='ip address of drone  and port for udp connection',default="localhost")

parser.add_argument('--port_d', type=int, help='port of drone  and port for udp connection',default=14550)

parser.add_argument('--ip_sv', type=str, help='ip address of server for streaming video',default="localhost")

parser.add_argument('--port_sv', type=int, help='port of server for streaming video',default=8435)

parser.add_argument('--ip_sc', type=str, help='ip address of server for chat server ',default="localhost")

parser.add_argument('--port_sc', type=int, help='port of server for chat server ',default=8000)

parser.add_argument('--r_width', type=int, help='Resolution of the image for saving . Width',default=320)
parser.add_argument('--r_height', type=int, help='Resolution of the image for saving . Height',default=240)

args = parser.parse_args()

print()
print("Parameters  Values")
print()
for key,value in args.__dict__.items():
    print(f'{key: <10}{value}')