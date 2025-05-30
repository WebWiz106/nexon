import utils
import hashlib
import pymongo
import settings
import logging
import json
import io
import base64
import boto3
import uuid
import copy
import razorpay
from datetime import datetime
import zipfile
import os
import uuid
from PIL import Image
import subprocess
import shortuuid
import time
from datetime import datetime, date, timedelta
from bson import json_util
from datetime import datetime
from model.user import User
import requests
from usecases import mail_usecase

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

# client = pymongo.MongoClient(settings.DBURL)
client = pymongo.MongoClient(
    "mongodb+srv://eazotel:admin@cluster0.p0kewzl.mongodb.net/"
)
print("===========================Database============================")
db = client["Gian"]


def get_number(token):
    try:
        data = utils.Decode_jwt(token)
        return data["Number"]

    except Exception as ex:
        raise ValueError("Unable to decode token error : {}", ex)


# ===================


def getEndUserDetailsfromNumber(number):
    try:
        endusercheck = db.SigninUser.find_one({"phoneNumber": number})
        if endusercheck == None:
            endcheckadmin = db.Users.find_one({"phone": number})
            if endcheckadmin == None:
                return False
            else:
                return True
        else:
            return True
    except Exception as ex:
        return False


def getEndUserfromDatabase(token):
    try:
        number = get_number(token)
        endusercheck = db.SigninUser.find_one({"phoneNumber": number})
        if endusercheck == None:
            endcheckadmin = db.Users.find_one({"phone": number})
            if endcheckadmin == None:
                return False, False
            else:
                return True, True
        else:
            return True, False
    except Exception as ex:
        return False, False


def addEndUserToDatabase(data):
    try:
        phoneNumber = data.get("number")
        # CLIENT_ID = "EVBO79V64Q7SN7HUYHAGN6HJFFT0M9X1"
        # CLIENT_SECRET = "ntlg56xcz8vnkqjammnahezu72fgj3ha"

        # for alhathifa
        CLIENT_ID = "1JPSZCP356AYDRQSYI0Z8GA856U60XZX"
        CLIENT_SECRET = "xvysvvmyz2bodl7mne7o8nfq1p6inluy"
        headers = {
            "clientId": CLIENT_ID,
            "clientSecret": CLIENT_SECRET,
            "Content-Type": "application/json",
        }
        print("91" + str(data.get("number")))
        reqdata = {
            "phoneNumber": "91" + str(data.get("number")),
            "otpLength": 6,
            "channel": "SMS",
            "expiry": 60,
        }
        # Make the API request
        response = requests.post(
            "https://auth.otpless.app/auth/otp/v1/send", headers=headers, json=reqdata
        )
        if response.status_code == 200:
            order_id = response.json()
            orderid = order_id.get("orderId")
            print(orderid)
            enduser = db.SigninUser.find_one({"phoneNumber": phoneNumber})
            if enduser == None:
                checkadmin = db.Users.find_one({"phone": phoneNumber})
                if checkadmin == None:
                    db.SigninUser.insert_one(
                        {
                            "phoneNumber": phoneNumber,
                            "orderId": orderid,
                            "isAuth": False,
                            "Name": data.get("Name"),
                            "Email": data.get("Email"),
                        }
                    )
                else:
                    db.Users.find_one_and_update(
                        {"phone": phoneNumber}, {"$set": {"orderId": orderid}}
                    )
            else:
                db.SigninUser.find_one_and_update(
                    {"phoneNumber": phoneNumber},
                    {"$set": {"orderId": orderid, "isAuth": False}},
                )

            return True
        else:
            print("Error:", response.status_code)
            print(response.text)
            return None
    except Exception as ex:
        return None


def blockTurf(data, token):
    try:
        seid = get_seid(token)
        obj = (
            db.Sports.find_one({"seid": seid, "sportName": data.get("sportName")})
            .get("blockedTurfs")
            .get(data.get("date"))
        )
        if obj is None:
            obj = {}
        if data.get("slotName") not in obj:
            obj[data.get("slotName")] = {}
        obj[data.get("slotName")] = data.get("turfs")
        db.Sports.find_one_and_update(
            {"seid": seid, "sportName": data.get("sportName")},
            {"$set": {"blockedTurfs." + data.get("date"): obj}},
        )
        return True
    except Exception as ex:
        return False


def getAllBlockedTurfs(token, sportName):
    try:
        seid = get_seid(token)
        return True, db.Sports.find_one({"seid": seid, "sportName": sportName}).get(
            "blockedTurfs"
        )
    except Exception as ex:
        return False


