import jwt
import logging
import settings

import pymongo
from datetime import datetime, timedelta
from random import *
from usecases import user_usecase

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

client = pymongo.MongoClient(settings.DBURL)

print("===========================Database============================")
print(client)
print(f"DB Name from settings: {settings.DBNAME} (Type: {type(settings.DBNAME)})")
# db = client[settings.DBNAME]
db = client["Courage"]
# db = client["Courage"]
# db = "Courage"


def create(data={}):
    try:
        expiry_date = datetime.now() + timedelta(days=15)
        data["exp"] = expiry_date.timestamp()
        token = jwt.encode(data, settings.JWT_SECRETS, algorithm=settings.JWT_ALGORITHM)
        return token
    except Exception as err:
        print("Token creation error:", err)
        return None


def Decode_jwt(token):
    data = jwt.decode(token, settings.JWT_SECRETS, algorithms=[settings.JWT_ALGORITHM])
    # This TOKEN have EMAIL AND PASSWORD of the user loggedin currently
    for i in data:
        if isinstance(data[i], str):
            data[i] = data[i]
        else:
            data[i] = data[i]

    # if "exp" in data and datetime.now().timestamp() > data["exp"]:
    #         raise ValueError("Token has expired")

    return data


def get_ndid(token):
    try:
        data = Decode_jwt(token)
        user = user_usecase.get_user(data["Email"])
        ndid = user.get("ndid")
        return ndid
    except Exception as ex:
        raise ValueError("Unable to decode token error : {}", ex)


def get_name(token):
    try:
        data = Decode_jwt(token)
        user = user_usecase.get_user(data["Email"])
        name = user.get("userName")
        return name
    except Exception as ex:
        raise ValueError("Unable to decode token error : {}", ex)


def get_email(token):
    try:
        data = Decode_jwt(token)
        return data["Email"]
    except Exception as ex:
        raise ValueError("Unable to decode token error : {}", ex)


def getdata(token):
    try:
        data = Decode_jwt(token)
        return data
    except Exception as ex:
        raise ValueError("Unable to decode token error : {}", ex)
