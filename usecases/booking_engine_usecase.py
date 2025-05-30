import utils
import constants
import pymongo
import json
import settings
import logging

from bson import json_util
from usecases import mail_usecase,booking_usecase
import random
from model.bookings import Bookings
from model.booking_item import BookingItem
from datetime import datetime, date, timedelta
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db

def get_engine(token, hId):
    try:
        logging.info(f"{token}")
        logging.info(f"{token}")
        ndid = utils.get_ndid(token)
        details = get_engine_details(ndid, hId)
        if details:
            return True, details
        else:
            return False, "No Engine registered with this id"
    except Exception as ex:
        LOGGER.error("Unabel to get engine datas:{}".format(ex))
        logging.error(f"{ex}")
        return False, "Error Occured"


def get_engine_details(ndid, hId):
    try:
        logging.info(f"{ndid}")
        data = db.BookingEngineData.find_one({"ndid": ndid, "hId": hId})
        logging.info(f"{data}")
        if data and "Details" in data:
            logging.info(f"Details found: {data['Details']}")
            return data["Details"]
        else:
            logging.warning(
                "Details not found for ndid: {} and hId: {}".format(ndid, hId))
            return False
    except Exception as ex:
        LOGGER.error("Unabel to get engine datas:{}".format(ex))
        logging.error(f"{ex}")
        return False


def get_engine_webiste(id):
    try:
        logging.info(f"{id}")
        website_data = db.Zucks_hotellinks.find_one({"ndid": id})
        if website_data:
            dashboard_link = website_data.get("dashboardLink")
            website_link = website_data.get("websiteLink")

            if dashboard_link and dashboard_link != "None":
                logging.info(f"Dashboard link found: {dashboard_link}")
                return dashboard_link
            elif website_link:
                logging.info(f"Website link found: {website_link}")
                return website_link
            else:
                logging.warning("No valid links found for ID: {}".format(id))
                return False
        else:
            logging.warning("No data found for ID: {}".format(id))
            return False
    except Exception as ex:
        LOGGER.error("Unabel to get engine websites:{}".format(ex))
        logging.error(f"{ex}")
        return False, "Error Occured"


def get_profile(id):
    try:
        logging.info(f"{id}")
        profile = db.Zucks_profile.find_one({"uId": id})
        if profile:
            logging.info(f"{profile}")
            return profile
        else:
            logging.warning(f"No profile found for ID: {id}")
            return False
    except Exception as ex:
        LOGGER.error("Unabel to get Profile:{}".format(ex))
        logging.error(f"{ex}")
        return False


def create_query_rates(booking_details, id):
    try:
        logging.info(f"{booking_details}, {id}")
        ndid = booking_details.get("id")
        hotelengine = db.BookingEngineData.find_one({"ndid": id})
        domain = db.Zucks_profile.find_one(
            {"hotelName": hotelengine.get("Details")["HotelName"]})

        name = booking_details.get("Name")
        EmailId = booking_details.get("EmailId")
        Number = booking_details.get("Number")
        Adults = booking_details.get("Adults")
        Kids = booking_details.get("Kids")
        Rooms = booking_details.get("Rooms")
        Checkin = booking_details.get("Checkin")
        Checkout = booking_details.get("Checkout")
        City = booking_details.get("City")
        Message = booking_details.get("Message")
        hId = booking_details.get("hId")
        db.Query_Clients.insert_one({
            "ndid": str(id),
            "hId": hId,
            "Name": name,
            "EmailId": EmailId,
            "Number": Number,
            "Adults": Adults,
            "Kids": Kids,
            "Rooms": Rooms,
            "Checkin": Checkin,
            "Checkout": Checkout,
            "City": City,
            "Message": Message
        })

        sendWith = "info@"+domain.get("domain")+".com"
        endUserEmail = booking_details.get("EmailId")
        clientEmail = sendWith
        personalclientemail = domain.get("domain")+"@gmail.com"

        mail_usecase.Send_Query_recieved(hotelengine.get("Details")["Footer"]["Logo"], name, hotelengine.get(
            "Details")["HotelName"], hotelengine.get("Details")["Footer"]["Phone"], endUserEmail, sendWith)
        
        mail_usecase.Send_Query_recieved_to_client(hotelengine.get("Details")["Footer"]["Logo"], hotelengine.get("Details")[
            "HotelName"], name, EmailId, Number, Adults, Kids, Rooms, Checkin, Checkout, City, Message, clientEmail, sendWith)
        try:
            mail_usecase.Send_Query_recieved_to_client(hotelengine.get("Details")["Footer"]["Logo"], hotelengine.get("Details")[
                "HotelName"], name, EmailId, Number, Adults, Kids, Rooms, Checkin, Checkout, City, Message, personalclientemail, sendWith)
        except:
            logging.error(f"email failed")
            print("email failed")
        return hotelengine.get("Details")["HotelName"]
    except Exception as ex:
        LOGGER.error("Unabel to create query rates:{}".format(ex))
        logging.error(f"{ex}")
        return False, "Error Occured"


