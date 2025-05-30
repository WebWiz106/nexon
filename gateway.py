import pymongo
import settings
from bson.binary import Binary
import base64
from utils import db


def get_profile(ndid):
    data= db.WebsiteData.find_one({"ndid":ndid})
    return data["Details"]["Reviews"]



