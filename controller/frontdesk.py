from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin

from usecases import frontdesk_usecase
# cms_controller = Blueprint('cms', __name__)
frontdesk_controller = Blueprint('frontdesk', __name__)




@frontdesk_controller.route("/hi")
def hello1():
    return {"Message":"Hi"}

@frontdesk_controller.route("/add-maintenance",methods=["POST"])
def add_maintenance():
    maintenance_details = request.get_json(force=True)
    status,message=frontdesk_usecase.add_maintenance_usecase(maintenance_details)
    return jsonify({"status":status,"message":message})

@frontdesk_controller.route("/update-maintenance",methods=["POST"])
def update_maintenance():
    maintenance_details = request.get_json(force=True)
    status,message=frontdesk_usecase.update_maintenance_usecase(maintenance_details)
    return jsonify({"status":status,"message":message})


@frontdesk_controller.route("/delete-maintenance",methods=["POST"])
def delete_maintenance():
    maintenance_details = request.get_json(force=True)
    status,message=frontdesk_usecase.delete_maintenance_usecase(maintenance_details)
    return jsonify({"status":status,"message":message}) 


@frontdesk_controller.route("/update-booking",methods=["POST"])
def update_booking_roomnumber_checkin_checkout():
    maintenance_details = request.get_json(force=True)
    status,message=frontdesk_usecase.update_booking_checkin_checkout_usecase(maintenance_details)
    return jsonify({"status":status,"message":message}) 