def updateEndUserToDatabase(data):
    try:
        # CLIENT_ID = "EVBO79V64Q7SN7HUYHAGN6HJFFT0M9X1"
        # CLIENT_SECRET = "ntlg56xcz8vnkqjammnahezu72fgj3ha"

        # for alhathaifa

        CLIENT_ID = "1JPSZCP356AYDRQSYI0Z8GA856U60XZX"
        CLIENT_SECRET = "xvysvvmyz2bodl7mne7o8nfq1p6inluy"
        phoneNumber = data.get("number")
        otp = data.get("otp")
        enduser = db.SigninUser.find_one({"phoneNumber": phoneNumber})
        if enduser == None:
            checkenduseradmin = db.Users.find_one({"phone": phoneNumber})
            if checkenduseradmin == None:
                return False, "-"
            else:
                data = {"Number": phoneNumber}
                token = utils.create(data)

                return True, token
        else:
            orderId = enduser.get("orderId")
            headers = {
                "clientId": CLIENT_ID,
                "clientSecret": CLIENT_SECRET,
                "Content-Type": "application/json",
            }
            reqdata = {
                "orderId": orderId,
                "otp": otp,
                "phoneNumber": str(91) + str(phoneNumber),
            }
            response = requests.post(
                "https://auth.otpless.app/auth/otp/v1/verify",
                headers=headers,
                json=reqdata,
            )

            if response.status_code == 200:
                db.SigninUser.find_one_and_update(
                    {"phoneNumber": phoneNumber}, {"$set": {"isAuth": True}}
                )
                data = {"Number": phoneNumber}
                token = utils.create(data)

                return True, token
            else:
                return False, "-"
    except Exception as ex:
        return False, "-"


def getProfileofUser(seid):
    try:
        userProfile = db.Profiles.find_one({"seid": seid})
        return userProfile
    except Exception as ex:
        return None


# ✅


def get_email(token):
    try:
        data = utils.Decode_jwt(token)
        return data["Email"]
    except Exception as ex:
        raise ValueError("Unable to decode token error : {}", ex)


# ✅
def get_seid(token):
    try:
        data = utils.Decode_jwt(token)
        user = db.Users.find_one({"Email": data["Email"]})
        ndid = user.get("seid")
        return ndid
    except Exception as ex:
        raise ValueError("Unable to decode token error : {}", ex)
        return None


# ✅
def getProfileUser(id):
    try:
        profiles = db.Profiles.find_one({"seid": id})
        return profiles
    except Exception as ex:
        return None


# ✅
def addProfile(data):
    try:
        seid = str(uuid.uuid4())
        check = db.Profiles.find_one({"email": data.get("email")})
        check1 = db.Users.find_one({"email": data.get("email")})
        if check != None or check1 != None:
            return False, "Name Already Exists", "-"

        password = hashlib.sha256(data.get("Passkey").encode("utf-8")).hexdigest()

        db.Users.insert_one(
            {
                "seid": seid,
                "UserName": data.get("UserName"),
                "Email": data.get("email"),
                "passKey": password,
                "accessScope": {},
                "isAdmin": True,
            }
        )
        db.Profiles.insert_one(
            {
                "seid": seid,
                "name": data.get("hotelName"),
                "email": data.get("email"),
                "gateWay": {"Type": "", "API_KEY": "", "SECRET_KEY": ""},
                "watiCreds": {"tenantId": "", "watiAccessToken": ""},
                "Locations": {},
                "dinabiteToken": {"access_token": "None"},
                "isVerified": False,
                "isActive": False,
            }
        )

        db.WebsiteData.insert_one(
            {
                "seid": seid,
                "Details": {
                    "SocialLinks": {
                        "Instagram": "None",
                        "Facebook": "None",
                        "Tinder": "None",
                        "Tripadvisors": "None",
                        "Linkedin": "None",
                        "Youtube": "None",
                    },
                    "Footer": {
                        "Logo": "None",
                        "Whatsapp": "",
                        "Phone": "",
                        "Address": "",
                        "City": "",
                        "Country": "",
                        "Abouttext": "",
                    },
                },
            }
        )

        data = {"Email": data.get("email")}

        token = utils.create(data)
        return True, "Profile Created Successfully", token
    except Exception as ex:
        return False, "-", None


# ✅
def LoginProfile(data):
    try:
        password = hashlib.sha256(data.get("passKey").encode("utf-8")).hexdigest()
        check = db.Users.find_one({"Email": data.get("email"), "passKey": password})
        if check == None:
            return False, "Login Failed", "-", "None", "None"

        check1 = db.Profiles.find_one({"seid": check.get("seid")})
        if check1 == None:
            return False, "Login Failed", "-", "None", "None"

        data = {"Email": data.get("email")}
        token = utils.create(data)

        return True, "Profile Login Successfully", token, check1, check
    except Exception as ex:
        return False, "-"


def LoginProfileWithDashboard(token):
    try:
        number = get_number(token)
        check = db.Users.find_one({"phone": number})
        if check == None:
            return False, "Login Failed", "-", "None", "None"

        check1 = db.Profiles.find_one({"seid": check.get("seid")})
        if check1 == None:
            return False, "Login Failed", "-", "None", "None"

        data = {"Email": check.get("Email")}
        token = utils.create(data)

        return True, "Profile Login Successfully", token, check1, check
    except Exception as ex:
        return True, "-", None, None, None


# ✅
def UpdateProfilePassword(data):
    try:
        email = data.get("emailid")
        passkey = data.get("passkey")
        newpasskey = data.get("newpasskey")

        password = hashlib.sha256(passkey.encode("utf-8")).hexdigest()
        passwordnew = hashlib.sha256(newpasskey.encode("utf-8")).hexdigest()

        check = db.Users.find_one({"Email": email, "passKey": password})
        if check == None:
            return False, "You Have Given Wrong Password"
        else:
            db.Users.find_one_and_update(
                {"Email": email}, {"$set": {"passKey": passwordnew}}
            )
            return True, "Password Changes Successfully"
    except Exception as ex:
        return False, "-"