def change_currency_profile_online_payment_status(booking_details, ndid):
    try:
        logging.info(f"{booking_details}, {ndid}")
        currency = booking_details.get("currency")
        online_payment = booking_details.get("isOnlinepayment")
        hId = booking_details.get("hId")
        db.BookingEngineData.find_one_and_update({"ndid": ndid, "hId": hId}, {"$set": {
            "Details.isOnlinePayment": online_payment == "true"
        }})

        hotelengine = db.BookingEngineData.find_one({"ndid": ndid})
        hotelname = hotelengine["Details"]["HotelName"]

        db.Zucks_profile.find_one_and_update({"hotelName": hotelname}, {"$set": {
            "currency": currency
        }})
        logging.info(f"{True}")
        return True
    except Exception as ex:
        LOGGER.error("Unabel to get engine datas:{}".format(ex))
        logging.error(f"{ex}")
        return False, "Error Occured"


def uploadDigitalCheckinData(promo_details):
    try:
        logging.info(f"{promo_details}")
        token = promo_details.get("token")
        hId = promo_details.get("hId")
        enquiry_bookingid = promo_details.get("enquiry_bookingid")
        enquiry_Name = promo_details.get("enquiry_Name")
        enquiry_email = promo_details.get("enquiry_email")
        enquiry_phone = promo_details.get("enquiry_phone")
        enquiry_gender = promo_details.get("enquiry_gender")
        enquiry_group_size = promo_details.get("enquiry_group_size")
        enquiry_Address = promo_details.get("enquiry_Address")
        enquiry_State = promo_details.get("enquiry_State")
        enquiry_city = promo_details.get("enquiry_city")
        GovtId = promo_details.get("GovtId")
        Passport = promo_details.get("Passport")
        Visa = promo_details.get("Visa")

        ndid = utils.get_ndid(token)
        db.DigitalCheckin.insert_one({
            "hId": hId,
            "ndid": str(ndid),
            "BookingId": enquiry_bookingid,
            "Name": enquiry_Name,
            "Email": enquiry_email,
            "Phone": enquiry_phone,
            "Gender": enquiry_gender,
            "GroupSize": enquiry_group_size,
            "Address": enquiry_Address,
            "State": enquiry_State,
            "City": enquiry_city,
            "GovtId": GovtId,
            "Passport": Passport,
            "Visa": Visa,
            "Filldate": str(datetime.now())
        })

        try:

            db.Bookings.find_one_and_update({"ndid": str(ndid), "hId": hId, "bookingId": enquiry_bookingid}, {"$set": {
                "digitalCheckin": {
                    "Name": enquiry_Name,
                    "Email": enquiry_email,
                    "Phone": enquiry_phone,
                    "Gender": enquiry_gender,
                    "GroupSize": enquiry_group_size,
                    "Address": enquiry_Address,
                    "State": enquiry_State,
                    "City": enquiry_city,
                    "GovtId": GovtId,
                    "Passport": Passport,
                    "Visa": Visa
                }
            }})

        except:
            pass
        logging.info("True")
        return True
    except Exception as ex:
        LOGGER.error("Unabel to get engine datas:{}".format(ex))
        logging.error(f"{ex}")
        return False, "Error Occured"


