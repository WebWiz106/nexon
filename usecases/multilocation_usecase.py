import utils
import constants
import pymongo
import json
import settings
import logging
import random

from bson import json_util
from datetime import datetime, date, timedelta

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db


def create_location_id():
    try:
        lower_bound = 10 ** (8 - 1)
        upper_bound = 10**8 - 1
        return str(random.randint(lower_bound, upper_bound))
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


def find_locations_of_hotel(ndid):
    # {"location":"Delhi","pinCode":"244553","hId":"11338813"}
    try:
        profile = db.Zucks_profile.find_one({"uId": ndid})
        # print(profile)
        locations = []
        allLocations = profile.get("hotels")
        for i in allLocations:
            dictonary = {}
            dictonary["location"] = allLocations[i]["location"]
            dictonary["pinCode"] = allLocations[i]["pinCode"]
            dictonary["hId"] = i
            locations.append(dictonary)

        return True, locations

    except:
        return False, []


def add_website_data_based_on_location(hid, ndid):
    data = db.WebsiteData.find_one({"ndid": ndid})

    if not data:
        print("No website data found for ndid:", ndid)
        return {}

    hotels = data["hotels"][0]
    details = hotels["Details"]

    return hotels


def add_locations_of_hotel(location_details):
    try:
        logging.info(f"Details sended to add:- {location_details}")
        token = location_details.get("token")
        local = location_details.get("local")
        city = location_details.get("city")
        state = location_details.get("state")
        country = location_details.get("country")
        # name = location_details.get("name")
        pincode = location_details.get("pincode")

        ndid = utils.get_ndid(token)
        profile = db.Zucks_profile.find_one({"uId": ndid})

        # print("fghhjkkl", profile)

        locationdetails = profile.get("hotels")
        new_location = create_location_id()
        locationdetails[new_location] = {
            "local": local,
            "city": city,
            "state": state,
            "country": country,
            "pinCode": pincode,
        }

        hid = next(iter(locationdetails))

        websiteUpdatedData = add_website_data_based_on_location(hid, ndid)
        new_hotel_object = {
            new_location:websiteUpdatedData,  # or {} if no data is needed here
        }

        # print("new object", new_hotel_object)

        engine_data = db.BookingEngineData.find_one({"ndid": ndid, "hId": hid})
        # print(engine_data.get("Details"))

        # * updating
        profile_updating = db.Zucks_profile.find_one_and_update(
            {"uId": ndid}, {"$set": {"hotels": locationdetails}}
        )
        details = db.WebsiteData.find_one({"ndid": ndid})
        data = details["hotels"]
        data[new_location] = websiteUpdatedData

        # updating website data
        db.WebsiteData.update_one(
            {"ndid": ndid},
            {"$push": {"hotels": data}},
        )

        # print(profile_updating)
        # * add booking engine data
        engine_data = db.BookingEngineData.insert_one(
            {"ndid": ndid, "hId": new_location, "Details": engine_data.get("Details")}
        )
        return True
    except:
        logging.error(f"Expect block prints for add Location")
        return False


def edit_locations_of_hotel(location_details):
    try:
        logging.info(f"Details sended to add:- {location_details}")
        token = location_details.get("Token")
        locationid = location_details.get("hId")
        name = location_details.get("Name")
        pincode = location_details.get("pincode")

        ndid = utils.get_ndid(token)
        profile = db.Zucks_profile.find_one({"uId": ndid})

        locationdetails = profile.get("hotels")
        locationdetails[locationid] = {"location": name, "pinCode": pincode}

        # updating
        profile_updating = db.Zucks_profile.find_one_and_update(
            {"uId": ndid}, {"$set": {"hotels": locationdetails}}
        )
        return True, "Location edited successfully!!"
    except:
        logging.error(f"Expect block prints for edit Location")
        return False, "Request failed to execute"


def delete_locations_of_hotel(location_details):
    try:
        logging.info(f"Details sended to delete:- {location_details}")
        token = location_details.get("Token")
        locationid = location_details.get("hId")

        ndid = utils.get_ndid(token)
        profile = db.Zucks_profile.find_one({"uId": ndid})

        locationdetails = profile.get("hotels")

        if len(locationdetails) > 1:
            del locationdetails[locationid]

        else:
            return False, "Only One location is their , can not delete"

        # print(locationdetails)
        # updating
        profile_updating = db.Zucks_profile.find_one_and_update(
            {"uId": ndid}, {"$set": {"hotels": locationdetails}}
        )

        bookingdata_updating = db.BookingEngineData.find_one_and_delete(
            {"ndid": ndid, "hId": locationid}
        )

        rooms = db.Rooms.find({"ndid": ndid, "hId": locationid})
        for room in rooms:
            db.Rooms.find_one_and_delete(
                {"ndid": ndid, "hId": locationid, "roomType": room.get("roomType")}
            )

        return True, "Location deleted Successfully"
    except:
        logging.error(f"Expect block prints for Delete Location")
        return False
