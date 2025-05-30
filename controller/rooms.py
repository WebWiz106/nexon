import logging
import settings
import utils
import json

from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from usecases import room_usecase
from usecases.booking_usecase import check_no_rooms
from datetime import datetime, timedelta
from bson import json_util


room_controller = Blueprint("rooms", __name__)


@room_controller.route("/hi",methods=["GET"])
def hello():
    return jsonify({"Message":"Hi"})

@room_controller.route("/engine/<id>", methods=["POST"])
def get_all_rooms_engine(id):
    try:
        room_details = request.get_json(force=True)
        rooms, prices = room_usecase.get_all_rooms_engine_with_price(room_details, id)
        # print(rooms)
        logging.info(f"{id}. Details: {rooms}, Prices: {prices}")
        return jsonify({"Status": True, "Details": rooms, "Price": prices})
    except Exception as ex:
        logging.error(f"{ex}")
        return jsonify({"Status": False, "Message": str(ex)}), 500

# ?done


@room_controller.route("/<token>", methods=["GET"])
def get_each_rooms(token):
    try:
        # print(token)
        rooms = room_usecase.get_each_rooms(token)
        logging.info(f"Rooms retrieved successfully for token: {token}")
        return jsonify({"data": rooms,"Status":True})
    except Exception as e:
        # Handle exceptions and log the error
        logging.error(e)
        return jsonify({"error": "Internal server error","Status":False}), 500


@room_controller.route("/get/room/website/<domain>", methods=["GET"])
def get_rooms_domain_based(domain):
    try:
        # print(token)
        rooms = room_usecase.get_domain_based_rooms(domain)
        logging.info(f"Rooms retrieved successfully for token: {domain}")
        return jsonify({"data": rooms,"Status":True})
    except Exception as e:
        # Handle exceptions and log the error
        logging.error(e)
        return jsonify({"error": "Internal server error","Status":False}), 500


@room_controller.route("/<token>/<hId>", methods=["GET"])
def get_all_rooms(token, hId):
    try:
        # print(token)
        rooms = room_usecase.get_all_rooms(token, hId)
        logging.info(f"Rooms retrieved successfully for token: {token}")
        return jsonify({"data": rooms,"Status":True})
    except Exception as e:
        # Handle exceptions and log the error
        logging.error(e)
        return jsonify({"error": "Internal server error","Status":False}), 500

# ?done


@room_controller.route("/create/<token>", methods=["POST"])
def create_room(token):
    try:
        room_details = request.get_json(force=True)
        status, message = room_usecase.add_room(room_details, token)
        logging.info(f"Room created successfully with token: {token}")
        return jsonify({"status": status, "message": message})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": "error", "message": message}), 500

# ?done


@room_controller.route("/delete/<roomtype>", methods=["POST"])
def delete_room(roomtype):
    try:
        room_details = request.get_json(force=True)
        token = room_details.get("token")
        hId = room_details.get("hId")
        status, message = room_usecase.delete_room(roomtype, token, hId)
        logging.info(f" deleted successfully. Status: {status}, Message: {message}")
        return jsonify({"status": status, "message": message})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": "error", "message": message}), 500
# ?done


@room_controller.route("/edit/<token>", methods=["POST"])
def edit_room(token):
    try:
        room_details = request.get_json(force=True)
        status, message = room_usecase.edit_room_db(room_details, token)
        logging.info(f" Status: {status}, Message: {message}")
        return jsonify({"status": status, "message": message})
    except Exception as ex:
        logging.error(ex)
        return jsonify({"status": "error", "error": "Internal server error"}), 500


# ?done
@room_controller.route("/available/next30days/<token>", methods=["POST"])
def available_rooms_for_next_month(token):
    try:
        booking_details = request.get_json(force=True)
        days = int(booking_details.get("days"))
        hId = booking_details.get("hId")
        ndid = utils.get_ndid(token)
        Rooms = []
        deluxrooms = check_no_rooms(ndid,hId, "1")
        superdeluxrooms = check_no_rooms(ndid,hId, "2")
        suiterooms = check_no_rooms(ndid,hId, "3")
        premiumrooms = check_no_rooms(ndid, hId,"4")

        for i in range(0, days):
            current_date = datetime.today().date()
            next_n_days = current_date + timedelta(days=i)
            date = str(next_n_days)
            delux, sd, suite, premium = room_usecase.room_getBookingCount_on_date(
                token, hId, checkin=date)
            Rooms.append({date: {
                "DELUX": deluxrooms-delux if deluxrooms-delux > 0 else 0,
                "SUPERDELUX": superdeluxrooms-sd if superdeluxrooms-sd > 0 else 0,
                "SUITE": suiterooms-suite if suiterooms-suite > 0 else 0,
                "PREMIUM": premiumrooms-premium if premiumrooms-premium > 0 else 0
            }})
        logging.info(f"Available rooms for the next 30 days: {Rooms}")
        return jsonify({"Status": True, "Rooms": Rooms})
    except Exception as ex:
        logging.error(f"Error : {token}, Error: {str(ex)}")
        return ({"Message": "{}".format(ex)}), 500
