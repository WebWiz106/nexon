import logging
import settings
import utils
import json

from usecases import upload_files_usecase
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from bson import json_util


upload_files_controller = Blueprint("upload_files", __name__)


@upload_files_controller.route("/hi",methods=["GET"])
def hello():
    return jsonify({"Message":"Hi"})



@upload_files_controller.route("/file/image",methods=["POST"])
def uploadImage():
    try:
        content = request.get_json(force=True)
        status,link = upload_files_usecase.upload_Image(content)
        return jsonify({"Status":status,"Image":link})
    except:
        return jsonify({"Status":False})
        

@upload_files_controller.route("/file/folder",methods=["POST"])
def uploadFolder():
    try:
        content = request.get_json(force=True)
        status,link = upload_files_usecase.upload_Folder(content)
        return jsonify({"Status": status, "link": link})

    except:
        return jsonify({"Status":False})
    

@upload_files_controller.route("/file/video",methods=["POST"])
def uploadVideo():
    try:
        content = request.get_json(force=True)
        status,link = upload_files_usecase.upload_Video(content)
        return jsonify({"Status":status,"Image":link})
    except:
        return jsonify({"Status":False})
    


@upload_files_controller.route("/file/videos",methods=["POST"])
def uploadVideos():
    try:
        content = request.get_json(force=True)
        status,link = upload_files_usecase.upload_Videos(content)
        return jsonify({"Status":status,"Image":link})
    except:
        return jsonify({"Status":False})
    

@upload_files_controller.route("/file/folderVideo",methods=["POST"])
def uploadVideoFolder():
    try:
        content = request.get_json(force=True)
        status,link = upload_files_usecase.upload_Folder_Video(content)
        return jsonify({"Status": status, "link": link})

    except:
        return jsonify({"Status":False})
    

@upload_files_controller.route("/file/db/data",methods=["POST"])
def uploadVid():
    try:
        content = request.get_json(force=True)
        upload_files_usecase.upload_data()
        return jsonify({"Status": True})

    except:
        return jsonify({"Status":False})