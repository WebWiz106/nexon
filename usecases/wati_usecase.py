import utils
import constants
import pymongo
import json
import settings
import logging
import requests
from model.room import Room
from bson import json_util
from usecases import booking_usecase
from datetime import datetime, date, timedelta
from model.roomFacilities import RoomFacility
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db


def addWatiCred(token,data):
    try:
        ndid=utils.get_ndid(token)
        obj={
            "tenantId":data.get("tenantId"),
            "watiAccessToken":data.get("watiAccessToken")
        }
        db.Zucks_profile.find_one_and_update({"uId":ndid},{"$set":{"watiCreds":obj}})
        return True
    except Exception as ex:
        return False



def getWatiCreds(token):
    try:
        ndid=utils.get_ndid(token)
        return True, db.Zucks_profile.find_one({"uId":ndid}).get("watiCreds")
    except Exception as ex:
        return False, "None"
   


def getContact(token):
    try:
        ndid=utils.get_ndid(token)
        obj=db.Zucks_profile.find_one({"uId":ndid}).get("watiCreds")
        tenantId=obj.get("tenantId")
        watiAccessToken=obj.get("watiAccessToken")
        url = f"{tenantId}/api/v1/getContacts"
        print(url)
        headers = {
            'Authorization': f'Bearer {watiAccessToken}',
            'Content-Type': 'application/json'
        }
        # IN FUTURE HANDLE PAGE SIZE COMPLEXITY HANDLE
        response=requests.get(url, headers=headers)
        return True, response.json()
    except Exception as ex:
        return False,None


def getMessgae(token,phoneNumber):
    ndid=utils.get_ndid(token)
    obj=db.Zucks_profile.find_one({"uId":ndid}).get("watiCreds")
    tenantId=obj.get("tenantId")
    watiAccessToken=obj.get("watiAccessToken")
    url = f"{tenantId}/api/v1/getMessages/{phoneNumber}"
    print(url)
    headers = {
        'Authorization': f'Bearer {watiAccessToken}',
        'Content-Type': 'application/json'
    }
    # IN FUTURE HANDLE PAGE SIZE COMPLEXITY HANDLE
    response=requests.get(url, headers=headers)
    return True, response.json()


def sendSessionMessage(token, phoneNumber, messageText):
    try:
        ndid = utils.get_ndid(token)
        obj = db.Zucks_profile.find_one({"uId": ndid}).get("watiCreds")
        tenantId = obj.get("tenantId")
        watiAccessToken = obj.get("watiAccessToken")
        url = f"{tenantId}/api/v1/sendSessionMessage/{phoneNumber}"
        print(url)
        headers = {
            'Authorization': f'Bearer {watiAccessToken}',
        }
        data = {
            'messageText': messageText
        }
        response = requests.post(url, headers=headers, data=data)
        data=response.json()
        print(data)
        if data.get("result")=="success":
            return True
        return False
    except Exception as ex:
        return False


def updateParams(token,data):
    try:
        ndid = utils.get_ndid(token)
        obj = db.Zucks_profile.find_one({"uId": ndid}).get("watiCreds")
        tenantId = obj.get("tenantId")
        watiAccessToken = obj.get("watiAccessToken")
        phoneNumber=data.get("phoneNumber")
        url = f"{tenantId}/api/v1/updateContactAttributes/{phoneNumber}"
        print(url)
        headers = {
            'Authorization': f'Bearer {watiAccessToken}',
        }
        customParams = {
            'customParams': data.get("customParams")
        }
        response = requests.post(url, headers=headers, json=customParams)
        data=response.json()
        print(data)
        if data.get("result")==True:
            return True
        return False
    except Exception as ex:
        return False
    
def addContact(token,data):
    try:
        ndid = utils.get_ndid(token)
        obj = db.Zucks_profile.find_one({"uId": ndid}).get("watiCreds")
        tenantId = obj.get("tenantId")
        watiAccessToken = obj.get("watiAccessToken")
        phoneNumber=data.get("phoneNumber")
        url = f"{tenantId}/api/v1/addContact/{phoneNumber}"
        headers = {
            'Authorization': f'Bearer {watiAccessToken}',
        }
        data={
            "customParams": data.get("customParams"),
            "name": data.get("name"),
        }
        response = requests.post(url, headers=headers, json=data)
        res=response.json()
        if(res.get("result")==True):
            return True
        return False
    except Exception as ex:
        return False

def getTemplateMessage(token):
    ndid = utils.get_ndid(token)
    obj = db.Zucks_profile.find_one({"uId": ndid}).get("watiCreds")
    tenantId = obj.get("tenantId")
    watiAccessToken = obj.get("watiAccessToken")
    url = f"{tenantId}/api/v1/getMessageTemplates"
    headers = {
        'Authorization': f'Bearer {watiAccessToken}',
    }
    response = requests.get(url, headers=headers)
    response=response.json()
    if response.get("result")=="success":
        return True,response.get("messageTemplates")
    return False,None


def sendTemplateMessage(token,phoneNumber,data):
    print(token)
    ndid = utils.get_ndid(token)
    print(ndid)
    obj = db.Zucks_profile.find_one({"uId": ndid}).get("watiCreds")
    tenantId = obj.get("tenantId")
    watiAccessToken = obj.get("watiAccessToken")
    url = f"{tenantId}/api/v1/sendTemplateMessage?whatsappNumber={phoneNumber}"
    print(url)
    headers = {
        'Authorization': f'Bearer {watiAccessToken}',
    }
    response = requests.post(url, headers=headers,json=data)
    response=response.json()
    if response.get("result")==True:
        return True
    return False