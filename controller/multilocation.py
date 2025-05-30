import logging
import settings
import utils
import json

from flask import Blueprint,request,jsonify
from bson import json_util
from usecases import multilocation_usecase
multilocation_controller = Blueprint('multlocation', __name__)


@multilocation_controller.route("/hi",methods=["GET"])
def hello():
    return json.dumps({"message": "hi"})


@multilocation_controller.route("/findlocations/dashboard/<token>",methods=["GET"])
def findLocationsOfHotel_Dashboard(token):
    try:
        ndid = utils.get_ndid(token)
        status,details= multilocation_usecase.find_locations_of_hotel(ndid)
        return jsonify({"Status":status,"Locations":json.loads(json_util.dumps(details))})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    

@multilocation_controller.route("/findlocations/engine/<ndid>",methods=["GET"])
def findLocationsOfHotel_Engine(ndid):
    try:
        status,details= multilocation_usecase.find_locations_of_hotel(ndid)
        return jsonify({"Status":status,"Locations":json.loads(json_util.dumps(details))})
    except Exception as ex:
        return ({"Status":False,"Message": "{}".format(ex)}), 500
    

@multilocation_controller.route("/addlocations/dashboard",methods=["POST"])
def AddLocationsOfHotel_Dashboard():
    try:
        Location_details = request.get_json(force=True)
        status= multilocation_usecase.add_locations_of_hotel(Location_details)
        return jsonify({"Status":status,"Message":"Location Added Successfully !!"})
    except Exception as ex:
        return ({"Status":False,"Message": "{}".format(ex)}), 500
    

@multilocation_controller.route("/editlocations/dashboard",methods=["POST"])
def EditLocationsOfHotel_Dashboard():
    try:
        Location_details = request.get_json(force=True)
        status,message= multilocation_usecase.edit_locations_of_hotel(Location_details)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return ({"Status":False,"Message": "{}".format(ex)}), 500


@multilocation_controller.route("/deletelocations/dashboard",methods=["POST"])
def DeleteLocationsOfHotel_Dashboard():
    try:
        Location_details = request.get_json(force=True)
        status,message= multilocation_usecase.delete_locations_of_hotel(Location_details)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return ({"Status":False,"Message": "{}".format(ex)}), 500