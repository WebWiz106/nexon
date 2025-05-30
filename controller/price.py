import logging
import settings
import utils
import json

from flask import Blueprint,request,jsonify
from flask_cors import CORS,cross_origin
from usecases import price_usecase
from usecases.booking_usecase import check_no_rooms
from datetime import datetime,timedelta
from bson import json_util


price_controller = Blueprint("price", __name__)


@price_controller.route("/hi")
def hello():
    return "hi!!"

#?:- DONE
@price_controller.route("/getprice",methods=["POST"])
def get_room_prices():
    try:
        booking_details = request.get_json(force=True)
        status,prices = price_usecase.get_price_of_rooms(booking_details)
        return jsonify({"Status":status,"Prices":prices})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?:- DONE
@price_controller.route("/getprice/all/<token>/<hId>",methods=["GET"])
def get_all_room_prices(token,hId):
    try:
        prices={}
        rooms = price_usecase.get_all_rooms(token,hId)
        next40dates=price_usecase.get_next_dates_from_today(8)
        for i in rooms:
            price={}
            for date in next40dates:
                if i["isWeekendFormat"]:

                    if(price_usecase.is_weekend(str(date))):
                        price[str(date)]=i["changedPrice"]["weekend"]
                    else:
                        price[str(date)]=i["changedPrice"]["weekday"]
                else:
                    if(str(date) in i["changedPrice"]):
                        price[str(date)]=i["changedPrice"][str(date)]
                    else:
                        price[str(date)]=i["price"]

            prices[i["roomType"]]=price
        return jsonify({"Status":True,"Prices":prices,"prev":str(next40dates[0]),"next":str(next40dates[7])})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?:- DONE
@price_controller.route("/update/price",methods=["POST"])
def update_room_prices():
    try:
        booking_details = request.get_json(force=True)
        status = price_usecase.update_price_of_rooms(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?:- DONE
@price_controller.route("/update/weekendprice",methods=["POST"])
def update_weakendPrice():
    try:
        booking_details = request.get_json(force=True)
        status = price_usecase.update_weekend_weakday_price(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?:- DONE
@price_controller.route("/update/weekendprice/range",methods=["POST"])
def update_weakend_weakday_Price_engine():
    try:
        booking_details = request.get_json(force=True)
        status = price_usecase.update_price_of_rooms_on_rangeBooking(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?:- DONE
@price_controller.route("/update/bulkprice",methods=["POST"])
def bulk_Update_prices():
    try:
        booking_details = request.get_json(force=True)
        status = price_usecase.update_bulk_price_of_rooms(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?:- DONE
@price_controller.route("/getprice/all/nextprev/<token>",methods=["POST"])
def get_all_room_prices_fordate(token):
    try:
        booking_details = request.get_json(force=True)

        date = booking_details.get("date")
        hId=booking_details.get("hId")
        operation = booking_details.get("operation")
        if operation=="prev":
            next40dates=price_usecase.get_prev_dates_from_date(date,8)
        else:
            next40dates=price_usecase.get_next_dates_from_date(date,8)

        prices={}
        rooms = price_usecase.get_all_rooms(token,hId)
        for i in rooms:
            price={}
            for date in next40dates:
                if i["isWeekendFormat"]:

                    if(price_usecase.is_weekend(str(date))):
                        price[str(date)]=i["changedPrice"]["weekend"]
                    else:
                        price[str(date)]=i["changedPrice"]["weekday"]

                else:

                    if(str(date) in i["changedPrice"]):
                        price[str(date)]=i["changedPrice"][str(date)]
                    else:
                        price[str(date)]=i["price"]

            prices[i["roomType"]]=price
        return jsonify({"Status":True,"Prices":prices,"prev":str(next40dates[0]),"next":str(next40dates[7])})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

#?:- DONE
@price_controller.route("/update/weakendformat",methods=["POST"])
def update_room_weakend_format_status():
    try:
        booking_details = request.get_json(force=True)
        status = price_usecase.update_weekend_format(booking_details)
        logging.info(f"Weekend format status updated. Status: {status}")
        return jsonify({"Status":status})
    except Exception as ex:
        logging.error(f"Error updating weekend format status. Error: {str(ex)}")
        return ({"Message": "{}".format(ex)}), 500
    
#?:- DONE
@price_controller.route("/update/bulkprice/dayswise",methods=["POST"])
def bulk_Update_prices_with_range_weakdays():
    try:
        booking_details = request.get_json(force=True)
        status = price_usecase.update_price_days_wise(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
    
#?:- DONE
@price_controller.route("/update/bulkprice/percentage",methods=["POST"])
def bulk_Update_prices_with_range_percentage():
    try:
        booking_details = request.get_json(force=True)
        status = price_usecase.update_price_percent_wise(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500
