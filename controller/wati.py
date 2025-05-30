import json
import logging
from bson import json_util
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from usecases import wati_usecase

wati_controller = Blueprint('wati', __name__)

@wati_controller.route("/getWatiCred/<token>", methods=["GET"])
def getWatiCreds(token):
    try:
        status,waticred=wati_usecase.getWatiCreds(token)
        return jsonify({"Status":status,"watiCred":waticred})
    except Exception as ex:
        return jsonify({"Status":False,"watiCred":"None"})



@wati_controller.route("/addWatiCred/<token>", methods=["POST"])
def addWatiCred(token):
    try:
        data = request.get_json(force=True)
        print(data)
        status=wati_usecase.addWatiCred(token,data)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})


@wati_controller.route("/getContactList/<token>", methods=["GET"])
def getContact(token):
    try:
        status,data=wati_usecase.getContact(token)
        return jsonify({"Status":status,"data":data})
    except Exception as ex:
        return jsonify({"Status":False,"data":None})



@wati_controller.route("/getMessagees/<phoneNumber>/<token>", methods=["GET"])
def getMessages(phoneNumber,token):
    try:
        status,data=wati_usecase.getMessgae(token,phoneNumber)
        return jsonify({"Status":status,"data":data})
    except Exception as ex:
        return jsonify({"Status":False,"data":None})
    


@wati_controller.route("/sendSessionMessage/<phoneNumber>/<token>", methods=["POST"])
def sendSessionMessage(phoneNumber,token):
    try:
        messageText = request.form.get('messageText')
        print(messageText)
        status=wati_usecase.sendSessionMessage(token,phoneNumber,messageText)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})


@wati_controller.route("/changeparams/<token>", methods=["POST"])
def updateParam(token):
    try:
        data = request.get_json(force=True)
        status=wati_usecase.updateParams(token,data)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":status})

@wati_controller.route("/addContact/<token>", methods=["POST"])
def addContact(token):
    try:
        data = request.get_json(force=True)
        status=wati_usecase.addContact(token,data)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})

@wati_controller.route("/gettemplatemessages/<token>", methods=["GET"])
def getTemplateMessage(token):
    status,data=wati_usecase.getTemplateMessage(token)
    return jsonify({"Status":status,"data":data})


@wati_controller.route("/sendtemplatemessages/<token>/<phoneNumber>", methods=["POST"])
def sendTemplateMessage(token,phoneNumber):
    try:
        data = request.get_json(force=True)
        print(data)
        status=wati_usecase.sendTemplateMessage(token,phoneNumber,data)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})
