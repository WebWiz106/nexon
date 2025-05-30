import json
import settings
import razorpay
import utils
from bson import json_util
from usecases import room_usecase ,roominventory_usecase,price_usecase
from flask import Blueprint,jsonify, request
from datetime import datetime,date,timedelta

roominventory = Blueprint('roominventory', __name__)

@roominventory.route("/hi")
def hi():
    return json.dumps({"mesage":"hi"})

@roominventory.route("/getinventory/all/<token>/<hId>",methods=["GET"])
def get_all_room_inventory(token,hId):
    try:
        inventory={}
        rooms = room_usecase.get_all_rooms(token,hId)
        next40dates=price_usecase.get_next_dates_from_today(8)
        for i in rooms:
            room_inventory={}
            for date in next40dates:
                inventoryStatus = i.get("inventoryStatus",{})
                if(str(date) in inventoryStatus):
                    room_inventory[str(date)]=int(inventoryStatus[str(date)])
                else:
                    room_inventory[str(date)]=int(i["noOfRooms"])

            inventory[i["roomType"]]=room_inventory
        return jsonify({"Status":True,"Inventory":inventory,"prev":str(next40dates[0]),"next":str(next40dates[7])})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

@roominventory.route("/getinventory/all/nextprev/<token>/<hid>",methods=["POST"])
def get_all_inventory_room_fordate(token,hid):
    try:
        booking_details = request.get_json(force=True)
        date = booking_details.get("date")
        operation = booking_details.get("operation")
        if operation=="prev":
            next40dates=room_usecase.get_prev_dates_from_date(date,8)
        else:
            next40dates=room_usecase.get_next_dates_from_date(date,8)
        inventory={}
        rooms = room_usecase.get_all_rooms(token,hid)
        for i in rooms:
            room_inventory={}
            roominv = i.get('inventoryStatus',{})
            for date in next40dates:
                if(str(date) in roominv):
                    room_inventory[str(date)]=int(roominv[str(date)])
                else:
                    room_inventory[str(date)]=int(i["noOfRooms"])
            inventory[i["roomType"]]=room_inventory
        return jsonify({"Status":True,"Inventory":inventory,"prev":str(next40dates[0]),"next":str(next40dates[7])})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

@roominventory.route("/update/daterange/inventory",methods=["POST"])
def update_inventory_room_fordate():
    try:
        booking_details = request.get_json(force=True)
        status = roominventory_usecase.update_inventory_of_rooms(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500

@roominventory.route("/update/bulk/inventory",methods=["POST"])
def update_inventory_room_forbulk():
    try:
        booking_details = request.get_json(force=True)
        status = roominventory_usecase.update_bulk_inventory_of_rooms(booking_details)
        return jsonify({"Status":status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500