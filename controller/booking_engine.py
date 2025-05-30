import json
import settings
import razorpay
import utils
from bson import json_util

from usecases import booking_usecase, booking_engine_usecase,mail_usecase
from flask import Blueprint, jsonify, request
from datetime import datetime, date, timedelta
import logging
booking_controller = Blueprint('booking_engine', __name__)


@booking_controller.route("/hi")
def hi():
    return json.dumps({"mesage": "hi"})


# ?:- DONE
@booking_controller.route("/getengine/<token>/<hId>", methods=["GET"])
def get_engine_details(token, hId):
    try:
        logging.info(f"{token}")
        status, message = booking_engine_usecase.get_engine(token, hId)
        logging.info(f"{status} and {message}")
        return jsonify({"Status": status, "Details": message})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500


# ?:- DONE
@booking_controller.route("/getenginedetails/<id>/<hId>", methods=["GET"])
def get_engine_details_for_engine(id, hId):
    try:
        logging.info(f"{id}")
        print(hId)
        message = booking_engine_usecase.get_engine_details(id, hId)
        # print(message)
        website = booking_engine_usecase.get_engine_webiste(id)
        profile = booking_engine_usecase.get_profile(id)
        logging.info(f"{message} , {website}, {profile}")
        if message and website and profile:
            return jsonify({"Status": True, "Details": message, "website": website, "Profile": json.loads(json_util.dumps(profile))})
        else:
            return jsonify({"Status": False})
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Status": False, "Message": "{}".format(ex)}), 500

# ?done


@booking_controller.route("/create", methods=["POST"])
def create_booking():
    try:
        booking_data = request.get_json(force=True)
        logging.info(f"{booking_data}")
        status, message = booking_usecase.create_booking(booking_data)
        logging.info(f"{status} , {message}")
        return jsonify({"status": status, "message": message})
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Status": False, "Message": "{}".format(ex)}), 500


@booking_controller.route("/update", methods=["POST"])
def update_booking():
    try:
        booking_data = request.get_json(force=True)
        logging.info(f"{booking_data}")
        status, message = booking_usecase.update_booking(booking_data)
        logging.info(f"{status} , {message}")
        return jsonify({"status": status, "message": message})
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Status": False, "Message": "{}".format(ex)}), 500


@booking_controller.route("/update/guest", methods=["POST"])
def update_booking_guest_info():
    try:
        booking_data = request.get_json(force=True)
        logging.info(f"{booking_data}")
        status = booking_usecase.editBookingGuestInfo(booking_data)
        logging.info(f"{status}")
        return jsonify({"status": status})
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Status": False, "Message": "{}".format(ex)}), 500


@booking_controller.route("/availablity/today/<token>/<hId>", methods=["GET"])
def get_availablity_of_today(token, hId):
    try:
        logging.info(f"{token}")
        ndid = utils.get_ndid(token)
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        booking_data = {
            "hId": hId,
            "ndid": ndid,
            "checkin": today.strftime('%Y-%m-%d'),
            "checkout": tomorrow.strftime('%Y-%m-%d')
        }
        status, message = booking_usecase.avaiblity_of_rooms(booking_data)
        logging.info(f"{status},{message}")
        return jsonify({"status": status, "Avaiblity": message})
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Status": False, "Message": "{}".format(ex)}), 500


@booking_controller.route("/availablity", methods=["POST"])
def get_availablity_booking():
    try:
        booking_data = request.get_json(force=True)
        logging.info(f"{booking_data}")
        status, message = booking_usecase.check_list_of_rooms_available_daterange(booking_data)
        logging.info(f"{status},{message}")
        return jsonify({"status": status, "Avaiblity": message})
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Status": False, "Message": "{}".format(ex)}), 500

# ?done


@booking_controller.route("/total/<ndid>", methods=["POST"])
def calculate_booking_total(ndid):
    try:
        logging.info(f"{ndid}")
        booking_details = request.get_json(force=True)
        amount = booking_usecase.calculate_booking_total(booking_details, ndid)
        logging.info(f"{amount}")
        return amount
    except Exception as ex:
        logging.info(f"{ex}")
        return ({"Status": False, "Message": "{}".format(ex)}), 500
# All Bookings

# ?:- DONE


@booking_controller.route("/bookings/<token>/<hId>", methods=["GET"])
def get_all_bookings_of_engine(token, hId):
    try:
        logging.info(f"{token}")
        status, message = booking_usecase.get_all_bookings(token, hId, "0")
        logging.info(f"{status},{message}")
        return jsonify({"Status": status, "Details": json.loads(json_util.dumps(message))})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

# ?:- DONE


@booking_controller.route("/checkintoday/<token>/<hId>", methods=["GET"])
def get_todays_checkin_and_list(token, hId):
    try:
        logging.info(f"{token}")
        status, count, message = booking_usecase.todays_checkin(
            token, hId, datetime.today().strftime('%Y-%m-%d'))
        logging.info(f"{status},{count},{message}")
        return jsonify({"Status": status, "Checkin": count, "Details": json.loads(json_util.dumps(message))})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

# ?:- DONE


@booking_controller.route("/checkouttoday/<token>/<hId>", methods=["GET"])
def get_todays_checkout_and_list(token, hId):
    try:
        logging.info(f"{token}")
        status, count, message = booking_usecase.todays_checkout(
            token, hId, datetime.today().strftime('%Y-%m-%d'))
        logging.info(f"{status},{count},{message}")
        return jsonify({"Status": status, "Checkout": count, "Details": json.loads(json_util.dumps(message))})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500


