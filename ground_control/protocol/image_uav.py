import struct
import pickle
import json
def send_msg(meta,image): 
    """
    meta is dictionary and image is numpy array
    """

    meta_json = json.dumps(meta).encode("utf-8")
    meta_json_size = len(meta_json)

    image_data = pickle.dumps(image,0)
    image_size = len(image_data)

    total_payload = struct.pack(">L", meta_json_size)+meta_json+struct.pack(">L", image_size)+image_data

    """
    Total payload = byte-size of json + json of metadata + byte-size of image + image
    """

    return total_payload


def get_msg(data,socket_connection):

    """
    data is binary string and socket_connection is the connection object of client and server using socket
    """

    meta_json_size_byte__size = struct.calcsize(">L")

    while len(data)< meta_json_size_byte__size:
        data+=socket_connection.recv(4096)

    # get the size of meta data 
    

    meta_size = struct.unpack(">L",data[:meta_json_size_byte__size])[0] ## length of the metadata

    # update the data
    data=data[meta_json_size_byte__size:]
    ## extract the metadata

    while len(data)<meta_size:
        data+=socket_connection.recv(4096)
    
    # get meta data
    

    meta_byte = data[:meta_size]
    meta = json.loads(meta_byte.decode("utf-8")) ## this is the meta data

    # update the data

    data = data[meta_size:]

    ## get image size
    image_size_byte__size = struct.calcsize(">L")

    while len(data)< image_size_byte__size:
        data+=socket_connection.recv(4096)

    ## This is the image size
    image_size = struct.unpack(">L",data[:image_size_byte__size])[0]

    ## update data

    data = data[image_size_byte__size:]


    while len(data)< image_size:
        data+=socket_connection.recv(4096)
    
    ## get the image

    image_byte = data[:image_size]
    image = pickle.loads(image_byte, fix_imports=True, encoding="bytes")
    ## update data

    data = data[image_size:]


    return meta,image,data