# ✅
def allUsersDashboard(token):
    try:
        seid = get_seid(token)
        users = db.Users.find({"seid": seid})

        allusers = []
        for user in users:
            user["_id"] = str(user["_id"])
            allusers.append(user)

        return True, allusers
    except Exception as ex:
        return False, None


# ✅
def addProfileDashboard(data, token):
    try:
        seid = get_seid(token)
        adminmail = get_email(token)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        usercheck = db.Users.find_one({"Email": email})
        usercheckphone = db.Users.find_one({"phone": data.get("phone")})
        if usercheck != None or usercheckphone != None:
            return False, "Email or phone Already Exists"

        user = db.Users.find_one({"seid": seid, "Email": adminmail})

        if user.get("isAdmin"):
            check1 = db.Users.insert_one(
                {
                    "seid": seid,
                    "UserName": username,
                    "Email": email,
                    "passKey": password,
                    "accessScope": {},
                    "isAdmin": False,
                    "phone": data.get("phone"),
                }
            )
            return True, "User Added"
        else:
            return False, "User Not have permission"
    except Exception as ex:
        return False, "User not have permission"


# ✅
def deleteProfileDashboard(data, token):
    try:
        seid = get_seid(token)
        email = get_email(token)

        user = db.Users.find_one({"seid": seid, "Email": email})
        if user.get("isAdmin"):
            user1 = db.Users.find_one({"Email": data.get("email")})
            if user1.get("isAdmin"):
                return True, "Admin can not be deleted"
            else:
                user = db.Users.find_one_and_delete({"Email": data.get("email")})
                return True, "Deleted Successfully"
        else:
            return False, "User don't have permissions to delete"
    except Exception as ex:
        return False, None


# ✅
def addSport(data, token):
    try:
        seid = get_seid(token)
        print(seid)
        if seid == None:
            return False
        print(1)
        data["seid"] = seid
        # Check if already exist
        alreadyexists = db.Sports.find_one(
            {"seid": seid, "sportName": data.get("sportName")}
        )
        print(2)
        if alreadyexists:
            return False
        print(3)
        data["sportId"] = shortuuid.uuid()
        data["blockedSlots"] = []
        data["customPrice"] = {}
        data["blockedTurfs"] = {}
        db.Sports.insert_one(data)
        return True
    except Exception as ex:
        return False


# ✅
def get_id(booking_count):

    try:
        logging.info(f"{booking_count}")
        for i in range(5 - len(booking_count)):
            booking_count = "0" + booking_count
        logging.info(f"{booking_count}")
        return booking_count
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


# ✅
def get_booking_id():
    try:
        query = {
            "createdAt": {
                "$gte": str(date.today()) + " 00:00",
                "$lte": str(date.today()) + " 23:59",
            }
        }
        booking_count = str(db.SportsBooking.count_documents(query) + 1)
        print(booking_count)
        logging.info(f"{booking_count}")
        return "B" + date.today().strftime("%Y%m%d") + get_id(booking_count)
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


# ✅
def createBooking(data):
    try:
        token = data.get("Token")
        number = get_number(token)
        userofnumber = db.SigninUser.find_one({"phoneNumber": number})

        if userofnumber == None:
            userofnumber1 = db.Users.find_one({"phone": number})
            if userofnumber1 == None:
                return False, None
            else:
                data["guestInfo"] = {
                    "Name": userofnumber1.get("UserName"),
                    "Phone": userofnumber1.get("phone"),
                    "Email": userofnumber1.get("Email"),
                }

        else:
            data["guestInfo"] = {
                "Name": userofnumber.get("Name"),
                "Phone": userofnumber.get("phoneNumber"),
                "Email": userofnumber.get("Email"),
            }
        gateWay = db.Profiles.find_one({"seid": data.get("seid")}).get("gateWay")
        apikey = gateWay.get("API_KEY")
        secretkey = gateWay.get("SECRET_KEY")
        razorpay_client = razorpay.Client(auth=(apikey, secretkey))
        order = razorpay_client.order.create(
            {
                "amount": float(data.get("price").get("amountPaid")) * 100,
                "currency": "INR",
                "receipt": "order_receipt_123",  # You can generate a unique receipt for each order
            }
        )
        data["sportBookingId"] = get_booking_id()
        data["isCheckedIn"] = False
        data["isCheckedOut"] = False
        data["payment"] = {
            "RefNo": str(order["id"]),
            "PaymentProvider": "",
            "Mode": "",
            "Status": "PENDING",
            "payId": "",
        }
        data.pop("Token")
        data["createdAt"] = str(datetime.now())
        status, _dict = CounterValue(
            {
                "seid": data.get("seid"),
                "sportId": data.get("sportId"),
                "date": data.get("bookingDate"),
            }
        )
        arr = []
        intitialobj = data.get("bookedSlots")[0]
        arr.append(intitialobj)
        incre = 1
        for i in range(int(data.get("duration")) - 1):
            slott = intitialobj.get("slotName")[0:4]
            lastslotnum = int(intitialobj.get("slotName")[4:])
            slotname = str(slott) + str(lastslotnum + incre)
            slotstart = (
                str(int(intitialobj.get("slotstart").split(":")[0]) + incre)
                + ":"
                + intitialobj.get("slotstart").split(":")[1]
            )
            slotend = (
                str(int(intitialobj.get("slotEnd").split(":")[0]) + incre)
                + ":"
                + intitialobj.get("slotEnd").split(":")[1]
            )
            arr.append(
                {
                    "slotName": slotname,
                    "slotstart": slotstart,
                    "slotEnd": slotend,
                    "turfName": intitialobj.get("turfName"),
                    "turfPrice": _dict[slotname][intitialobj.get("turfName")],
                }
            )
            incre += 1
        data["bookedSlots"] = arr
        db.SportsBooking.insert_one(data)
        return True, order["id"]
    except Exception as ex:
        return False, None