# ?:- DONE
@booking_controller.route("/filter/<Type>", methods=["POST"])
def get_filtered_bookings_of_engine(Type):
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        token = booking_details.get("token")
        hId = booking_details.get("hId")
        status, message = booking_usecase.get_all_bookings(token, hId, Type)
        logging.info(f"{status} , {message}")
        return jsonify({"Status": status, "Details": json.loads(json_util.dumps(message))})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

# ?:- DONE


@booking_controller.route("/filter/dates", methods=["POST"])
def get_bookings_from_dates():
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        status, message = booking_usecase.get_dates_range_booking(
            booking_details)
        logging.info(f"{status},{message}")
        return jsonify({"Status": status, "Details": json.loads(json_util.dumps(message))})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

# ?:- DONE


@booking_controller.route("/filter/bookingid", methods=["POST"])
def get_bookings_from_bookingid():
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        status, message = booking_usecase.get_bookingid_range_booking(
            booking_details)
        logging.info(f"{status} ,  {message}")
        return jsonify({"Status": status, "Details": json.loads(json_util.dumps(message))})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

# ?:- DONE


@booking_controller.route("/filter/payment/<status>", methods=["POST"])
def bookings_for_payment_status(status):
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        token = booking_details.get("token")
        hId = booking_details.get("hId")
        message, bookings = booking_usecase.booking_on_filter_peyment_status(
            status, token, hId)
        logging.info(f"{message}, {bookings}")
        return jsonify({"Status": message, "Bookings": json.loads(json_util.dumps(bookings))})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

# ?:- DONE


@booking_controller.route("/payment/status/<status>", methods=["POST"])
def change_booking_status(status):
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        print(booking_details)
        token = booking_details.get("token")
        booking_id = booking_details.get("bookingId")
        hId = booking_details.get("hId")
        message = booking_usecase.cancel_booking_payment_status(
            token, booking_id, status, hId)
        logging.info(f"{message}")
        return jsonify({"Status": message})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500
    


@booking_controller.route("/payment/checkinout", methods=["POST"])
def change_booking_checkin_out_status():
    try:
        booking_details = request.get_json(force=True)
        token = booking_details.get("token")
        booking_id = booking_details.get("bookingId")
        isCheckedin = booking_details.get("isCheckedin")
        isCheckout = booking_details.get("isCheckout")
        hId = booking_details.get("hId")
        logging.info(f"{booking_details}")
        message = booking_usecase.change_booking_checked_in_out_status(token, booking_id, isCheckedin, isCheckout, hId)
        logging.info(f"{message}")
        return jsonify({"Status": message})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500

# ?:- DONE


@booking_controller.route("/cancel/<token>", methods=["POST"])
def cancel_booking(token):
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        booking_id = booking_details.get('bookingId')
        hId = booking_details.get('hId')
        status = booking_usecase.cancel_booking_usecase(token, booking_id, hId)
        logging.info(f"{status}")
        return jsonify({"Status": status})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500


@booking_controller.route("/engine/queryrates/<id>", methods=["POST"])
def Query_rates(id):
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        message = booking_engine_usecase.create_query_rates(
            booking_details, id)
        logging.info(f"{message}")
        return jsonify({"Status": True, "Messsage": "Query sended to "+message})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500


@booking_controller.route('/profile/currency/edit/<token>', methods=["POST"])
def Update_Currency_paymentstatus(token):
    try:
        booking_details = request.get_json(force=True)
        ndid = utils.get_ndid(token)
        logging.info(f"{booking_details}")
        message = booking_engine_usecase.change_currency_profile_online_payment_status(
            booking_details, ndid)
        logging.info(f"{message}")
        return jsonify({"Status": True})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500


@booking_controller.route("/create/digital/checkin", methods=["POST"])
def create_Digital_checkin_hotel():
    try:
        booking_details = request.get_json(force=True)
        logging.info(f"{booking_details}")
        status = booking_engine_usecase.uploadDigitalCheckinData(
            booking_details)
        logging.info(f"{status}")
        return jsonify({"Status": status})
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500
    

@booking_controller.route("/generateotp", methods=["POST"])
def generateOtp():
    try:
        booking_details = request.get_json(force=True)
        ndid=booking_details.get("ndid")
        hId=booking_details.get("hId")
        bookingId=booking_details.get("bookingId")
        status,message=booking_engine_usecase.sendOtp(bookingId,ndid,hId)
        return jsonify({"Status":status,"Message":message}) 
    except Exception as ex:
        logging.error(f"{ex}") 
        return jsonify({"Status":False,"Message": "{}".format(ex)})
    

@booking_controller.route("/cancelOtp", methods=["POST"])
def cancelBookingookingEngine():
    try:
        booking_details = request.get_json(force=True)
        ndid=booking_details.get("ndid")
        hId=booking_details.get("hId")
        bookingId=booking_details.get("bookingId")
        otp=booking_details.get("otp")
        status,message=booking_engine_usecase.cancelBookingFromBookingEngine(bookingId,ndid,hId,otp)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        logging.error(f"{ex}")
        return jsonify({"Status":False,"Message": "{}".format(ex)})
    
@booking_controller.route("/cancelwithoutOtp", methods=["POST"])
def cancelBookingookingEngineWihoutOtp():
    try:
        booking_details = request.get_json(force=True)
        ndid=booking_details.get("ndid")
        hId=booking_details.get("hId")
        bookingId=booking_details.get("bookingId")
        status,message=booking_engine_usecase.cancelBookingFromBookingEnginewithoutOtp(bookingId,ndid,hId)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        logging.error(f"{ex}")
        return jsonify({"Status":False,"Message": "{}".format(ex)})