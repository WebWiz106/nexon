import utils
import constants
import pymongo
import json
import string
import settings
import logging
import uuid
import requests
import hashlib
from bs4 import BeautifulSoup
import urllib.request
import os
from urllib.parse import urljoin
import math
from bson import json_util
from usecases import mail_usecase
from pathlib import Path
import re

from datetime import datetime, date, timedelta
from usecases import room_usecase
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db
def otas_create_usecase(maintenance_details,ndid,hId):
    try:
        hotel={
            "hId":hId,
            "ndid":ndid,
            "country":maintenance_details.get("hotelCountry"),
            "street": maintenance_details.get("hotelAddress"),
            "postcode": maintenance_details.get("hotelPinCode"),
            "city": maintenance_details.get("hotelCity"),
            "hotelName": maintenance_details.get("hotelName"),
            "starRating": maintenance_details.get("starRating"),
            "hasPool": maintenance_details.get("hasPool"),
            "amenities":[key for key, value in maintenance_details.get("Facilities").items() if value == "true"],
            "breakfastOption": maintenance_details.get("breakfastOption"),
            "address": maintenance_details.get("hotelAddress"),
            "serveBreakfast":maintenance_details.get("serveBreakfast"),
            "breakfastIncluded":maintenance_details.get("breakfastIncluded"),
            "parkingAvailability":maintenance_details.get("parkingAvailability"),
            "parkingCost":maintenance_details.get("parkingCost"),
            "pricingStructure":maintenance_details.get("pricingStructure"),
            "reservationRequirement":maintenance_details.get("reservationRequirement"),
            "parkingLocation":maintenance_details.get("parkingLocation"),
            "parkingType":maintenance_details.get("parkingType"),
            "languages":maintenance_details.get("languages"),
            "checkInFrom":maintenance_details.get("checkInFrom"),
            "checkInUntil":maintenance_details.get("checkInUntil"),
            "checkOutFrom":maintenance_details.get("checkOutFrom"),
            "checkOutUntil":maintenance_details.get("checkOutUntil"),
            "allowChildren":maintenance_details.get("allowChildren"),
            "petCharges":maintenance_details.get("petCharges"),
            "allowPets":maintenance_details.get("allowPets"),
            "roomDetails":[]
        }
        for val in maintenance_details.get("roomCategories"):
            if val.get("child")!=0 and hotel["allowChildren"]=="false":
                return False,f"Ota process failed ,either make allowChildren true or make child value in roomtype {val.get('roomType')} equal 0"
        for room in maintenance_details.get("roomCategories"):
            arr={
                "numberOfRooms":room.get("noOfRooms"),
                "roomname":room.get("roomName"),
                "guestCapacity":int(room.get("child"))+int(room.get("adult")),
                "pricePerNight":room.get("price"),
                "roomAmenities":room.get("roomFacilities"),

                "outdooroptions":room.get("outdooroptions"),
                "foodanddrink":room.get("foodanddrink"),
                "roomSize":room.get("roomSize"),
                "roomSizeUnit":room.get("roomSizeUnit"),
                "smokingAllowed":room.get("smokingAllowed"),
                "bathroomPrivacy":room.get("bathroomPrivacy"),
                "bathroomOptions":room.get("bathroomOptions"),
            }
            hotel["roomDetails"].append(arr)

        # print(hotel)
        db.OTADetails.insert_one(hotel)
        return True,"Ota process Successful"
    except Exception as ex:
        return False,f"Ota process Failed"
    


def getOTAinformations(token,locationid):
    try:
        ndid = utils.get_ndid(token)

        details = db.OTADetails.find_one({"ndid":ndid,"hId":locationid})
        return details
    
    except:
        return {}