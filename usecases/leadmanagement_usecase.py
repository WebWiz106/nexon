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
import base64

import random
from datetime import datetime, date, timedelta
from usecases import room_usecase
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db

def addSheetname(data):
    try:
        ndid = utils.get_ndid(data.get("token"))
        hId = data.get("hId")
        spreadSheetName = data.get("spreadSheetName")
        spreadSheetId = data.get("spreadSheetId")
        dataifpresent = db.LeadManagement.find_one({"ndid": ndid, "hId": hId})
        
        if dataifpresent:
            for val in dataifpresent.get("spreadSheet"):
                if val.get("Name") == spreadSheetName:
                    return False, "SpreadSheet with this Name Already Exists"
                
            db.LeadManagement.find_one_and_update(
                {"ndid": ndid, "hId": hId},
                { "$push": { "spreadSheet": { "Name": spreadSheetName, "id": spreadSheetId } } }
            )
            return True,"Added SuccessFully"
        else:
            obj={
                "hId":hId,
                "ndid":ndid,
                "googleToken":"None",
                "spreadSheet":[{"Name":spreadSheetName,"id":spreadSheetId}],
            }
            db.LeadManagement.insert_one(obj)
        
        return True,"Added SuccessFully"
    except Exception as ex:
        return False


def getSheet(token):
    try:
        print(1)
        ndid=utils.get_ndid(token)
        print(2,ndid)
        data=db.LeadManagement.find_one({"ndid":ndid}).get("spreadSheet")
        print(data)
        return True,data
    except Exception as ex:
        return False,"Some problem occured while fetching"
    

def updateGoogleToken(google,token):
    try:
        ndid=utils.get_ndid(token)
        db.LeadManagement.find_one_and_update({"ndid":ndid},{"$set":{"googleToken":google}})
        return True,"Google token updated successfylly"
    except Exception as ex:
        return False,"Some Error Occured while updating google token"
    

def getSheetDetailsforlead(sheetId,sheetName,token):
    try:
        ndid=utils.get_ndid(token)
        alldata=db.LeadManagement.find_one({"ndid":ndid})
        # print(alldata)
        data=alldata.get("spreadSheet")
        gtoken=alldata.get("googleToken")
        match=False
        for obj in data:
            if obj.get("id")==sheetId:
                match=True

        if match==False:
            return False,"None"
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/{sheetName}"
        headers = {
            'Authorization': f'Bearer {gtoken}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        print(response)
        if response.status_code == 200:
            data = response.json()
            arr=data["values"]
            max_length = max(len(sublist) for sublist in arr)
            
            # Pad each internal list with zeros to make them all of equal length
            padded_array = [sublist + [''] * (max_length - len(sublist)) for sublist in arr]
            
            # row=(len(padded_array))
            # col=len(padded_array[0])
            # print(row,col)
            # newarr=[""]
            # addcol=0
            # for char in string.ascii_uppercase:
            #     addcol+=1
            #     newarr.append(char)
            # mul=24
            # while len(newarr)<=col:
            #     i=len(newarr)-1
            #     tobeadd=newarr[-mul:]
            #     for char in string.ascii_uppercase:
            #         if len(newarr)<=mul:
            #             for val in tobeadd:
            #                 if len(newarr)<=mul:
            #                     newarr.append(char+""+val)
            #                     addcol+=1
            #                 else:
            #                     break
            #         else:
            #             break
            #     mul*=26
            # newans=[]
            # newans.append(newarr)
            # i=1
            # for val in padded_array:
            #     val.insert(0,i)
            #     i+=1
            #     newans.append(val)
            # max_length = max(len(sublist) for sublist in newans)
            
            # # Pad each internal list with zeros to make them all of equal length
            # padded_array = [sublist + [''] * (max_length - len(sublist)) for sublist in newans]
            
            # print(padded_array)
            data["values"]=padded_array
            data["Status"]=True
            return True,data
        else:
            # db.LeadManagement.find_one_and_update({"ndid":ndid},{"$set":{"googleToken":"None"}})
            print(f"Failed to fetch sheet names. Status code: {response.status_code}")
            return False,"None"
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False,"None"



def getAllSheetName(spreadSheetId,token):
    ndid=utils.get_ndid(token)
    googleToken=db.LeadManagement.find_one({"ndid":ndid}).get("googleToken")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadSheetId}?fields=sheets(properties/title)"
    headers = {
        'Authorization': f'Bearer {googleToken}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            data["Status"]=True
            return True,data
        else:
            # db.LeadManagement.find_one_and_update({"ndid":ndid},{"$set":{"googleToken":"None"}})
            print(f"Failed to fetch sheet names. Status code: {response.status_code}")
            return False,"None"
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False,"None"



def getGoogleToken(token):
    try:
        ndid=utils.get_ndid(token)
        gtoken=db.LeadManagement.find_one({"ndid":ndid}).get("googleToken")
        if gtoken=="None":
            return False,"None"
        return True,gtoken
    except Exception as ex:
        return False,"None"
    

def updateSheetUsecase(token,sheetId,sheetName,data):
    try:
        print(2)
        rowstart=data.get("rowstart")
        rowend=data.get("rowend")
        colstart=data.get("colstart")
        colend=data.get("colend")
        value=data.get("values")
        ndid=utils.get_ndid(token)
        range=sheetName+"!"+colstart+rowstart+":"+colend+rowend
        gtoken=db.LeadManagement.find_one({"ndid":ndid}).get("googleToken")
        url=f"https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/{range}?valueInputOption=USER_ENTERED"

        headers = {
            'Authorization': f'Bearer {gtoken}',
            'Content-Type': 'application/json'
        }
        body={
            "range":range,
            "majorDimension": "ROWS",
            "values":data.get("values")
        }
        response = requests.put(url, headers=headers,json=body)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to fetch sheet names. Status code: {response.status_code}")
            return False
    except Exception as ex:
        return False