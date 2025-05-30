import utils
import constants
import pymongo
import json
import settings
import logging

from bson import json_util
from usecases import booking_usecase
from datetime import datetime, date, timedelta
from model.dashboardmealplan import DashboardMealPlan
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db

# ?not req


def get_id(booking_count):
    try:
        logging.info(f"{booking_count}")
        for i in range(5 - len(booking_count)):
            booking_count = "0" + booking_count
        logging.info(f"{booking_count}")
        return booking_count
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error occurred while processing booking count: {e}"
        logging.error(error_message)
        return None

# ?not done


def get_plan_id():
    try:
        query = {
            "planCreatedAt": {
                "$gte": str(date.today()) + " 00:00",
                "$lte": str(date.today()) + " 23:59"
            }
        }
        print("entered")
        plan_count = str(db.Meal_Packages.count_documents(query)+1)
        logging.info(f"{plan_count}")
        return "PLAN" + date.today().strftime("%Y%m%d") + get_id(plan_count)
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error occurred while getting plan id: {e}"
        logging.error(error_message)
        return None

# ?done


def create_package(plan_details):
    try:
        logging.info(f"{plan_details}")
        meal = DashboardMealPlan.from_dict(plan_details)
        token = plan_details.get("token")
        # packageName = plan_details.get("package_name")
        # packageDesc = plan_details.get("package_description")
        # packagePrice = plan_details.get("plan_price")
        # packageImage = plan_details.get("plan_image")
        # planStart = plan_details.get("plan_start")
        # planEnd = plan_details.get("plan_end")
        # isPerRoom = plan_details.get("isPerRoom")
        # hId = plan_details.get("hId")
        ndid = utils.get_ndid(token)
        meal.planCreatedAt = str(datetime.now())
        meal.planId = get_plan_id()
        meal.ndid = ndid
        print(meal.to_dict())
        db.Meal_Packages.insert_one(DashboardMealPlan.to_dict(meal))
        # db.Meal_Packages.insert_one({
        #     "hId": hId,
        #     "ndid": ndid,
        #     "planId": get_plan_id(),
        #     "packageName": packageName,
        #     "packageDesc": packageDesc,
        #     "packagePrice": packagePrice,
        #     "packageImage": packageImage,
        #     "planStart": planStart,
        #     "planEnd": planEnd,
        #     "isPerRoom": isPerRoom == "true",
        #     "planCreatedAt": str(datetime.now())
        # })
        logging.info("True")
        return True
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error occurred while creating meal package: {e}"
        logging.error(error_message)
        return None

# ?not done


def get_packages_hotel(ndid, hId):
    try:
        logging.info(f"{ndid},{hId}")
        packages = []
        plans = db.Meal_Packages.find({"ndid": ndid, "hId": hId})
        for p in plans:
            packages.append(p)
        logging.info(f"{packages}")
        return packages
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error occurred while getting package hotel: {e}"
        logging.error(error_message)
        return None

# ?done


def edit_package(plan_details):
    try:
        logging.info(f"{plan_details}")
        token = plan_details.get("token")
        hId = plan_details.get("hId")
        ndid = utils.get_ndid(token)
        planId = plan_details.get("planId")
        mpackage = db.Meal_Packages.find_one(
            {"ndid": ndid, "hId": hId, "planId": planId})
        print(ndid, hId, planId)
        if mpackage:
            prev_mpackage = DashboardMealPlan.from_dict(mpackage)
            new_mpackage = DashboardMealPlan.from_dict(plan_details)
            new_mpackage.ndid = prev_mpackage.ndid
            new_mpackage.planCreatedAt = prev_mpackage.planCreatedAt
            db.Meal_Packages.find_one_and_update(
                {"ndid": ndid, "hId": hId, "planId": planId}, {"$set": new_mpackage.to_dict()})
        else:
            return False, "Meal Package not found or not updated"
        logging.info("True")
        return True
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error occurred while editing meal package: {e}"
        logging.error(error_message)
        return None

# ?not required


def delete_package(plan_details):
    try:
        logging.info(f"{plan_details}")
        token = plan_details.get("token")
        planId = plan_details.get("planId")
        hId = plan_details.get("hId")
        ndid = utils.get_ndid(token)
        db.Meal_Packages.find_one_and_delete(
            {"ndid": ndid, "hId": hId, "planId": planId})
        logging.info("True")
        return True
    except Exception as e:
        # Handle exceptions and log the error
        error_message = f"An error occurred while Deleting meal package: {e}"
        logging.error(error_message)
        return None
