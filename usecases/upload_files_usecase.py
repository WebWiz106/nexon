import utils
import hashlib
import pymongo
import settings
import logging
import json
import io
import base64
import boto3
import uuid
import zipfile
import os
from PIL import Image
import subprocess


from bson import json_util
from datetime import datetime
from model.user import User
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

from utils import db
client = boto3.client('s3')


def domainofToken(token):
    ndid = utils.get_ndid(token)
    profile = db.Zucks_profile.find_one({"uId": ndid})
    return profile.get('domain')


def GenerateNewName():
    date = uuid.uuid4()
    return date



def convert_jpg_to_webp_local(input_path, folder_name, filename, output_path="D:/webp/", quality=90):
    try:
        image_bytes = base64.b64decode(input_path)
        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert('RGB')
        output_path = output_path+filename
        img.save(output_path, format='WEBP', quality=quality)
        print(f"Conversion successful. WebP image saved at {output_path}")
        return True
    except Exception as e:
        print("ERROR OCUURED")
        # print(f"Conversion failed: {e}")
        return False


def convert_jpg_to_webp_buffer(input_path, filename, output_path="D:/webp/", quality=90):
    try:
        image_bytes = base64.b64decode(input_path)
        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert('RGB')
        buffer = io.BytesIO()
        output_path = output_path+filename
        img.save(buffer, format='WEBP', quality=quality)
        buffer.seek(0,0)
        return buffer
        print(f"Conversion successful. WebP image saved at {output_path}")
        return True
    except Exception as e:
        print("ERROR OCUURED")
        # print(f"Conversion failed: {e}")
        return False


def upload_Image(edit_details):
    try:
        token = edit_details.get("token")
        ndid = utils.get_ndid(token)
        domain = domainofToken(token)

        base64_string = edit_details.get("image")

        buffer = convert_jpg_to_webp_buffer(input_path=base64_string,filename="test")
        # image_bytes = base64.b64decode(base64_string)

        webp_filename = str(GenerateNewName()) + ".webp"
        key_name = domain + "/images/" + webp_filename

        # Replace with your S3 region
        s3 = boto3.client('s3', region_name='ap-south-1')
        s3.upload_fileobj(
            Fileobj=buffer,
            Bucket='eazotel-client-images',
            Key=key_name,
            ExtraArgs={'ContentType': "image/webp"}
        )

        Live_link = "https://eazotel-client-images.s3.ap-south-1.amazonaws.com/" + key_name
        print(Live_link)
       
        return True , Live_link

    except Exception as e:
        print(e)
        return False, "No Image"


def upload_Folder(edit_details):
    try:
        token = edit_details.get("token")
        folderName = edit_details.get("folderName")
        base64_string = edit_details.get("image")
        domain = domainofToken(token)
        webp_filename = str(GenerateNewName()) + ".webp"
        key_name = domain + "/images/" + folderName+"/" + webp_filename
        buffer = convert_jpg_to_webp_buffer(input_path=base64_string, filename=str(webp_filename))

        s3 = boto3.client('s3', region_name='ap-south-1')  # Replace with your S3 region
        s3.upload_fileobj(
            Fileobj=buffer,
            Bucket='eazotel-client-images',
            Key=key_name,
            ExtraArgs={'ContentType': "image/webp"}
        )
        # Live_link = "https://eazotel-client-images.s3.ap-south-1.amazonaws.com/" + key_name

        return True, "Live_link"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False, "Error uploading folder"


def convert_mp4_to_webm(base64string):
    try:
        # Decode base64 string to bytes
        video_bytes = base64.b64decode(base64string)

        # Write video bytes to a temporary file
        temp_filename = 'temp.mp4'
        with open(temp_filename, 'wb') as temp_file:
            temp_file.write(video_bytes)

        # Convert MP4 to WebM using ffmpeg
        webm_filename = 'output.webm'
        subprocess.run(['ffmpeg', '-i', temp_filename, webm_filename])

        # Read the converted WebM file
        with open(webm_filename, 'rb') as webm_file:
            webm_bytes = webm_file.read()

        return webm_bytes

    except Exception as e:
        print(f"Conversion failed: {e}")
        return False