def getForDateAndSport(date, sports):
    try:
        sportsdb = db.Sports.find_one({"sportName": sports})
        data = {}
        for slot in sportsdb.get("slots"):
            print(slot)
            data[slot] = sportsdb.get("slots").get(slot)
            data[slot]["turf"] = {}
            for trf in sportsdb.get("turfs"):
                data[slot]["turf"][trf] = True

        sportbookings = db.SportsBooking.find({"Date": date, "Sport": sports})
        for eachBooking in sportbookings:
            for eachSlot in eachBooking.get("bookedSlots"):
                if (
                    eachSlot.get("slot") in data
                    and eachSlot.get("turf") in data[eachSlot.get("slot")]["turf"]
                ):
                    data[eachSlot.get("slot")]["turf"][eachSlot.get("turf")] = False
        return data
    except Exception as ex:
        return None


# --------------------------- DASHBOARD APIS ---------------------------#
def updateBookingDashBoardDashboard(token, data):
    try:
        seid = get_seid(token)
        db.SportsBooking.find_one_and_update(
            {
                "sportBookingId": data.get("sportBookingId"),
                "sportId": data.get("sportId"),
                "seid": seid,
            },
            {
                "$set": {
                    "bookingDate": data.get("bookingDate"),
                    "bookedSlots": data.get("bookedSlots"),
                    "payment": data.get("payment"),
                }
            },
            return_document=True,  # Assuming you want the updated document back; use pymongo.ReturnDocument.AFTER if needed
        )
        return True
    except Exception as ex:
        print(f"An error occurred: {ex}")
        return False


def changeStatusBookingId(token, sportBookingId, data):
    try:
        seid = get_seid(token)
        db.SportsBooking.find_one_and_update(
            {"sportBookingId": sportBookingId, "seid": seid},
            {
                "$set": {
                    "isCheckedIn": True if data.get("isCheckedIn") == "true" else False,
                    "isCheckedOut": (
                        True if data.get("isCheckedOut") == "true" else False
                    ),
                }
            },
        )
        return True
    except Exception as ex:
        return False


def getSportForDashboard(token):
    try:
        seid = get_seid(token)
        data = db.Sports.find({"seid": seid})

        # Convert cursor to list of dictionaries and remove _id field
        sports_data = []
        for document in data:
            document.pop("_id", None)
            sports_data.append(document)

        return sports_data

    except Exception as ex:
        print(f"Exception in getSportForDashboard: {ex}")
        return None


def deleteSport(token, sportId):
    try:
        seid = get_seid(token)
        db.Sports.find_one_and_delete({"seid": seid, "sportId": sportId})
        return True
    except Exception as ex:
        return False


def updateSportDashboard(data, token, sportId):
    try:
        seid = get_seid(token)
        update_document = {
            "$set": {
                "sportName": data.get("sportName"),
                "images": data.get("images"),
                "slots": data.get("slots"),
                "turfs": data.get("turfs"),
            }
        }

        result = db.Sports.find_one_and_update(
            {"seid": seid, "sportId": sportId}, update_document, return_document=True
        )

        if result is None:
            return False

        return True

    except Exception as ex:
        return False


def updateSlotsForDateDashBoard(data, token, sportName):
    try:
        seid = get_seid(token)
        sports_document = db.Sports.find_one({"seid": seid, "sportName": sportName})
        if not sports_document:
            return False
        slotname = ""
        slots = sports_document.get("slots")
        for val in slots:
            if slots.get(val).get("start") == data.get("start") and slots.get(val).get(
                "end"
            ) == data.get("end"):
                slotname = val

        if slotname == "":
            return False
        blockedSlots = sports_document.get("blockedSlots", [])
        pres = False
        for val in blockedSlots:
            if val.get("date") == data.get("date"):
                pres = True
                val["blockedSlots"][slotname] = data.get("value")
        if pres == False:
            obj = {slotname: data.get("value")}
            blockedSlots.append({"date": data.get("date"), "blockedSlots": obj})
        db.Sports.find_one_and_update(
            {"seid": seid, "sportName": sportName},
            {"$set": {"blockedSlots": blockedSlots}},
        )

        return True

    except Exception as ex:
        print(f"Exception in updateSlotsForDateDashBoard: {ex}")
        return False


