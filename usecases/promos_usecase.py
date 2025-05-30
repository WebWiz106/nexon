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

def get_promo_id():
    try:
        query = {
            "promoCreatedAt": {
                "$gte": str(date.today()) + " 00:00",
                "$lte": str(date.today()) + " 23:59"
            }
        }
        print("entered")
        plan_count = str(db.Promo_Codes.count_documents(query)+1)
        logging.info(f"{plan_count}")
        return "PROMO" + date.today().strftime("%Y%m%d") + get_id(plan_count)
    except Exception as ex:
        logging.error(f"{ex}")
        return None


def get_id(booking_count):
    try:
        logging.info(f"{booking_count}")
        for i in range(5 - len(booking_count)):
            booking_count = "0" + booking_count
        logging.info(f"{booking_count}")
        return booking_count
    except Exception as ex:
        logging.error(f"{ex}")
        return None


def get_promos_for_hotel(ndid,hId):
    try:
        logging.info(f"{ndid}")
        promos = []
        hotelPromos = db.Promo_Codes.find({"ndid": ndid,"hId":hId})
        for promo in hotelPromos:
            promos.append(promo)
        logging.info(f"{promos}")
        return promos
    except Exception as ex:
        logging.error(f"{ex}")
        return None


def create_promo_for_hotel(promo_details):
    try:
        logging.info(f"{promo_details}")
        token = promo_details.get("token")
        promoHeading = promo_details.get("promoHeading")
        promoDesc = promo_details.get("promoDescription")
        promoCode = promo_details.get('promoCode')
        ispercent = promo_details.get("ispercent")
        discountAmount = promo_details.get("discountAmount")
        startDate = promo_details.get("startDate")
        endDate = promo_details.get("endDate")
        hId = promo_details.get("hId")
        ndid = utils.get_ndid(token)
        print(promo_details)
        db.Promo_Codes.insert_one({
            "hId": hId,
            "ndid": ndid,
            "promoId": get_promo_id(),
            "promoHeading": promoHeading,
            "promoDescription": promoDesc,
            "promoCode": promoCode,
            "ispercent": ispercent == "true",
            "discountAmount": discountAmount,
            "promoStartDate": startDate,
            "promoEndDate": endDate,
            "promoCreatedAt": str(datetime.now())
        })
        logging.info(f"{True}")
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False


def edit_promo_for_hotel(promo_details):
    try:
        logging.info(f"{promo_details}")
        token = promo_details.get("token")
        promoId = promo_details.get("promoId")
        promoHeading = promo_details.get("promoHeading")
        promoDesc = promo_details.get("promoDescription")
        promoCode = promo_details.get('promoCode')
        ispercent = promo_details.get("ispercent")
        discountAmount = promo_details.get("discountAmount")
        startDate = promo_details.get("startDate")
        endDate = promo_details.get("endDate")

        ndid = utils.get_ndid(token)
        hId = promo_details.get("hId")
        db.Promo_Codes.find_one_and_update({"ndid": ndid, "hId": hId, "promoId": promoId}, {"$set": {
            "promoHeading": promoHeading,
            "promoDescription": promoDesc,
            "promoCode": promoCode,
            "ispercent": ispercent == "true",
            "discountAmount": discountAmount,
            "promoStartDate": startDate,
            "promoEndDate": endDate,
        }})
        logging.info(f"{True}")
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False


def delete_promo_for_hotels(promo_details):
    try:
        logging.info(f"{promo_details}")
        token = promo_details.get("token")
        promoId = promo_details.get("promoId")
        hId = promo_details.get("hId")
        ndid = utils.get_ndid(token)
        db.Promo_Codes.find_one_and_delete(
            {"ndid": ndid, "hId": hId, "promoId": promoId})
        logging.info(f"{True}")
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False
