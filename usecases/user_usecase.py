import utils
import hashlib
import pymongo
import settings
import logging
import json

from bson import json_util
from datetime import datetime
from model.user import User

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


def get_user(email_id):
    try:
        logging.info(f"{email_id}")
        user_data = utils.db.Zucks_users.find_one({"emailId": email_id})

        if user_data:
            user_dict = User.to_dict(User.from_dict(user_data))
            logging.info(f"{user_dict}")
            return user_dict
        else:
            logging.info("User not found")
            return None
    except Exception as ex:
        logging.error(ex)
        return None


def get_all_user(token):
    try:
        logging.info(f"{token}")
        ndid = utils.get_ndid(token)
        users_all = utils.db.Zucks_users.find({"ndid": ndid})
        users_list = [user for user in users_all]

        logging.info(f"{users_list}")
        return users_list
    except Exception as ex:
        logging.error(ex)
        return None


def test_add_user(content, token):
    try:
        user = User.from_dict(content)
        # print("shjdgfjshdgf", user.get("emailId"))

        emailId = content.get("emailId", None)
        user_alreadyExists = get_user(emailId)
        if user_alreadyExists:
            raise Exception("User already exists with this email id")

        ndid = utils.get_ndid(token)
        user.ndid = ndid
        user.accesskey = hashlib.sha256(
            content.get("access_id", "").encode("utf-8")
        ).hexdigest()
        user.createdAt = str(datetime.utcnow())
        utils.db.Zucks_users.insert_one(User.to_dict(user))
        logging.info("User Created Successfully")
        return {"Status": True, "Message": "User Created Successfully"}
    except Exception as ex:
        error_message = str(ex)
        logging.error(error_message)
        return {"Status": False, "Message": error_message}


# def add_user(content, token):
#     try:
#         user = User.from_dict(content)
#         emailId = content.get("emailId", None)
#         user_alreadyExists = get_user(emailId)
#         if user_alreadyExists:
#             raise Exception("User already exists with this email id")

#         ndid = utils.get_ndid(token)
#         user.ndid = ndid
#         user.accesskey = hashlib.sha256(content.get(
#             "access_id", "").encode("utf-8")).hexdigest()
#         user.createdAt = str(datetime.utcnow())
#         utils.db.Zucks_users.insert_one(User.to_dict(user))
#         logging.info("User Created Successfully")
#         return {"Status": True, "Message": "User Created Successfully"}
#     except Exception as ex:
#         error_message = str(ex)
#         logging.error(error_message)
#         return {"Status": False, "Message": error_message}


def test_edit_user(content, token):
    try:
        user = User.from_dict(content)
        # print("Parsed user object:", user)

        logging.info(f"{content},{token}")
        emailId = content.get("emailId", None)
        user_exists = get_user(emailId)
        # print(user_exists)

        # return user_exists

        if user_exists:
            user.ndid = user_exists.get("ndid")
            user.accesskey = user_exists.get("accesskey")
            user.createdAt = user_exists.get("createdAt")
            utils.db.Zucks_users.find_one_and_update(
                {"emailId": emailId}, {"$set": User.to_dict(user)}
            )
            logging.info("User Edited Successfully")
            return "User Edited Successfully"
        else:
            return "User does not Exists"
    except Exception as ex:
        logging.error(ex)
        return None


# def edit_user(content, token):
#     try:
#         user = User.from_dict(content)
#         logging.info(f"{content},{token}")
#         emailId = content.get("emailId", None)
#         user_exists = get_user(emailId)
#         if user_exists:
#             user.ndid = user_exists.get("ndid")
#             user.accesskey = user_exists.get("accesskey")
#             user.createdAt = user_exists.get("createdAt")
#             utils.db.Zucks_users.find_one_and_update(
#                 {"emailId": emailId}, {"$set": User.to_dict(user)}
#             )
#             logging.info("User Edited Successfully")
#             return "User Edited Successfully"
#         else:
#             return "User does not Exists"
#     except Exception as ex:
#         logging.error(ex)
#         return None


def delete_user(email):
    try:
        logging.info(f"{email}")
        utils.db.Zucks_users.find_one_and_delete({"emailId": email})
        logging.info("Deleted")
        return "Deleted"
    except Exception as ex:
        logging.error(ex)
        return None