# ✅
def getAllBookingDashBoard(token, date=None):
    try:
        seid = get_seid(token)
        query = {"seid": seid}
        if date:
            query["bookingDate"] = date
        cursor = db.SportsBooking.find(query, {"_id": 0})
        bookings = list(cursor)
        return bookings
    except Exception as ex:
        print(f"An error occurred: {ex}")
        return None


# ✅
def updateBookingDashBoard(data):
    try:
        db.SportsBooking.find_one_and_update(
            {
                "sportBookingId": data.get("sportBookingId"),
                "sportId": data.get("sportId"),
            },
            {
                "$set": {
                    "bookingDate": data.get("bookingDate"),
                    "bookedSlots": data.get("bookedSlots"),
                    "payment": data.get("payment"),
                }
            },
            return_document=True,  # Assuming you want the updated document back; use pymongo.ReturnDocument.AFTER if needed
        )
        return True
    except Exception as ex:
        print(f"An error occurred: {ex}")
        return False


def updateBookingRazorpay(data):
    try:
        booking = db.SportsBooking.find_one(
            {"payment.RefNo": data.get("orderId"), "sportId": data.get("sportId")}
        )
        db.SportsBooking.find_one_and_update(
            {"payment.RefNo": data.get("orderId"), "sportId": data.get("sportId")},
            {
                "$set": {
                    "payment.PaymentProvider": "Razorpay",
                    "payment.Mode": "Online",
                    "payment.Status": (
                        "SUCCESS"
                        if booking.get("price").get("amountPaid")
                        == booking.get("price").get("totalAmount")
                        else "ADVANCED"
                    ),
                    "payment.payId": data.get("payid"),
                }
            },
            return_document=True,  # Assuming you want the updated document back; use pymongo.ReturnDocument.AFTER if needed
        )

        data = db.SportsBooking.find_one(
            {"payment.RefNo": data.get("orderId"), "sportId": data.get("sportId")}
        )
        loneprofile = db.Profiles.find_one(
            {"seid": "779f43ea-5ed0-43ee-86fb-c7d296a769cf"}
        )

        # send mail confirmation to user
        mail_usecase.Send_Booking_confirmation_to_loneuser(
            data.get("sportBookingId"),
            data.get("guestInfo").get("Email"),
            loneprofile.get("email"),
            loneprofile.get("logo"),
            data.get("guestInfo").get("Name"),
            loneprofile.get("name"),
            data.get("bookingDate"),
            data.get("bookingDate"),
            data.get("price").get("totalAmount"),
            data.get("price").get("amountPaid"),
            data.get("guestInfo").get("Phone"),
            loneprofile.get("phone"),
            data,
        )

        # send mail confirmation to lonestar
        mail_usecase.Send_Booking_confirmation_to_loneadmin(
            data.get("sportBookingId"),
            loneprofile.get("email"),
            data.get("guestInfo").get("Email"),
            loneprofile.get("email"),
            loneprofile.get("logo"),
            data.get("guestInfo").get("Name"),
            loneprofile.get("name"),
            data.get("bookingDate"),
            data.get("bookingDate"),
            data.get("price").get("totalAmount"),
            data.get("price").get("amountPaid"),
            data.get("guestInfo").get("Phone"),
            loneprofile.get("phone"),
            data,
        )

        return True, data
    except Exception as ex:
        print(f"An error occurred: {ex}")
        return False, "-"


def deleteBookingDashBoard(data):
    try:
        sportBookingId = data.get("bookingId")
        db.SportsBooking.find_one_and_update(
            {"sportBookingId": sportBookingId},
            {
                "$set": {
                    "payment.Status": "CANCELLED",
                    "Message": "Booking Cancelled by Admin",
                }
            },
        )
        return True
    except Exception as ex:
        return False


