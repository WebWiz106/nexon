import logging
import settings
import utils
import json

from flask import Blueprint,request,jsonify,redirect,abort,render_template
from flask_cors import CORS,cross_origin
from usecases import phonepe_usecase
from usecases.booking_usecase import check_no_rooms
from datetime import datetime,timedelta
from bson import json_util
import base64
import hashlib





phonepe_controller = Blueprint("phonepe", __name__)

merchant_id = "YOUR_MERCHANT_ID"  
salt_key = "YOUR_SALT_KEY"  
salt_index = 1 


@phonepe_controller.route("/hi")
def hello():
    return "hi!!"

@phonepe_controller.route("/pay",methods=["POST"])
def DataforPay():
    booking_details = request.get_json(force=True)
    transitionid = phonepe_usecase.pay(booking_details)
    return transitionid


@phonepe_controller.route("/fetchpayment",methods=["POST"])
def DataforPaymentfetch():
    booking_details = request.get_json(force=True)
    transitionid = phonepe_usecase.payment_return(booking_details)
    return transitionid


@phonepe_controller.route("/postpaymentredirect",methods=["POST"])
def postpaymentredirect():
    try:
        data = request.form 
        if data.get("code")=="PAYMENT_SUCCESS" and data.get("merchantId") and data.get("transactionId") and data.get("providerReferenceId"):
            status,data,logo,hotelname=phonepe_usecase.payment_post_return(data)
            if status:
                return render_template("success.html",data=data,logo=logo,hotelname=hotelname)
            else:
                return render_template("failure.html")
        else:
            return render_template("failure.html")
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@phonepe_controller.route("/test",methods=["GET"])
def posttesttesttesttest():
    return render_template("check.html")





