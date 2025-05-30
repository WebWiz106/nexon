import utils
import constants
import pymongo
import json
import settings
import logging
from bson import json_util
from usecases import booking_usecase
from datetime import datetime,date,timedelta
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)
from utils import db

def update_inventory_of_rooms(room_details):
    try:
        token = room_details.get("token")
        roomType = room_details.get("roomType")
        date1 = room_details.get("date1")
        date2 = room_details.get("date2")
        room = room_details.get("room")
        hId = room_details.get("hId")

        ndid = utils.get_ndid(token)
        date_range = [date1]
        current_date = date1
        while current_date < date2:
            current_date = (datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            # print(current_date)
            date_range.append(current_date)
        # Construct the update query dynamically
        update_query = {"$set":{}}
        for date in date_range:
            update_query["$set"][f"inventoryStatus.{date}"] = int(room)
        # print(update_query)
        db.Rooms.find_one_and_update({"ndid":ndid,"roomType":roomType,"hId":hId},update_query)
        return True
    except:
        return False


def update_bulk_inventory_of_rooms(room_details):
    try:
        hId = room_details.get("hId")
        token = room_details.get("token")
        Data = room_details.get("bulkinventory")                #{"1":{"2023-10-19":"1700","2023-10-27":"2200"},"2":{"2023-10-22":"3300"}}
        ndid = utils.get_ndid(token)
        room = db.Rooms.find({"ndid":ndid,"hId":hId})                         #all rooms
        totalrooms=[]
        for r in room:
            totalrooms.append(r)
        for room in totalrooms:
            roomType = room["roomType"]
            if roomType in Data:
                roomInventory = room.get("inventoryStatus",{})
                data_for_room = Data[roomType]
                for date, roominv in data_for_room.items():
                    roomInventory[date] = int(roominv)
                update_query = {
                    "$set": {
                        "inventoryStatus":roomInventory
                    }
                }
                db.Rooms.find_one_and_update({"ndid":ndid,"roomType":roomType,"hId":hId},update_query)
        return True
    except:
        return False