# ✅
def getAllSlotsForDateDashBoard(seid, date):
    try:
        data = []
        sports = db.Sports.find({"seid": seid}, {"_id": 0})
        for sport in sports:
            isholiday = sport.get("holdiayDates").get(date, False)
            blockedSlots = sport.get("blockedSlots")
            turf_order = []
            for val in sport.get("turfs"):
                turf_order.append(val["name"])
            bookings = db.SportsBooking.find({"bookingDate": date, "seid": seid})
            slot_data = []

            store_data = {}
            for booking in bookings:
                if (
                    booking.get("payment").get("Status") == "SUCCESS"
                    or booking.get("payment").get("Status") == "ADVANCED"
                ):
                    for val in booking["bookedSlots"]:
                        if val["slotName"] in store_data:
                            store_data[val["slotName"]].append(val["turfName"])
                        else:
                            store_data[val["slotName"]] = []
                            store_data[val["slotName"]].append(val["turfName"])

            blockedTurfs = sport.get("blockedTurfs").get(date, {})
            for slot in sport["slots"]:
                turf_data = []
                maxpres = False
                smallcount = 0
                for turfs in sport["turfs"]:
                    if slot in store_data and turfs["name"] in store_data[slot]:
                        if turfs["name"] == turf_order[2]:
                            maxpres = True
                        else:
                            smallcount += 1
                    else:
                        turf_data.append(
                            {
                                "name": turfs["name"],
                                "price": (
                                    sport.get("customPrice")
                                    .get(date)
                                    .get(slot)
                                    .get(turfs["name"])
                                    if date in sport.get("customPrice")
                                    and slot in sport.get("customPrice").get(date)
                                    and turfs["name"]
                                    in sport.get("customPrice").get(date).get(slot)
                                    else turfs["price"]
                                ),
                            }
                        )
                if maxpres:
                    # If max one is pres then other turfs will not be there
                    turf_data.clear()
                if smallcount == 1:
                    # If any of the smaller turf is there then max one should not be there
                    popidx = -1
                    for index, val in enumerate(turf_data):
                        if val.get("name") == turf_order[2]:
                            popidx = index
                            break
                    turf_data.pop(popidx)
                elif smallcount == 2:
                    # If both smaller turf are booked then remove even the larger
                    turf_data.clear()

                for val in blockedSlots:
                    if val.get("date") == date:
                        if val.get("blockedSlots").get(slot, True) == False:
                            turf_data.clear()
                new_turf_data = []
                blockedturfslot = blockedTurfs.get(slot, [])
                for turf in turf_data:
                    if turf["name"] not in blockedturfslot:
                        new_turf_data.append(turf)

                if turf_order[2] in blockedturfslot:
                    new_turf_data.clear()
                elif (
                    turf_order[0] in blockedturfslot
                    and turf_order[1] in blockedturfslot
                ):
                    new_turf_data.clear()

                if len(new_turf_data) == 2:
                    idx = -1
                    for i, val in enumerate(new_turf_data):
                        if val.get("name") == turf_order[2]:
                            idx = i
                    if idx != -1:
                        new_turf_data.pop(idx)
                if isholiday:
                    new_turf_data.clear()
                slot_data.append(
                    {
                        "slotName": slot,
                        "slotEnd": sport["slots"][slot]["end"],
                        "slotStart": sport["slots"][slot]["start"],
                        "Turfs": new_turf_data,
                    }
                )
            data.append(
                {
                    "sportId": sport["sportId"],
                    "sportName": sport["sportName"],
                    "images": sport["images"],
                    "slotData": slot_data,
                }
            )

        return data
    except Exception as ex:
        return None


def holidayhandle(token, data):
    try:
        seid = get_seid(token)
        obj = db.Sports.find_one({"seid": seid}).get("holdiayDates")
        for dates in data:
            obj[dates] = data.get(dates)
            # db.Sports.update_many({"seid":seid},{"$set":{"holdiayDates":{dates:data.get(dates)}}})
        db.Sports.update_many({"seid": seid}, {"$set": {"holdiayDates": obj}})
        return True
    except Exception as ex:
        return False


def blockTurfs(data):
    try:
        token = data.get("Token")
        seid = get_seid(token)
        data["seid"] = seid
        data.pop("Token")
        arr = []
        intitialobj = data.get("blockedSlot")[0]
        arr.append(intitialobj)
        incre = 1
        slott = intitialobj.get("slotName")[0:4]
        lastslotnum = int(intitialobj.get("slotName")[4:])
        slotname = str(slott) + str(lastslotnum)
        for i in range(int(data.get("duration"))):
            obj = (
                db.Sports.find_one({"seid": seid})
                .get("blockedTurfs")
                .get(data.get("date"))
            )
            if obj is None:
                obj = {}
            if slotname not in obj:
                obj[slotname] = {}
            obj[slotname] = intitialobj.get("turfName")
            db.Sports.update_many(
                {"seid": seid}, {"$set": {"blockedTurfs." + data.get("date"): obj}}
            )
            slott = intitialobj.get("slotName")[0:4]
            lastslotnum = int(intitialobj.get("slotName")[4:])
            slotname = str(slott) + str(lastslotnum + incre)

            incre += 1
        data["blockedSlot"] = arr
        return True
    except Exception as ex:
        return False


# ✅
def getAllBookingMonthDashBoard(token):
    try:
        seid = get_seid(token)

        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        current_month_string = f"{current_year:04}-{current_month:02}"
        bookings = db.SportsBooking.find(
            {"seid": seid, "bookingDate": {"$regex": f"^{current_month_string}"}},
            {"_id": 0},
        )
        return list(bookings)
    except Exception as ex:
        return []


# ✅
def getAllBookingPaymentStatus(token, status):
    try:
        seid = get_seid(token)
        booking = db.SportsBooking.find(
            {"seid": seid, "payment.Status": status}, {"_id": 0}
        )
        return list(booking)
    except Exception as ex:
        return []


# ✅
def getAllBookingDateRange(token, data):
    try:
        seid = get_seid(token)
        fromDate_str = data.get("fromDate")
        toDate_str = data.get("toDate")

        if fromDate_str == "None":
            bookings = db.SportsBooking.find(
                {"seid": seid, "bookingDate": toDate_str}, {"_id": 0}
            )

        else:
            bookings = db.SportsBooking.find(
                {
                    "seid": seid,
                    "bookingDate": {"$gte": fromDate_str, "$lte": toDate_str},
                },
                {"_id": 0},
            )

        return list(bookings)

    except Exception as ex:
        print("An error occurred:", ex)
        return []


def getParticularBooking(token, sportBookingId):
    try:
        seid = get_seid(token)
        return db.SportsBooking.find_one(
            {"seid": seid, "sportBookingId": sportBookingId}, {"_id": 0}
        )
    except Exception as ex:
        return None


