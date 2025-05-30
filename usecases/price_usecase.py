import utils
import constants
import pymongo
import json
import settings
import logging

from bson import json_util
from usecases import booking_usecase
from datetime import datetime, date, timedelta

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

from utils import db

def is_weekend(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        return date.weekday() in [5, 6]
    except Exception as ex:
        logging.error(f"{ex}")
        return None


def get_all_rooms(token, hId):
    try:
        logging.info(f"{token}")
        ndid = utils.get_ndid(token)
        rooms = db.Rooms.find({"ndid": ndid, "hId": hId})
        logging.info(f"{rooms}")
        return json.loads(json_util.dumps(rooms))
    except Exception as ex:
        logging.error(f"{ex}")
        return None

# 1


def get_price_of_rooms(room_details):
    try:
        logging.info(f"{room_details}")
        token = room_details.get("token")
        roomType = room_details.get("roomType")
        hId = room_details.get("hId")
        print(room_details)

        ndid = utils.get_ndid(token)

        room = db.Rooms.find_one(
            {"ndid": ndid, "hId": hId, "roomType": roomType})
        logging.info(f"{room}")
        return True, room.get("changedPrice")
    except Exception as ex:
        logging.error(f"{ex}")
        return False
# 2


def update_price_of_rooms(room_details):
    try:
        token = room_details.get("token")
        roomType = room_details.get("roomType")
        date1 = room_details.get("date1")
        date2 = room_details.get("date2")
        price = room_details.get("price")
        hId = room_details.get("hId")
        ndid = utils.get_ndid(token)
        date_range = [date1]
        current_date = date1
        while current_date < date2:
            current_date = (datetime.strptime(
                current_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            # print(current_date)
            date_range.append(current_date)

        # Construct the update query dynamically
        update_query = {
            "$set": {
                "isWeekendFormat": False
            }
        }

        for date in date_range:
            update_query["$set"][f"changedPrice.{date}"] = price

        # print(update_query)
        db.Rooms.find_one_and_update(
            {"ndid": ndid, "hId": hId, "roomType": roomType}, update_query)
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False
# 4


def update_price_of_rooms_on_rangeBooking(room_details):
    try:
        token = room_details.get("token")
        roomType = room_details.get("roomType")
        date1 = room_details.get("date1")
        date2 = room_details.get("date2")
        priceweakday = room_details.get("priceweakday")
        priceweakend = room_details.get("priceweakend")
        hId = room_details.get("hId")
        ndid = utils.get_ndid(token)
        date_range = []
        current_date = date1
        while current_date < date2:
            current_date = (datetime.strptime(
                current_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            # print(current_date)
            date_range.append(current_date)

        update_query = {
            "$set": {
                "isWeekendFormat": False
            }
        }

        for date in date_range:
            if (is_weekend(date)):
                update_query["$set"][f"changedPrice.{date}"] = priceweakend
            else:
                update_query["$set"][f"changedPrice.{date}"] = priceweakday

        # print(update_query)
        db.Rooms.find_one_and_update(
            {"ndid": ndid, "hId": hId, "roomType": roomType}, update_query)
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False
# 3


def update_weekend_weakday_price(room_details):
    try:
        token = room_details.get("token")
        roomType = room_details.get("roomType")
        weekend = room_details.get("weekend")
        weekDay = room_details.get("weekday")
        hId = room_details.get("hId")
        ndid = utils.get_ndid(token)
        print("To Update")

        room = db.Rooms.find_one_and_update({"ndid": ndid, "hId": hId, "roomType": roomType}, {"$set": {
            "isWeekendFormat": True,
            "changedPrice": {
                "weekend": weekend,
                "weekday": weekDay
            }
        }})

        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False
# 4


def update_bulk_price_of_rooms(room_details):
    try:
        token = room_details.get("token")
        # {"1":{"2023-10-19":"1700","2023-10-27":"2200"},"2":{"2023-10-22":"3300"}}
        Data = room_details.get("bulkprice")
        hId = room_details.get("hId")
        ndid = utils.get_ndid(token)

        room = db.Rooms.find({"ndid": ndid, "hId": hId})  # all rooms
        totalrooms = []
        for r in room:
            totalrooms.append(r)

        for room in totalrooms:
            roomType = room["roomType"]
            if roomType in Data:
                roomPrice = room.get("changedPrice")
                data_for_room = Data[roomType]

                for date, price in data_for_room.items():
                    roomPrice[date] = price

                update_query = {
                    "$set": {
                        "isWeekendFormat": False,
                        "changedPrice": roomPrice
                    }
                }

                db.Rooms.find_one_and_update(
                    {"ndid": ndid, "hId": hId, "roomType": roomType}, update_query)
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False
# 5


def get_next_dates_from_today(number):
    try:
        current_date = datetime.today().date()
        dates = [current_date]
        for i in range(1, number):
            next_n_days = current_date + timedelta(days=i)
            dates.append(next_n_days)

        return dates
    except Exception as ex:
        logging.error(f"{ex}")
        return None
# 7


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


def update_price_days_wise(details):
    try:
        token = details.get("token")
        roomtype = details.get("roomtype")
        Mon = details.get("Mon")
        Tue = details.get("Tue")
        Wed = details.get("Wed")
        Thu = details.get("Thu")
        Fri = details.get("Fri")
        Sat = details.get("Sat")
        Sun = details.get("Sun")
        start_date = details.get("start_date")
        end_date = details.get("end_date")
        hId = details.get("hId")

        ndid = utils.get_ndid(token)
        room = db.Rooms.find_one(
            {"ndid": ndid, "roomType": roomtype, "hId": hId})
        roomPrice = room.get("changedPrice")

        days = {}
        if Mon != "None":
            days["Mon"] = Mon
        if Tue != "None":
            days["Tue"] = Tue
        if Wed != "None":
            days["Wed"] = Wed
        if Thu != "None":
            days["Thu"] = Thu
        if Fri != "None":
            days["Fri"] = Fri
        if Sat != "None":
            days["Sat"] = Sat
        if Sun != "None":
            days["Sun"] = Sun

        dates = get_dates_in_range(start_date, end_date)
        for i in dates:
            a = return_weakday(str(i))
            if (a in days):
                i = str(i)
                roomPrice[i] = days[a]

        update_query = {
            "$set": {
                "isWeekendFormat": False,
                "changedPrice": roomPrice
            }
        }

        db.Rooms.find_one_and_update(
            {"ndid": ndid, "roomType": roomtype, "hId": hId}, update_query)

        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False


def update_price_percent_wise(details):
    try:
        token = details.get("token")
        roomtype = details.get("roomtype")
        percent = details.get("percent")
        start_date = details.get("start_date")
        end_date = details.get("end_date")
        hId = details.get("hId")

        ndid = utils.get_ndid(token)
        room = db.Rooms.find_one(
            {"ndid": ndid, "roomType": roomtype, "hId": hId})
        roomPrice = room.get("changedPrice")

        dates = get_dates_in_range(start_date, end_date)

        for i in dates:
            if (str(i) in roomPrice):
                newprice = ((int(percent)/100) *
                            int(roomPrice[str(i)]))+int(roomPrice[str(i)])
                roomPrice[str(i)] = str(int(newprice))
            else:
                newprice = ((int(percent)/100) *
                            int(room["price"]))+int(room["price"])
                roomPrice[str(i)] = str(int(newprice))

        update_query = {
            "$set": {
                "isWeekendFormat": False,
                "changedPrice": roomPrice
            }
        }

        db.Rooms.find_one_and_update(
            {"ndid": ndid, "roomType": roomtype, "hId": hId}, update_query)

        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False


def update_weekend_format(room_details):
    try:
        logging.info(f"{room_details}")
        token = room_details.get("token")
        roomType = room_details.get("roomType")
        isWeekendFormat = room_details.get("isWeekendFormat")
        hId = room_details.get("hId")
        ndid = utils.get_ndid(token)
        print("To Update")
        if (isWeekendFormat == "true"):
            room = db.Rooms.find_one_and_update({"ndid": ndid, "hId": hId, "roomType": roomType}, {"$set": {
                "isWeekendFormat": isWeekendFormat == "true",
                "changedPrice": {
                    "weekend": "1900",
                    "weekday": "1980"
                }
            }})
        else:
            room = db.Rooms.find_one_and_update({"ndid": ndid, "hId": hId, "roomType": roomType}, {"$set": {
                "isWeekendFormat": isWeekendFormat == "true",
                "changedPrice": {}
            }})

        logging.info(f"True")
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False


def get_dates_in_range(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        # Calculate the number of days between start_date and end_date
        delta = end_date - start_date

        # Generate a list of dates within the date range
        date_list = [start_date + timedelta(days=i)
                     for i in range(delta.days + 1)]

        return date_list
    except Exception as ex:
        logging.error(f"{ex}")
        return None


def return_weakday(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Get the day name using the day_of_week as an index
        day_name = day_names[date.weekday()]
        return day_name
    except Exception as ex:
        logging.error(f"{ex}")
        return None