def convert_mp4_to_webm_local(base64string, output_dir='D:/webp'):
    try:
        # Decode base64 string to bytes
        video_bytes = base64.b64decode(base64string)

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Write video bytes to a temporary file
        temp_filename = os.path.join(output_dir, 'temp.mp4')
        with open(temp_filename, 'wb') as temp_file:
            temp_file.write(video_bytes)

        print(f"Saved MP4 to: {temp_filename}")

        # Convert MP4 to WebM using ffmpeg
        webm_filename = os.path.join(output_dir, 'output.webm')
        subprocess.run(['ffmpeg', '-i', temp_filename, webm_filename])

        print(f"Converted to WebM: {webm_filename}")

        # Read the converted WebM file
        with open(webm_filename, 'rb') as webm_file:
            webm_bytes = webm_file.read()

        print(f"Read WebM file: {webm_filename}")
        return webm_bytes

    except Exception as e:
        print(f"Conversion failed: {e}")
        return False


def upload_Video(edit_details):
    try:
        token = edit_details.get("token")
        # Include logic to get ndid and domain based on your requirements
        # ndid = utils.get_ndid(token)
        # domain = domainofToken(token)

        base64_string = edit_details.get("video")

        webm_bytes = convert_mp4_to_webm_local(base64_string)

        if not webm_bytes:
            return False, "Conversion failed"

        # Replace with your S3 region
        # s3 = boto3.client('s3', region_name='ap-south-1')

        # # Replace 'your-bucket-name' with your S3 bucket name
        # bucket_name = 'your-bucket-name'
        # key_name = 'videos/output.webm'  # Update with your desired S3 key

        # s3.upload_fileobj(
        #     Fileobj=io.BytesIO(webm_bytes),
        #     Bucket=bucket_name,
        #     Key=key_name,
        #     ExtraArgs={'ContentType': "video/webm"}
        # )

        # live_link = f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{key_name}"
        # print(live_link)
        return True, "live_link"

    except Exception as e:
        print(e)
        return False, "No Video"


def upload_Videos(edit_details):
    try:
        token = edit_details.get("token")
        # Include logic to get ndid and domain based on your requirements
        # ndid = utils.get_ndid(token)
        # domain = domainofToken(token)

        base64_string = edit_details.get("video")

        webm_bytes = convert_mp4_to_webm_local(base64_string)

        if not webm_bytes:
            return False, "Conversion failed"

        # Replace with your S3 region
        # s3 = boto3.client('s3', region_name='ap-south-1')

        # # Replace 'your-bucket-name' with your S3 bucket name
        # bucket_name = 'your-bucket-name'
        # key_name = 'videos/output.webm'  # Update with your desired S3 key

        # s3.upload_fileobj(
        #     Fileobj=io.BytesIO(webm_bytes),
        #     Bucket=bucket_name,
        #     Key=key_name,
        #     ExtraArgs={'ContentType': "video/webm"}
        # )

        # live_link = f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{key_name}"
        # print(live_link)
        return True, "live_link"

    except Exception as e:
        print(e)
        return False, "No Video"

def upload_Folder_Video(edit_details):
    try:
        token = edit_details.get("token")
        folderName = edit_details.get("folderName")
        base64_string = edit_details.get("image")
        domain = domainofToken(token)
        webp_filename = str(GenerateNewName()) + ".webp"
        key_name = domain + "/images/" + folderName+"/" + webp_filename
        buffer = convert_jpg_to_webp_buffer(input_path=base64_string, folder_name=str(
            folderName), filename=str(webp_filename))

        s3 = boto3.client('s3', region_name='ap-south-1')  # Replace with your S3 region
        s3.upload_fileobj(
            Fileobj=buffer,
            Bucket='eazotel-client-images',
            Key=key_name,
            ExtraArgs={'ContentType': "image/webp"}
        )
        # Live_link = "https://eazotel-client-images.s3.ap-south-1.amazonaws.com/" + key_name

        return True, "Live_link"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False, "Error uploading folder"


def upload_data():
    rooms = db.Rooms.find()
    for i in rooms:

        db.Rooms.find_one_and_update({"ndid":i.get("ndid"),"hId":i.get("hId"),"roomType":i.get("roomType")},{"$set":{
            "roomNumbers":[],
            "inMaintanance":[]
        }})