# ?NEED TO UPDATE
def getQRCode(token, orderId):
    try:
        seid = get_seid(token)
        gateWay = db.Profiles.find_one({"seid": seid}).get("gateWay")
        apikey = gateWay.get("API_KEY")
        secretkey = gateWay.get("SECRET_KEY")
        current_time = int(time.time())
        close_by_time = current_time + 900

        razorpay_client = razorpay.Client(auth=(apikey, secretkey))
        customer = razorpay_client.customer.create(
            {
                "name": "Gaurav Kumar",
                "contact": 9123456780,
                "email": "gaurav.kumar@example.com",
                "fail_existing": 0,
                "notes": {
                    "notes_key_1": "Tea, Earl Grey, Hot",
                    "notes_key_2": "Tea, Earl Grey… decaf.",
                },
            }
        )
        print(customer["id"])

        response = razorpay_client.qrcode.create(
            {
                "type": "upi_qr",
                "name": "Store_1",
                "usage": "single_use",
                "fixed_amount": True,
                "payment_amount": 300,
                "description": "For Store 1",
                "customer_id": customer["id"],
                "close_by": close_by_time,
                "notes": {"purpose": "Test UPI QR code notes"},
            }
        )
        print(response["image_url"])
        print(response["status"])
        return True
    except Exception as ex:
        return False


# ✅
def makeBookingSuccess(token, data):
    try:
        seid = get_seid(token)
        sportBookingId = data.get("sportBookingId")
        orderId = data.get("orderId")
        print(seid, sportBookingId, orderId)
        booking = db.SportsBooking.find_one(
            {"seid": seid, "sportBookingId": sportBookingId, "payment.RefNo": orderId}
        )

        if booking:
            totalamt = booking.get("price", {}).get("totalAmount", 0)
            db.SportsBooking.find_one_and_update(
                {
                    "seid": seid,
                    "sportBookingId": sportBookingId,
                    "payment.RefNo": orderId,
                },
                {
                    "$set": {
                        "payment.Status": "SUCCESS",
                        "payment.PaymentProvider": "Dashboard",
                        "payment.Mode": "CASH",
                        "price.amountPaid": totalamt,
                    }
                },
            )
            return True
        else:
            print("Booking not found.")
            return False
    except Exception as ex:
        return False


# --------------------------- WEBSITE APIS ---------------------------#
def getSportForWebsite(seid):
    try:
        data = db.Sports.find({"seid": seid})
        sport_names = [sport["sportName"] for sport in data]
        return sport_names
    except Exception as ex:
        return None


def getParticularSlot(seid, sportId, querydate):
    try:
        data = db.Sports.find_one({"seid": seid, "sportId": sportId})
        if querydate in data.get("blockedSlots"):
            ret = data.get("blockedSlots").get(querydate)
            slots = data.get("slots")
            for val in slots:
                if ret[val] == True:
                    ret[val] = slots[val]
                else:
                    ret.pop(val)
            return ret
        return data.get("slots")
    except Exception as ex:
        return None


def addCustomPrice(token, maintaindata):
    try:
        seid = get_seid(token)

        data = db.Sports.find_one(
            {"seid": seid, "sportId": maintaindata.get("sportId")}
        ).get("customPrice")
        if maintaindata.get("date") not in data:
            data[maintaindata.get("date")] = {}
        data[maintaindata.get("date")][maintaindata.get("slotName")] = maintaindata.get(
            "turfprice"
        )
        db.Sports.find_one_and_update(
            {"seid": seid, "sportId": maintaindata.get("sportId")},
            {"$set": {"customPrice": data}},
        )
        return True, "Custom price added"
    except Exception as ex:
        return False, None


def addCustomPriceDayBasis(token, maintaindata):
    try:
        seid = get_seid(token)
        data = db.Sports.find_one(
            {"seid": seid, "sportId": maintaindata.get("sportId")}
        ).get("customPrice")
        start_date = datetime.strptime(maintaindata.get("fromdate"), "%Y-%m-%d")
        end_date = datetime.strptime(maintaindata.get("todate"), "%Y-%m-%d")
        current_date = start_date
        while current_date <= end_date:
            if str(current_date.weekday()) == maintaindata.get("day"):
                date_str = current_date.strftime("%Y-%m-%d")
                print(type(date_str))
                current_date += timedelta(days=1)
                if date_str not in data:
                    data[date_str] = {}
                data[date_str][maintaindata.get("slotName")] = maintaindata.get(
                    "turfprice"
                )
            else:
                print(current_date)
                current_date += timedelta(days=1)
        db.Sports.find_one_and_update(
            {"seid": seid, "sportId": maintaindata.get("sportId")},
            {"$set": {"customPrice": data}},
        )
        return True, "Custom price added"
    except Exception as ex:
        return False, "None"


def bulkUpdatePrice(token, data):
    try:
        seid = get_seid(token)
        for val in data:
            db.Sports.find_one_and_update(
                {"seid": seid, "sportId": val}, {"$set": {"customPrice": data[val]}}
            )

        return True, "Updated Successfully"
    except Exception as ex:
        return False, None


