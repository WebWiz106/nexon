import utils
import constants
import pymongo
import json
import settings
import logging
import datetime
from bson import json_util
from usecases import booking_usecase
from model.dashboardpackages import DashboardPackage
from datetime import datetime, date, timedelta
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)
from utils import db


def inHouse_and_todayOccupied(token,hId):
    try:
        ndid=utils.get_ndid(token)
        today_date_str = datetime.now().strftime("%Y-%m-%d")

        # Convert the string to a datetime object
        today_date = datetime.strptime(today_date_str, "%Y-%m-%d")
        allBooking=db.Bookings.find({"hId":hId,"ndid":ndid})
        bookedroom=0
        rooms=db.Rooms.find({"hId":hId,"ndid":ndid})
        totalRoom=0
        for room in rooms:
            totalRoom+=int(room.get("noOfRooms"))
        # print(allBooking)
        personstaying=0
        for booking in allBooking:
            print(booking)
            checkin_str = booking.get("checkIn")
            checkout_str = booking.get("checkOut")
            
            if checkin_str and checkout_str:
                checkin = datetime.strptime(checkin_str, "%Y-%m-%d")
                checkout = datetime.strptime(checkout_str, "%Y-%m-%d")
                
                print(type(checkin), type(today_date), type(checkout))
                print(checkin, today_date, checkout)
                print(checkin <= today_date <= checkout)
                if checkin <= today_date <= checkout:
                    bookedroom += 1
                    personstaying = int(booking.get("Adults")) + int(booking.get("Kids"))
        data={
            "bookedroom":bookedroom,
            "totalRoom":totalRoom,
            "personstaying":personstaying
        }
        logging.info(f"Analtics detail for ndid {ndid} hid {hId} bookedroom {bookedroom} totalRoom {totalRoom} personstaying {personstaying}" )
        return True,data
    except Exception as ex:
        return False