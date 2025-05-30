import utils
import constants
import pymongo
import json
import settings
import logging
from model.room import Room
from bson import json_util
from usecases import booking_usecase
from datetime import datetime, date, timedelta
from model.roomFacilities import RoomFacility
from utils import db
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


def add_roomnumber_in_createprocess(n,start):
    number_list = [str(int(start) + i) for i in range(n)]
    return number_list

#?DONE
def add_room(room_details, token):
    try:
        logging.info(f"{room_details},{token}")
        room=Room.from_dict(room_details)
        ndid = utils.get_ndid(token)
        room_type = room.roomType
        hId = room_details.get("hId", "")
        room.ndid=ndid
        number = room_type+"01"
        room.roomNumbers = add_roomnumber_in_createprocess(int(room.noOfRooms),int(number))
        room_type_name = constants.room_type_name.get(room_type)
        available_room = get_room(ndid, hId, room_type_name)
        if available_room:
            logging.info(f"False")
            return False, "Room already exist with the provided Room Type"
        room.roomTypeName=room_type_name
        db.Rooms.insert_one(Room.to_dict(room))
        
        logging.info(f"True")
        return True, "Success"
    except Exception as ex:
        logging.error(f"{ex}")
        LOGGER.error("Unabel to create room error:{}".format(ex))
        return False, "Error Occured"

#?NOT REQUIRED
def delete_room_db(ndid, hId, room_type_name):
    try:
        return db.Rooms.delete_one({"ndid": ndid, "hId": hId, "roomTypeName": room_type_name})
    except Exception as e:
        logging.error(f"Error in deleting room from db {e}")

#?NOT REQUIRED
def delete_room(roomtype, token, hId):
    try:
        logging.info(f"{roomtype},{token}")
        ndid = utils.get_ndid(token)
        room_type_name = constants.room_type_name.get(roomtype)
        available_room = delete_room_db(ndid, hId, room_type_name)
        if available_room.deleted_count == 1:
            logging.info(f"Room Deleted")
            return True, "Room Deleted"
        else:
            logging.info(f"Room Not exists")
            return False, "Room Not exists"
    except Exception as ex:
        logging.error(f"{ex}")
        LOGGER.error("Unable to delete room error:{}".format(ex))
        return False, "Error Occured"

#?DONE
def edit_room_db(room_details, token):
    try:
        logging.info(f"{room_details},{token}")
        
        ndid = utils.get_ndid(token)
        room_type = room_details.get("roomType", "1")
        room_type_name = constants.room_type_name.get(room_type)
        hId = room_details.get("hId")
        room_exist=get_room(ndid,hId,room_type_name)
        number = room_type+"01"
        if room_exist:
            room=Room.from_dict(room_exist)
            room.roomName=room_details.get("roomName", "")
            room.roomDescription= room_details.get("roomDescription", "")
            room.child = room_details.get("child", -1)
            room.adult = room_details.get("adult", -1)
            room.noOfRooms = room_details.get("noOfRooms", 1)
            room.price= room_details.get("price", 0)
            room.roomImage= room_details.get("roomImage", [])
            facilities = room_details.get("roomFacilities", {})
            room.roomSubheading = room_details.get("roomSubheading", "enjoy")
            filter_criteria = {
                "ndid": ndid,
                "hId": hId,
                "roomTypeName": room_type_name
            }
            room.roomFacilities=RoomFacility.from_dict(facilities)
            room_updated=room.to_dict()
            result = db.Rooms.update_one(filter_criteria, {"$set": room_updated})
            if result.modified_count > 0:
                logging.info(f"Room Updated")
                return True, "Room Updated"
            else:
                logging.info(f"No Matching")
                return False, "No matching room found for update"
        else:
            return False, "Room not found or not updated"
    except Exception as ex:
        logging.info(f"{ex}")
        LOGGER.error("Unablr to edit room error:{}".format(ex))
        return False, "Error Occured"

#?NOT DONE
def get_room(ndid, hId, room_type_name):
    try:
        return db.Rooms.find_one({"ndid": ndid, "hId": hId, "roomTypeName": room_type_name})
    except Exception as ex:
        logging.error(ex)
        return None

def get_each_rooms(token):
    try:
        counter+=1  
        print(counter)
        ndid = utils.get_ndid(token)
        rooms = db.Rooms.find({"ndid": ndid})
        return json.loads(json_util.dumps(rooms))
    except Exception as ex:
        logging.error(ex)
        return None
    
