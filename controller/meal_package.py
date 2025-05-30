import logging
import settings
import utils
import json

from flask import Blueprint,request,jsonify
from usecases import meal_package_usecase
from bson import json_util
meal_package_controller = Blueprint('meal_package', __name__)


@meal_package_controller.route("/hi",methods=["GET"])
def hello():
    return json.dumps({"message": "hi"})



#?done
@meal_package_controller.route("/packages/<token>/<hId>",methods=["GET"])
def get_package_for_hotel(token,hId):
    try:
        ndid = utils.get_ndid(token)
        packages = meal_package_usecase.get_packages_hotel(ndid,hId)
        return jsonify({"Status":True,"Packages":json.loads(json_util.dumps(packages))})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?done
@meal_package_controller.route("/packages/engine/<ndid>/<hId>",methods=["GET"])
def get_package_for_hotel_engine(ndid,hId):
    try:
        packages = meal_package_usecase.get_packages_hotel(ndid,hId)
        return jsonify({"Status":True,"Packages":json.loads(json_util.dumps(packages))})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?done
@meal_package_controller.route("/packages/create",methods=["POST"])
def create_package_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        status = meal_package_usecase.create_package(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    
#?done
@meal_package_controller.route("/packages/edit",methods=["POST"])
def edit_package_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        status = meal_package_usecase.edit_package(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    
#?done
@meal_package_controller.route("/packages/delete",methods=["POST"])
def delete_package_for_hotel():
    try:
        booking_details = request.get_json(force=True)
        status = meal_package_usecase.delete_package(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    
