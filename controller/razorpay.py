import logging
import settings
import utils
import json

from usecases import razorpay_usecase
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from bson import json_util


razorpay_controller = Blueprint("razorpay", __name__)


@razorpay_controller.route("/hi",methods=["GET"])
def hello():
    return jsonify({"Message":"Hi"})


@razorpay_controller.route("/edit/gateway",methods=["POST"])
def EditGateway():
    try:
        room_details = request.get_json(force=True)
        status,message = razorpay_usecase.edit_Gateway_dashboard(room_details)
        return jsonify({"status": status, "Message": message})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": False, "message": "Some Problem Occured"}), 500
    

@razorpay_controller.route("/deactivate/razorpay",methods=["POST"])
def deactivateGateway():
    try:
        room_details = request.get_json(force=True)
        room_details["API_KEY"]=""
        room_details["SECRET_KEY"]=""
        room_details["Type"]=""
        status,message = razorpay_usecase.edit_Gateway_dashboard(room_details)
        return jsonify({"status": status, "Message": message})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": False, "message": "Some Problem Occured"}), 500
    



@razorpay_controller.route("/v1/payments", methods=["POST"])
def AllPayments_Razorpay():
    try:
        room_details = request.get_json(force=True)
        status,details = razorpay_usecase.allPayment(room_details)
        return jsonify({"status": status, "Details": details})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": False, "message": "Some Problem Occured"}), 500
    


@razorpay_controller.route("/v1/filtered/orders", methods=["POST"])
def FilteredOrder_Razorpay():
    try:
        room_details = request.get_json(force=True)
        status,details = razorpay_usecase.filterOrders(room_details)
        return jsonify({"status": status, "Details": details})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": False, "message": "Some Problem Occured"}), 500
    


@razorpay_controller.route("/v1/filtered/payments", methods=["POST"])
def FilteredPayments_Razorpay():
    try:
        room_details = request.get_json(force=True)
        status,details = razorpay_usecase.filterPayments(room_details)
        return jsonify({"status": status, "Details": details})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": False, "message": "Some Problem Occured"}), 500


