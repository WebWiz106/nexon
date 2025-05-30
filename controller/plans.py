import logging
import settings
import utils
import json

from flask import Blueprint,request,jsonify
from flask_cors import CORS,cross_origin
from usecases import eazotel_usecase,plans_usecase
from usecases.booking_usecase import check_no_rooms
from datetime import datetime,timedelta
from bson import json_util


plan_controller = Blueprint("plans", __name__)


@plan_controller.route("/hi")
def hello():
    return "hi!!"

@plan_controller.route("/createplan",methods=["POST"])
def addplans():
    try:
        booking_details = request.get_json(force=True)
        status,message = plans_usecase.addplanEazotel(booking_details)
        return jsonify({"status":status,"Message":message})
    except:
        return jsonify({"status":False})
    
@plan_controller.route("/deleteplan",methods=["POST"])
def deleteplans():
    try:
        booking_details = request.get_json(force=True)
        status,message = plans_usecase.deleteplanEazotel(booking_details)
        return jsonify({"status":status,"Message":message})
    except:
        return jsonify({"status":False})