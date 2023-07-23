import os
from datetime import datetime
import time
import exif

def save_img(image,image_type,count):
    pwd = os.getcwd()
    pre_date_time = datetime.now()
    dirname = f"{pre_date_time.year}_{pre_date_time.month}_{pre_date_time.day}_{pre_date_time.hour}_{pre_date_time.minute}"

    dirname_rgb = dirname+"/rgb"
    dirname_multi = dirname+"/multi"

    path_rgb = os.path.join(pwd,dirname_rgb)
    path_multi = os.path.join(pwd,dirname_multi)

    try:
        os.makedirs(path_rgb,exist_ok=True) 
        os.makedirs(path_multi,exist_ok=True)

    except OSError as error:
        print(f"Directory {dirname_rgb} and {dirname_multi} can't be created!! ")

    if image_type =="rgb":
        filename = f'{dirname_rgb}/image_{count}.jpg'
    else:
        filename = f'{dirname_multi}/image_{count}.jpg'
    
    try:
        with open(filename,'wb') as new_file:
            new_file.write(image.get_file())
    except:
        print("Connot save file")


def insert_meta_data(image,meta_data):

    """
    Inserting GPS data as exif data
    """

    exif_jpg = exif.Image(image.tobytes())

    exif_jpg['gps_latitude'] = meta_data['lat']
    exif_jpg['gps_longitude'] = meta_data['lon']
    exif_jpg['gps_altitude'] = meta_data['alt']

    return exif_jpg

def get_gps(master):
    gps_data = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)

    # Extract the GPS coordinates and height from the data
    lat = gps_data.lat / 10000000.0
    lon = gps_data.lon / 10000000.0
    alt = gps_data.alt / 1000.0

    return {"lat":lat,"lon":lon,"alt":alt}


def get_data_save(image,image_type,count,master):

    """
    This will read the data like GPS coordinates available in master and embedded to the jpg image as exif data,
    Then , a new filename will be generated according to the counter and datetime.
    Finally the images will be save in the current working directory.
    
    """
    metadata = get_gps(master)
    exif_image = insert_meta_data(image,metadata)
    save_img(exif_image,image_type,count)


