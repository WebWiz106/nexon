import logging
import settings
import utils
import json

from flask import Blueprint,request,jsonify
from usecases import promos_usecase
from usecases.booking_usecase import check_no_rooms
from datetime import datetime,timedelta
from bson import json_util


promos_controller = Blueprint("promos", __name__)

@promos_controller.route("/hi",methods=["GET"])
def hello():
    return jsonify({"Message":"Hi"})

@promos_controller.route("/promos/<token>/<hId>",methods=["GET"])
def get_promos_for_hotels(token,hId):
    try:
        ndid = utils.get_ndid(token)
        packages = promos_usecase.get_promos_for_hotel(ndid,hId)
        return jsonify({"Status":True,"Promos":json.loads(json_util.dumps(packages))})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@promos_controller.route("/promos/engine/<ndid>/<hId>",methods=["GET"])
def get_promos_for_hotel_engine(ndid,hId):
    try:
        packages = promos_usecase.get_promos_for_hotel(ndid,hId)
        return jsonify({"Status":True,"Promos":json.loads(json_util.dumps(packages))})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@promos_controller.route("/promos/create",methods=["POST"])
def create_promos_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        status = promos_usecase.create_promo_for_hotel(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    

@promos_controller.route("/promos/edit",methods=["POST"])
def edit_promos_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        status = promos_usecase.edit_promo_for_hotel(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    

@promos_controller.route("/promos/delete",methods=["POST"])
def delete_promos_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        status = promos_usecase.delete_promo_for_hotels(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    

@promos_controller.route("/promos/apply",methods=["POST"])
def apply_promo_to_price():
    try:
        booking_details = request.get_json(force=True)
        status = promos_usecase.delete_promo_for_hotels(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    