def get_domain_based_rooms(domain):
    try:
        profile = db.Zucks_profile.find_one({"domain":domain})
        rooms = db.Rooms.find({"ndid": profile.get("uId")})
        return json.loads(json_util.dumps(rooms))
    except Exception as ex:
        logging.error(ex)
        return None



#?NOT DONE
def get_all_rooms(token, hId):
    try:
        ndid = utils.get_ndid(token)
        rooms = db.Rooms.find({"ndid": ndid, "hId": hId})
        return json.loads(json_util.dumps(rooms))
    except Exception as ex:
        logging.error(ex)
        return None

#?NOT DONE
def get_all_rooms_engine(ndid, hId):
    try:
        logging.info(f"{ndid}")
        rooms = db.Rooms.find({"ndid": ndid, "hId": hId})
        logging.info(f"{rooms}")
        return json.loads(json_util.dumps(rooms))
    except Exception as ex:
        logging.error(ex)
        return None

#?NOT DONE
def room_getBookingCount_on_date(token, hId, checkin):
    try:
        logging.info(f"{token},{checkin}")
        Delux = SuperDelux = Suite = Premium = 0

        ndid = utils.get_ndid(token)
        query = {
            "hId": hId,
            "ndid": ndid,
            "checkIn": {
                "$lte": checkin
            },
            "checkOut": {
                "$gt": checkin
            }
        }
        bookings = db.Bookings.find(query)

        for booking in bookings:
            for bookingdata in booking.get("Bookings"):
                if bookingdata.get("Qty") > 0:
                    if bookingdata.get('RoomType') == "1":
                        Delux += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "2":
                        SuperDelux += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "3":
                        Suite += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "4":
                        Premium += bookingdata.get("Qty")
        logging.info(f"{Delux},{SuperDelux},{Suite},{Premium}")
        return Delux, SuperDelux, Suite, Premium
    except Exception as ex:
        logging.error(ex)
        return None



#?NOT DONE
def get_all_rooms_prices(room_details, ndid, hId):
    try:
        logging.info(f"{room_details},{ndid}")
        price = {}
        rooms = db.Rooms.find({"ndid": ndid, "hId": hId})
        for room in rooms:
            booking_details = {
                "checkIn": room_details.get('checkIn'),
                "checkOut": room_details.get('checkOut'),
                "roomType": room.get('roomType')
            }
            amount = booking_usecase.calculate_booking_total(
                booking_details, ndid, hId)
            price[room.get('roomType')] = amount
        logging.info(f"{price}")
        return price
    except Exception as ex:
        logging.error(ex)
        return None

#?NOT DONE
def get_all_rooms_engine_with_price(room_details, ndid):
    try:
        logging.info(f"{room_details},{ndid}")
        hId = room_details.get("hId")
        rooms = db.Rooms.find({"ndid": ndid, "hId": hId})
        prices = get_all_rooms_prices(room_details, ndid, hId)
        logging.info(f"{rooms},{prices}")
        return json.loads(json_util.dumps(rooms)), prices
    except Exception as ex:
        logging.error(ex)
        return None
# =========================================PRICES===================================================

#?NOT REQUIRED
def get_id(booking_count):
    try:
        logging.info(f"{booking_count}")
        for i in range(5 - len(booking_count)):
            booking_count = "0" + booking_count
        logging.info(f"{booking_count}")
        return booking_count
    except Exception as ex:
        logging.error(ex)
        return None

#?NOT REQUIRED
def get_next_dates_from_date(date, number):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d").date()
        dates = []
        for i in range(0, number):
            next_n_days = current_date + timedelta(days=i)
            dates.append(next_n_days)

        return dates
    except Exception as ex:
        logging.error(f"{ex}")
        return None
# 6

#?NOT REQUIRED
def get_prev_dates_from_date(date, number):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d").date()
        dates = []
        for i in range(number, 0, -1):
            next_n_days = current_date - timedelta(days=i)
            dates.append(next_n_days)

        return dates
    except Exception as ex:
        logging.error(f"{ex}")
        return None
    
#?NOT REQUIRED
def return_weakday(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Get the day name using the day_of_week as an index
        day_name = day_names[date.weekday()]
        return day_name
    except Exception as ex:
        logging.error(ex)
        return None
