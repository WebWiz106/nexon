import utils
import constants
import pymongo
import json
import settings
import logging

from bson import json_util
from usecases import booking_usecase
from model.dashboardpackages import DashboardPackage
from datetime import datetime, date, timedelta
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)
from utils import db


# ?not req


def get_id(booking_count):
    try:
        for i in range(5 - len(booking_count)):
            booking_count = "0" + booking_count
        logging.info(f"{booking_count}")
        return booking_count
    except Exception as e:
        logging.error(f"An error occured:{e}")
        return None

# ?not done


def get_adpackage_id():
    try:
        query = {
            "packageCreatedAt": {
                "$gte": str(date.today()) + " 00:00",
                "$lte": str(date.today()) + " 23:59"
            }
        }
        # print("entered")
        plan_count = str(db.Ads_Packages.count_documents(query)+1)
        logging.info(f"{plan_count}")
        return "ADPACKAGE" + date.today().strftime("%Y%m%d") + get_id(plan_count)
    except Exception as e:
        error_message = f"An error occurred in getting ad package: {e}"
        logging.error(error_message)
        return None

# ?not done


def get_ad_packages_hotel(ndid, hId):
    try:
        packages = []
        plans = db.Ads_Packages.find({"ndid": ndid, "hId": hId})
        for p in plans:
            packages.append(p)
        logging.info(f"{packages}")
        return packages
    except Exception as e:
        error_message = f"An error occurred in getting (ndid: {ndid}, hId: {hId}): {e}"
        logging.error(error_message)
        return None

# ?not done


def get_ad_packages_for_specific_dates(ndid, booking_details):
    try:
        checkin_date = booking_details.get("checkin")
        checkout_date = booking_details.get("checkout")
        hId = booking_details.get("hId")
        plans = db.Ads_Packages.find(
            {
                "hId": hId,
                "ndid": ndid,
                "packageStart": {
                    "$lte": checkin_date
                },
                "packageEnd": {
                    "$gte": checkout_date
                }
            }
        )
        packages = []
        for p in plans:
            packages.append(p)
        logging.info(f"{packages}")
        return packages
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error occurred in getting ad package for specific date (ndid: {ndid}, hId: {hId}): {e}"
        logging.error(error_message)
        return None  # or raise an exception or handle it accordingly

# ?model done


def create_ad_package(plan_details):
    try:
        logging.info(f"{plan_details}")
        package = DashboardPackage.from_dict(plan_details)
        token = plan_details.get("token")
        package.ndid = utils.get_ndid(token)
        package.packageId = get_adpackage_id()
        package.packageCreatedAt = str(datetime.now())
        db.Ads_Packages.insert_one(DashboardPackage.to_dict(package))

        logging.info("True")
        return True
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error in creation adpackage: {e}"
        logging.error(error_message)
        return False

#?model done
def edit_ad_package(plan_details):
    try:
        logging.info(f"{plan_details}")
        adpackage = DashboardPackage.from_dict(plan_details)
        token = plan_details.get("token")
        adpackage.ndid = utils.get_ndid(token)
        print(adpackage.ndid, adpackage.hId, adpackage.packageId)
        adpackage_exist = db.Ads_Packages.find_one(
            {"ndid": adpackage.ndid, "hId": adpackage.hId, "packageId": adpackage.packageId})
        if adpackage_exist:
            prevadpackage = DashboardPackage.from_dict(adpackage_exist)
            adpackage.packageCreatedAt = prevadpackage.packageCreatedAt
            print(adpackage.to_dict())
            db.Ads_Packages.find_one_and_update(
                {"ndid": adpackage.ndid, "hId": adpackage.hId, "packageId": adpackage.packageId}, {"$set": adpackage.to_dict()})
            logging.info("adpackge Updated")
            return True
        else:
            return False
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error in editing adpackage: {e}"
        logging.error(error_message)
        return False


def delete_ad_package(plan_details):
    try:
        logging.info(f"{plan_details}")
        token = plan_details.get("token")
        packageId = plan_details.get("packageId")
        hId = plan_details.get("hId")
        ndid = utils.get_ndid(token)
        db.Ads_Packages.find_one_and_delete(
            {"ndid": ndid, "hId": hId, "packageId": packageId})
        logging.info(f"True")
        return True
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error in deleting adpackageId: {packageId}, hId: {hId}: {e}"
        logging.error(error_message)
        return False