def helper(seid, date):
    try:
        data = []
        sports = db.Sports.find({"seid": seid}, {"_id": 0})

        for sport in sports:
            turf_order = []
            for val in sport.get("turfs"):
                turf_order.append(val["name"])
            slot_data = []

            for slot in sport["slots"]:
                turf_data = []
                for turfs in sport["turfs"]:
                    turf_data.append(
                        {
                            "name": turfs["name"],
                            "price": (
                                sport.get("customPrice")
                                .get(date)
                                .get(slot)
                                .get(turfs["name"])
                                if date in sport.get("customPrice")
                                and slot in sport.get("customPrice").get(date)
                                and turfs["name"]
                                in sport.get("customPrice").get(date).get(slot)
                                else turfs["price"]
                            ),
                        }
                    )

                slot_data.append(
                    {
                        "slotName": slot,
                        "slotEnd": sport["slots"][slot]["end"],
                        "slotStart": sport["slots"][slot]["start"],
                        "Turfs": turf_data,
                    }
                )
            data.append(
                {
                    "sportId": sport["sportId"],
                    "sportName": sport["sportName"],
                    "slotData": slot_data,
                }
            )

        return data
    except Exception as ex:
        return []


def getEightPrevAfter(token, data):
    try:
        seid = get_seid(token)
        date = data.get("date")
        return helper(seid, date)
    except Exception as ex:
        return None


def getAllUsers(token):
    try:
        seid = get_seid(token)
        users = list(db.SigninUser.find({}, {"_id": 0}))
        return True, users
    except Exception as ex:
        return False, None


def counterValueHelper(seid, date, sportId):
    try:
        data = []
        sport = db.Sports.find_one({"seid": seid, "sportId": sportId}, {"_id": 0})

        blockedSlots = sport.get("blockedSlots")
        blockedTurfs = sport.get("blockedTurfs")
        turf_order = []
        for val in sport.get("turfs"):
            turf_order.append(val["name"])
        bookings = db.SportsBooking.find(
            {"bookingDate": date, "sportId": sport["sportId"], "seid": seid}
        )
        slot_data = []

        store_data = {}
        for booking in bookings:
            if (
                booking.get("payment").get("Status") == "SUCCESS"
                or booking.get("payment").get("Status") == "ADVANCED"
            ):
                for val in booking["bookedSlots"]:
                    if val["slotName"] in store_data:
                        store_data[val["slotName"]].append(val["turfName"])
                    else:
                        store_data[val["slotName"]] = []
                        store_data[val["slotName"]].append(val["turfName"])

        for slot in sport["slots"]:
            turf_data = set()
            maxpres = False
            smallcount = 0
            for turfs in sport["turfs"]:
                if slot in store_data and turfs["name"] in store_data[slot]:
                    if turfs["name"] == turf_order[2]:
                        maxpres = True
                    else:
                        smallcount += 1
                else:
                    turf_data.add(turfs["name"])
            if maxpres:
                # If max one is pres then other turfs will not be there
                turf_data.clear()
            if smallcount == 1:
                # If any of the smaller turf is there then max one should not be there
                if len(turf_order) > 2 and turf_order[2] in turf_data:
                    turf_data.remove(turf_order[2])
            elif smallcount == 2:
                # If both smaller turf are booked then remove even the larger
                turf_data.clear()

            for val in blockedSlots:
                if val.get("date") == date:
                    if val.get("blockedSlots").get(slot, True) == False:
                        turf_data.clear()

            if date in blockedTurfs:
                if slot in blockedTurfs[date]:
                    slot_data.append(
                        {
                            "slotName": slot,
                            "slotEnd": sport["slots"][slot]["end"],
                            "slotStart": sport["slots"][slot]["start"],
                            "Turfs": [],
                        }
                    )
                else:
                    slot_data.append(
                        {
                            "slotName": slot,
                            "slotEnd": sport["slots"][slot]["end"],
                            "slotStart": sport["slots"][slot]["start"],
                            "Turfs": turf_data,
                        }
                    )

        return slot_data, turf_order
    except Exception as ex:
        return None, None


def CounterValue(data):
    try:
        seid = data.get("seid")
        val, turf_order = counterValueHelper(
            seid, data.get("date"), data.get("sportId")
        )
        print(val)

        def extract_num(slot):
            return int(slot["slotName"].replace("slot", ""))

        # Sort the data based on the numerical part of slotName
        val = sorted(val, key=extract_num)
        if len(val) == 0:
            return False, None
        obj = {}
        val.reverse()
        obj[val[0].get("slotName")] = {}
        for turf in turf_order:
            obj[val[0].get("slotName")][turf] = 1 if turf in val[0].get("Turfs") else 0

        for i in range(1, len(val)):
            obj[val[i].get("slotName")] = {}
            for turf in turf_order:
                obj[val[i].get("slotName")][turf] = (
                    1 + obj[val[i - 1].get("slotName")][turf]
                    if turf in val[i].get("Turfs")
                    else 0
                )
        return True, obj
    except Exception as ex:
        return False, None


def getTodayBooking(token):
    try:
        seid = get_seid(token)
        today_date = datetime.now()
        formatted_date = today_date.strftime("%Y-%m-%d")
        count = db.SportsBooking.count_documents(
            {"seid": seid, "bookingDate": formatted_date}
        )
        return True, count
    except Exception as ex:
        return False, 0
