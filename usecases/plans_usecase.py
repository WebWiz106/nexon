import utils
import constants
import pymongo
import json
import settings
import logging

from bson import json_util
from usecases import booking_usecase,admin_usecase
from datetime import datetime, date, timedelta

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db



def addplanEazotel(details):
    try:
        token = details.get("token")
        planName = details.get("planName")
        planPrice = details.get("planPrice")
        planfeatures = details.get("planfeatures")
        planDescription = details.get("planDescription")
        planTenure = details.get("planTenure")
        bookingEngine = details.get("bookingEngine")=="true"
        ota = details.get("ota")=="true"
        website = details.get("website")=="true"

        isowner = admin_usecase.admin_is_owner(token)

        if isowner:
            db.Zucks_plans.insert_one({
                "planName":planName,
                "planPrice":planPrice,
                "planfeatures":{
                    "socialMedia":planfeatures.get("socialMedia",False)=="true",
                    "channelManager":planfeatures.get("channelManager",False)=="true",
                    "seoManager":planfeatures.get("seoManager",False)=="true",
                    "paymentGateway":planfeatures.get("paymentGateway",False)=="true",
                    "reservationDesk":planfeatures.get("reservationDesk",False)=="true",
                    "Frontdesk":planfeatures.get("Frontdesk",False)=="true",
                    "fnbManager":planfeatures.get("fnbManager",False)=="true",
                    "whatsapp":planfeatures.get("whatsapp",False)=="true",
                    "leadsMgmt":planfeatures.get("leadsMgmt",False)=="true"
                },
                "planDescription":planDescription,
                "planTenure":planTenure,
                "bookingEngine":bookingEngine,
                "ota":ota,
                "website":website
            })
        

            return True,"Plan Created Successfully"
        else:
            return False,"You don't have access to create"

    except:
        return False,"Some Problem"


def deleteplanEazotel(details):
    try:
        token = details.get("token")
        isowner = admin_usecase.admin_is_owner(token)

        if isowner:
            planName = details.get("planName")

            db.Zucks_plans.find_one_and_delete({"planName":planName})

            return True,"Plan Deleted Successfully"
        else:
            return False,"You don't have access to delete"
    
    except:
        return False,"Some Problem"