import utils
import constants
import pymongo
import json
import settings
import logging

from bson import json_util
from usecases import mail_usecase


from datetime import datetime, date, timedelta
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db


def verify_acess_token_db(ndid):
    try:
        try:
            profile = db.Zucks_profile.find_one({"uId":ndid})
            dinabitetoken = profile["dinabiteToken"].get("access_token")
            if(dinabitetoken=="None"):
                return False,"None"
            else:
                return True,dinabitetoken
        except:
            return False,"Profile Not found"
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)
    

def update_acess_token_db(data):
    token = data.get("token")
    accesstoken = data.get("access_token")

    ndid = utils.get_ndid(token)
    try:
        try:
            profile = db.Zucks_profile.find_one_and_update({"uId":ndid},{"$set":{
                "dinabiteToken.access_token":accesstoken
            }})
            return True,"Token Updated"
        except:
            return False,"Profile Not found"
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)