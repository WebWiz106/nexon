import pymongo
import json
import settings
import constants
import utils
from model.bookings import Bookings
import requests

from datetime import datetime, date, timedelta
from usecases import room_usecase, mail_usecase,booking_usecase
from model.booking_item import BookingItem
from model.guest_info import GuestInfo
import logging
import re

from utils import db

def get_number(token):
    try:
        data = utils.Decode_jwt(token)
        return data["Number"]
    
    except Exception as ex:
        return "None"


def sendOtpTONumber(phoneNumber):
    CLIENT_ID="EVBO79V64Q7SN7HUYHAGN6HJFFT0M9X1"
    CLIENT_SECRET="ntlg56xcz8vnkqjammnahezu72fgj3ha"
    headers = {
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "Content-Type": "application/json"
    }
    reqdata={
        "phoneNumber":"91"+str(phoneNumber),
        "otpLength": 6,
        "channel":"SMS",
        "expiry": 60
    }
    # Make the API request
    response = requests.post('https://auth.otpless.app/auth/otp/v1/send', headers=headers, json=reqdata)
    if response.status_code == 200:
            order_id=response.json()
            orderid =order_id.get("orderId")
            return orderid
    else:
        print("Error:", response.status_code)


def verifyOtpToNumber(phoneNumber,orderid,otp):
    CLIENT_ID="EVBO79V64Q7SN7HUYHAGN6HJFFT0M9X1"
    CLIENT_SECRET="ntlg56xcz8vnkqjammnahezu72fgj3ha"
    headers = {
                "clientId": CLIENT_ID,
                "clientSecret": CLIENT_SECRET,
                "Content-Type": "application/json"
            }
    reqdata={
        "orderId":orderid,
        "otp":otp,
        "phoneNumber":str(91)+str(phoneNumber)
    }
    response = requests.post('https://auth.otpless.app/auth/otp/v1/verify', headers=headers, json=reqdata)
    
    if response.status_code == 200:
        return True
    else:
        return False


def Check_User_Engine_Login(ndid,hId,token):
    try:
        number = get_number(token)

        if(number=="None"):
            return False
        else:

            user = db.Engine_Users.find_one({"ndid":ndid,"hId":hId,"Number":number})
            if user:
                return True
            else:
                return False
    except:
        return False


def register_User_Engine_Login(data):
    try:
        ndid = data.get("ndid")
        hotelid = data.get("hotelid")
        name = data.get("Name")
        phone = data.get("phone")
        email = data.get("emailId")

        user_exists = db.Engine_Users.find_one({"ndid":ndid,"hId":hotelid,"Number":phone})
        if user_exists:
            return False, "User Exists with this phone number. Please Login"
        else:
            orderid = sendOtpTONumber(phone)
            db.Engine_Users.insert_one({
                "ndid":ndid,
                "hId":hotelid,
                "Name":name,
                "Number":phone,
                "Email":email,
                "orderId":orderid,
                "verified":False
                })
            
            return True, "User Created successfully"

    except:
        return False, "Some Problem occured"
    

def login_User_Engine_Login(data):
    try:
        ndid = data.get("ndid")
        hotelid = data.get("hotelid")
        name = data.get("Name")
        phone = data.get("phone")
        email = data.get("emailId")

        user_exists = db.Engine_Users.find_one({"ndid":ndid,"hId":hotelid,"Number":phone})
        if user_exists:
            orderid = sendOtpTONumber(phone)
            db.Engine_Users.find_one_and_update({"ndid":ndid,"hId":hotelid,"Number":phone},{"$set":{
                "orderId":orderid
            }})
            return True, "Otp sent to user to login"
        else:
            return False, "No user registered with same phone number"

    except:
        return False, "Some Problem occured"
    

def checkotp_User_Engine_Login(data):
    try:
        ndid = data.get("ndid")
        hId = data.get("hotelid")
        phone = data.get("phone")
        otp = data.get("otp")

        userexists = db.Engine_Users.find_one({"ndid":ndid,"hId":hId,"Number":phone})

        orderid = userexists.get("orderId")

        verified = verifyOtpToNumber(phone,orderid,otp)

        db.Engine_Users.find_one_and_update({"ndid":ndid,"hId":hId,"Number":phone},{"$set":{
            "verified":True
        }})

        data = {
                    "Number":phone
                }
        token = utils.create(data)

        return True,token
    
    except:
        return False,"-"
    
def getPrevBookings(ndid, hId, token):
    number = get_number(token)
    current_date = datetime.now().strftime("%Y-%m-%d")    
    escaped_number = re.escape(number)
    regex_pattern = f"{escaped_number}$"

    # Use the regex pattern in the query
    data = list(db.Bookings.find({
        "guestInfo.Phone": {"$regex": regex_pattern},
        "ndid": ndid,
        "hId": hId,
        "checkIn": {"$lte": current_date}
    }, {"_id": 0}))
    return data

def getFutureBooking(ndid, hId, token):
    number = get_number(token)
    current_date = datetime.now().strftime("%Y-%m-%d")  
    escaped_number = re.escape(number)
    regex_pattern = f"{escaped_number}$"

    data = list(db.Bookings.find({
        "guestInfo.Phone": {"$regex": regex_pattern},
        "ndid": ndid,
        "hId": hId,
        "checkIn": {"$gte": current_date}
    }, {"_id": 0}))
    return data



def cancelBookingByUser(ndid,hId,token,bookingid):
    try:
        phoneNumber=get_number(token)
        booking_exist = Bookings.from_dict(db.Bookings.find_one(
            {"ndid": ndid, "bookingId": bookingid, "hId": hId}))
        booking_exist.payment.status = "CANCELLED"
        db.Bookings.find_one_and_update({"ndid": ndid, "bookingId": bookingid, "hId": hId}, {
                                        "$set": Bookings.to_dict(booking_exist)})
        booking = Bookings.from_dict(db.Bookings.find_one(
            {"ndid": ndid, "hId": hId, "bookingId": bookingid}))
        # update
        checkindate = booking.checkIn
        checkoutdate = booking.checkOut
        bookings = []
        for ele in booking.bookingItems:
            bookings.append(BookingItem.to_dict(ele))
        # update Inventory
        print(bookings)
        booking_usecase.room_Number_deallocation(hId,ndid,bookingid)
        booking_usecase.updateInventory_increase(
            checkindate, checkoutdate, bookings, ndid, hId)
        logging.info(f"True")
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)


def getUserByPhoneNo(token):
    phNo=get_number(token)
    user=db.Engine_Users.find_one({"Number":phNo},{"_id":0})
    return user