def sendOtp(bookingId, ndid, hId):
    # send mail
    try:
        sender = db.WebsiteData.find_one({"ndid": ndid, "hId": hId}).get("Domain") + ".com"
        # sender="info@eazotel.com"
        receiver = db.Bookings.find_one({"ndid": ndid, "hId": hId, "bookingId": bookingId}).get("guestInfo").get("EmailId")
        otp = random.randint(100000, 999999)
        receiver_arr=[]
        receiver_arr.append(receiver)
        resp=mail_usecase.send_email("6 Digit Otp for Booking Cancellation", f"Your Otp is {otp}", sender, receiver_arr)
        print(0)
        print(resp)
        print(1)
        print(receiver)
        print(2)        
        # database setup
        db.Bookings.find_one_and_update(
            {"bookingId": bookingId, "ndid": ndid, "hId": hId},
            {"$set": {"bookingCancelOtp": str(otp)}}
        )
        return True,f"Otp generated please check for any mail sent from {sender}"
    except Exception as ex:
        return False,"Otp Generation Process Failed"

def cancelBookingFromBookingEngine(bookingId,ndid,hId,otp):
    try:
        otpindb=db.Bookings.find_one({"hId":hId,"ndid":ndid,"bookingId":bookingId}).get("bookingCancelOtp")
        if otpindb!=otp:
            return False,"Otp doesn't match try again"
        booking_exist = Bookings.from_dict(db.Bookings.find_one(
            {"ndid": ndid, "bookingId": bookingId, "hId": hId}))
        booking_exist.payment.status = "CANCELLED"
        db.Bookings.find_one_and_update({"ndid": ndid, "bookingId": bookingId, "hId": hId}, {
                                        "$set": Bookings.to_dict(booking_exist)})
        booking = Bookings.from_dict(db.Bookings.find_one(
            {"ndid": ndid, "hId": hId, "bookingId": bookingId}))
        # update
        checkindate = booking.checkIn
        checkoutdate = booking.checkOut
        bookings = []
        for ele in booking.bookingItems:
            bookings.append(BookingItem.to_dict(ele))
        # update Inventory
        print(bookings)
        booking_usecase.room_Number_deallocation(hId,ndid,bookingId)
        booking_usecase.updateInventory_increase(
            checkindate, checkoutdate, bookings, ndid, hId)
        return True,"Booking cancelled successfully"
    except Exception as ex :
        return False,f"Booking Cancellation Failed {ex}"
    

def cancelBookingFromBookingEnginewithoutOtp(bookingId,ndid,hId):
    try:

        booking_exist = Bookings.from_dict(db.Bookings.find_one(
            {"ndid": ndid, "bookingId": bookingId, "hId": hId}))
        booking_exist.payment.status = "CANCELLED"
        db.Bookings.find_one_and_update({"ndid": ndid, "bookingId": bookingId, "hId": hId}, {
                                        "$set": Bookings.to_dict(booking_exist)})
        booking = Bookings.from_dict(db.Bookings.find_one(
            {"ndid": ndid, "hId": hId, "bookingId": bookingId}))
        # update
        checkindate = booking.checkIn
        checkoutdate = booking.checkOut
        bookings = []
        for ele in booking.bookingItems:
            bookings.append(BookingItem.to_dict(ele))
        # update Inventory
        print(bookings)
        booking_usecase.room_Number_deallocation(hId,ndid,bookingId)
        booking_usecase.updateInventory_increase(
            checkindate, checkoutdate, bookings, ndid, hId)
        return True,"Booking cancelled successfully"
    except Exception as ex :
        return False,f"Booking Cancellation Failed {ex}"