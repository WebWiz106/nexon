import utils
import json

from flask import Blueprint,request,jsonify
from flask_cors import CORS,cross_origin
from usecases import ad_package_usecase
from usecases.booking_usecase import check_no_rooms
from datetime import datetime,timedelta
from bson import json_util
import logging

ad_package_controller = Blueprint("ad_package", __name__)

@ad_package_controller.route("/hi")
def hi():
    return json.dumps({"mesage": "Ad-Packages working"})

#?done
@ad_package_controller.route("/ad/packages/<token>/<hId>",methods=["GET"])
def get_ad_package_for_hotel(token,hId):
    try:
        ndid = utils.get_ndid(token)
        packages = ad_package_usecase.get_ad_packages_hotel(ndid,hId)
        logging.info(f"{packages}")
        return jsonify({"Status":True,"Packages":json.loads(json_util.dumps(packages))})
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

#?done
@ad_package_controller.route("/ad/packages/engine/<ndid>",methods=["POST"])
def get_ad_package_for_hotel_engine(ndid):
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        packages = ad_package_usecase.get_ad_packages_for_specific_dates(ndid,booking_details)
        logging.info(f"{packages}")
        return jsonify({"Status":True,"Packages":json.loads(json_util.dumps(packages))})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

#?done
@ad_package_controller.route("/ad/packages/create",methods=["POST"])
def create_ad_package_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        # print(booking_details)
        status = ad_package_usecase.create_ad_package(booking_details)
        
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    
#?done
@ad_package_controller.route("/ad/packages/edit",methods=["POST"])
def edit_ad_package_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        status = ad_package_usecase.edit_ad_package(booking_details)
        logging.info(f"{status}")
        return jsonify({"Status":status})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500
    
#?done
@ad_package_controller.route("/ad/packages/delete",methods=["POST"])
def delete_ad_package_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        status = ad_package_usecase.delete_ad_package(booking_details)
        logging.info(f"{status}")
        return jsonify({"Status":status})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500
    