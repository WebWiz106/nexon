import pymongo
import json
import settings
import constants
import utils
from model.bookings import Bookings

from datetime import datetime, date, timedelta
from usecases import room_usecase, mail_usecase
from model.booking_item import BookingItem
from model.guest_info import GuestInfo
import logging

from utils import db

#================================ROOM ALLOCATION============================================

def checker_overlap(st1,en1,st2,en2):
    print(st1,en1,st2,en2)
    st1 = datetime.strptime(st1, '%Y-%m-%d')
    en1 = datetime.strptime(en1, '%Y-%m-%d')
    st2 = datetime.strptime(st2, '%Y-%m-%d')
    en2 = datetime.strptime(en2, '%Y-%m-%d')
    print(st1,en1,st2,en2)
    #overlap pe return true
    if st1<st2:
        if en1>st2:
            return True
        else:
            return False
    elif st1>=st2 and st1<en2:
        return True
    return False    
    



def room_Number_allocation(hId,ndid,bookings,checkin, checkout,bookingId):
    
    allocated_room_number=[]
    for booking in bookings:
        rtype = booking["RoomType"]
        qty = booking["Qty"]
        if qty!=0:
            query=db.Rooms.find_one({"hId":hId,"ndid":ndid,"roomType":rtype})
            roomtypearr=query.get("roomNumbers")
            maintenance=query.get("inMaintanance")
            # maintenance = [{
            #     "roomNumber": roomNumber,
            #     "Message": Message,
            #     "start": start,
            #     "end": end
            # }]
            print(roomtypearr)#--->QTY ele chahiye 
            allocated=0
            for room in roomtypearr:
                #maintenance check
                chk=True
                for obj in maintenance:
                    rNo=obj["roomNumber"]
                    start=obj["start"]
                    end=obj["end"]
                    if rNo==room:
                        if checker_overlap(checkin,checkout,start,end):
                            chk=False
                print("CHECKOUT","CHECKOUT")
                print(checkin,checkout)
                print("DIVYANSHu")
                all_bookings=db.Bookings.find({"hId":hId,"ndid":ndid})
                for already_booking in all_bookings:
                    print("Abhay")
                    print(already_booking.get("roomNumbers"))
                    if room in already_booking.get("roomNumbers"):
                        print(checker_overlap(checkin,checkout,already_booking.get("checkIn"),already_booking.get("checkOut")))
                        if checker_overlap(checkin,checkout,already_booking.get("checkIn"),already_booking.get("checkOut")):
                            chk=False
                print("NIKLA")
                print(room,chk)
                #if pass in above check then allocated+=1
                if chk:
                    allocated+=1
                    allocated_room_number.append(room)
                if allocated==qty:
                    break
    
    print(allocated_room_number)
    db.Bookings.update_one({"bookingId":bookingId,"hId":hId,"ndid":ndid},{"$set":{"roomNumbers":allocated_room_number}})
    return ""


def room_Number_deallocation(hId,ndid,bookingId):
    print(hId,ndid,bookingId)
    db.Bookings.update_one({"bookingId":bookingId,"hId":hId,"ndid":ndid},{"$set":{"roomNumbers":[]}})

# =======================================Bookings=============================================
# ?MODELS DONE
def create_booking(booking_details):
    try:
        # print(booking_details)
        booking = Bookings.from_dict(booking_details)
        logging.info(f"{booking_details}")
        print(1)
        bookingId = get_booking_id()
        booking.bookingId = bookingId
        booking.bookingDate = str(datetime.now())
        print(2)
        db.Bookings.insert_one(Bookings.to_dict(booking))
        ndid = booking_details.get("ndid")
        hotelengine = db.BookingEngineData.find_one({"ndid": ndid,"hId":booking.hId})
        print(3)
        domain = db.Zucks_profile.find_one({"uId":ndid})
        hotelEmail=domain.get("hotelEmail")
        print(4)
        sendWith = "info@"+domain.get("domain")+".com"
        mailto = (booking_details.get("guestInfo")).get("EmailId")
        Name = (booking_details.get("guestInfo")).get("guestName")
        print(5)
        try:

            mail_usecase.Send_Booking_email(hotelengine.get("Details")[
                "Footer"]["Logo"], Name, hotelengine.get("Details")["HotelName"], bookingId, mailto, sendWith)
            

            mail_usecase.Send_Booking_emailToClient(hotelengine.get("Details")[
                "Footer"]["Logo"], hotelengine.get("Details")["HotelName"], bookingId, hotelEmail, sendWith,booking_details)

        except:
            print("Mail Not send")

        return True, "Success"
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS DONE
def update_booking(booking_details):
    try:
        logging.info(f"{booking_details}")
        ndid = booking_details.get("ndid")
        orderid = booking_details.get("orderid")
        paymentid = booking_details.get("paymentid")
        Status = booking_details.get("Status")
        hId = booking_details.get("hId")
        filter = {
            "ndid": ndid,
            "hId": hId,
            "payment.RefNo": orderid
        }
        hotelengine = db.BookingEngineData.find_one({"ndid": ndid, "hId": hId})

        existing_booking_data = db.Bookings.find_one(filter)
        if existing_booking_data:
            # Create a Booking object from existing data
            existing_booking = Bookings.from_dict(existing_booking_data)
            existing_booking.payment.status = Status if Status else existing_booking.payment.get(
                "Status")
            existing_booking.payment.payId = paymentid if paymentid else existing_booking.payment.get(
                "PayId")
            updated_booking_data = existing_booking.to_dict()
            result = db.Bookings.update_one(
                filter, {"$set": updated_booking_data})
            domain = db.Zucks_profile.find_one(
                {"uId": ndid})
            sendWith = "info@"+domain.get("domain")+".com"
            clientmail = domain.get("hotelEmail")

            try:
                mail_usecase.Send_Booking_confirmation(bookingId=existing_booking_data.get("bookingId"), email_to=existing_booking_data.get("guestInfo")["EmailId"], email_from=sendWith, logo=hotelengine.get("Details")["Footer"]["Logo"], name=existing_booking_data.get("guestInfo")["guestName"], hotelName=hotelengine.get(
                    "Details")["HotelName"], checkin=existing_booking_data.get("checkIn"), checkout=existing_booking_data.get("checkOut"), total=existing_booking_data.get("price")["Total"], phone=existing_booking_data.get("guestInfo")["Phone"], hotelnumber=hotelengine.get("Details")["Footer"]["Phone"])
                
                mail_usecase.Send_Booking_confirmation_to_client(bookingId=existing_booking_data.get("bookingId"), email_to=clientmail, customeremail=existing_booking_data.get("guestInfo")["EmailId"], email_from=sendWith, logo=hotelengine.get("Details")["Footer"]["Logo"], name=existing_booking_data.get("guestInfo")[
                    "guestName"], hotelName=hotelengine.get("Details")["HotelName"], checkin=existing_booking_data.get("checkIn"), checkout=existing_booking_data.get("checkOut"), total=existing_booking_data.get("price")["Total"], phone=existing_booking_data.get("guestInfo")["Phone"], hotelnumber=hotelengine.get("Details")["Footer"]["Phone"])
            except:
                print("Mail Not send")

            # update
            checkindate = existing_booking_data.get('checkIn')
            checkoutdate = existing_booking_data.get('checkOut')
            bookings = existing_booking_data.get('Bookings')
            # update Inventory
            # print(bookings)
            room_Number_allocation(hId,ndid,bookings,checkindate,checkoutdate,existing_booking_data.get("bookingId"))
            updateInventory_decrease(
                checkindate, checkoutdate, bookings, ndid, hId)
            logging.info(f"{True}")
            return True, "Success"
        else:
            return False, "Booking not found or not updated"
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT DONE ROOMS
def check_list_of_rooms_available_daterange(booking_details):
    available = {
        "DELUX": 0,
        "SUPERDELUX": 0,
        "SUITE": 0,
        "PREMIUM": 0,
        "PremiereRetreat":0,
        "EliteSuite":0,
        "GrandDeluxe":0,
        "ImperialSuite":0,
        "SupremeRetreat":0,
        "RoyalDeluxe":0,
        "PrestigeSuite":0,
        "ExclusiveRetreat":0
    }
    try:
        ndid = booking_details.get("ndid")
        hId = booking_details.get("hId")
        checkin = booking_details.get("checkin")
        checkout = booking_details.get("checkout")
        number_of_days_between = get_dates_in_range(checkin, checkout)
        # print(number_of_days_between)
        rooms = db.Rooms.find({"ndid": ndid, "hId": hId})
        for room in rooms:
            min_room = 99999
            inventory = room.get('inventoryStatus', {})
            for days in number_of_days_between:
                if (str(days) in inventory):
                    max_room = int(inventory[str(days)])
                else:
                    max_room = int(room.get('noOfRooms'))
                if (max_room < min_room):
                    min_room = max_room
            if (room.get('roomType') == "1"):
                available["DELUX"] = min_room
            if (room.get('roomType') == "2"):
                available["SUPERDELUX"] = min_room
            if (room.get('roomType') == "3"):
                available["SUITE"] = min_room
            if (room.get('roomType') == "4"):
                available["PREMIUM"] = min_room
            if (room.get('roomType') == "5"):
                available["PremiereRetreat"] = min_room
            if (room.get('roomType') == "6"):
                available["EliteSuite"] = min_room
            if (room.get('roomType') == "7"):
                available["GrandDeluxe"] = min_room
            if (room.get('roomType') == "8"):
                available["ImperialSuite"] = min_room
            if (room.get('roomType') == "9"):
                available["SupremeRetreat"] = min_room
            if (room.get('roomType') == "10"):
                available["RoyalDeluxe"] = min_room
            if (room.get('roomType') == "11"):
                available["PrestigeSuite"] = min_room
            if (room.get('roomType') == "12"):
                available["ExclusiveRetreat"] = min_room
             
        return True, available
    except:
        return False, available


# ?MODELS NOT DONE ROOMS
def updateInventory_decrease(checkin, checkout, bookingsarray, ndid, hId):
    try:
        dates = get_dates_in_range(checkin, checkout)
        for booking in bookingsarray:
            if booking['Qty'] > 0:
                room = db.Rooms.find_one(
                    {"ndid": ndid, "hId": hId, "roomType": booking["RoomType"]})
                inventory = room.get('inventoryStatus', {})
                for d in dates:
                    if (str(d) in inventory):
                        inventory[str(d)] = int(inventory[str(d)]) - int(booking['Qty'])
                    else:
                        inventory[str(d)] = int(room.get('noOfRooms'))-int(booking['Qty'])
                room = db.Rooms.find_one_and_update({"ndid": ndid, "hId": hId, "roomType": booking["RoomType"]}, {"$set": {
                    "inventoryStatus": inventory
                }})
    except Exception as e:
        logging.error(f"Error Updating inventory increase:{e}")

# ?MODELS NOT DONE ROOMS
def updateInventory_increase(checkin, checkout, bookingsarray, ndid, hId):
    try:
        dates = get_dates_in_range(checkin, checkout)
        for booking in bookingsarray:
            if booking['Qty'] > 0:
                room = db.Rooms.find_one(
                    {"ndid": ndid, "hId": hId, "roomType": booking["RoomType"]})
                inventory = room.get('inventoryStatus')
                for d in dates:
                    inventory[str(d)] = int(inventory[str(d)])+int(booking['Qty'])
                room = db.Rooms.find_one_and_update({"ndid": ndid, "hId": hId, "roomType": booking["RoomType"]}, {"$set": {
                    "inventoryStatus": inventory
                }})
    except Exception as e:
        logging.error(f"Error Updating inventory decrease:{e}")

# ?MODELS DONE
def editBookingGuestInfo(booking_details):
    try:
        logging.info(f"{booking_details}")
        bookingId = booking_details.get("bookingId")
        guestInfo = booking_details.get("guestInfo")
        booking_exists = Bookings.from_dict(
            db.Bookings.find_one({"bookingId": bookingId}))
        booking_exists.guestInfo = GuestInfo.from_dict(guestInfo)
        editInfo = db.Bookings.find_one_and_update(
            {"bookingId": bookingId}, {"$set": Bookings.to_dict(booking_exists)})
        logging.info(f"{True}")
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT REQUIRED
def get_booking_id():
    try:
        query = {
            "bookingDate": {
                "$gte": str(date.today()) + " 00:00",
                "$lte": str(date.today()) + " 23:59"
            }
        }
        print("entered")
        booking_count = str(db.Bookings.count_documents(query)+1)
        print(booking_count)
        logging.info(f"{booking_count}")
        return "B" + date.today().strftime("%Y%m%d") + get_id(booking_count)
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)

# ?MODELS NOT DONE ROOMS
def create_room_id(ndid, hId, type, checkIn):
    try:
        logging.info(f"{ndid},{type},{checkIn}")
        roomid = type+"0"
        query = {
            "ndid": ndid,
            "roomType": type,
            "checkIn": checkIn
        }
        Total_rooms = db.Rooms.find_one(
            {"ndid": ndid, "hId": hId, "roomType": type})
        booking_count = str(db.Bookings.count_documents(query)+1)
        if int(Total_rooms.get("noOfRooms")) < int(booking_count):

            return "0000"

        if (int(booking_count) > 9):
            roomid = roomid+booking_count
        else:
            roomid = roomid+"0"+booking_count
        logging.info(f"{roomid}")
        return roomid
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)

# ?MODELS NOT DONE UNABLE TO DO
def get_all_bookings(token, hId, type):
    try:
        logging.info(f"{token},{type}")
        ndid = utils.get_ndid(token)
        if type == "0":
            bookings = db.Bookings.find({"ndid": ndid, "hId": hId})
        else:
            bookings = db.Bookings.find({"ndid": ndid, "hId": hId, "Bookings": {
                "$elemMatch": {
                    "RoomType": type,
                    "Qty": {"$gt": 0}
                }
            }})

        result_list = [(booking) for booking in bookings]
        logging.info(f"{result_list}")
        return True, result_list
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT DONE UNABLE TO DO
def todays_checkin(token, hId, today):
    try:
        logging.info(f"{token},{today}")
        ndid = utils.get_ndid(token)
        query = {
            "hId": hId,
            "ndid": ndid,
            "checkIn": today
        }
        bookings = db.Bookings.find(query)
        booking_count = db.Bookings.count_documents(query)

        Booking_list = [booking for booking in bookings]
        logging.info(f"{booking_count},{Booking_list}")
        return True, booking_count, Booking_list
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT DONE UNABLE TO DO
def todays_checkout(token, hId, today):
    try:
        ndid = utils.get_ndid(token)
        query = {
            "hId": hId,
            "ndid": ndid,
            "checkOut": today
        }
        bookings = db.Bookings.find(query)
        booking_count = db.Bookings.count_documents(query)

        Booking_list = [booking for booking in bookings]
        logging.info(f"{booking_count},{Booking_list}")
        return True, booking_count, Booking_list
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT DONE UNABLE TO DO
def check_list_of_bookings(ndid, hId, checkin, checkout):
    try:
        logging.info(f"{ndid},{checkin},{checkout}")
        # booking have checkin small and checkout greata
        query1 = {
            "checkIn": {
                "$lte": checkin
            },
            "checkOut": {
                "$gte": checkout
            }
        }

        # booking have checkin small but checkout small then my checkout
        query2 = {
            "checkIn": {
                "$lte": checkin
            },
            "checkOut": {
                "$gte": checkin,
                "$lt": checkout
            },
        }

        query3 = {
            "checkIn": {
                "$gt": checkin,
                "$lte": checkout
            },
            "checkOut": {
                "$gte": checkout
            }
        }

        query4 = {
            "checkIn": {
                "$gt": checkin,
                "$lt": checkout
            },
            "checkOut": {
                "$lt": checkout
            }
        }

        bookings4 = db.Bookings.find({
            "ndid": ndid,
            "hId": hId,
            "payment.Status": {
                "$in": ["SUCCESS", "ADVANCED"]
            },
            "$or": [query1, query2, query3, query4]})

        Delux = SuperDelux = Suite = Premium =PremiereRetreat=EliteSuite=GrandDeluxe=ImperialSuite=SupremeRetreat=RoyalDeluxe=PrestigeSuite=ExclusiveRetreat =0

        for booking in bookings4:
            for bookingdata in booking.get("Bookings"):
                if bookingdata.get("Qty") > 0:
                    if bookingdata.get('RoomType') == "1":
                        Delux += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "2":
                        SuperDelux += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "3":
                        Suite += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "4":
                        Premium += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "5":
                        PremiereRetreat += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "6":
                        EliteSuite += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "7":
                        GrandDeluxe += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "8":
                        ImperialSuite += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "9":
                        SupremeRetreat += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "10":
                        RoyalDeluxe += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "11":
                        PrestigeSuite += bookingdata.get("Qty")

                    if bookingdata.get('RoomType') == "12":
                        ExclusiveRetreat += bookingdata.get("Qty")


        logging.info(f"{Delux},{SuperDelux},{Suite},{Premium},{PremiereRetreat},{EliteSuite},{GrandDeluxe},{ImperialSuite},{SupremeRetreat},{RoyalDeluxe},{PrestigeSuite},{ExclusiveRetreat}")
        return Delux, SuperDelux, Suite, Premium,PremiereRetreat,EliteSuite,GrandDeluxe,ImperialSuite,SupremeRetreat,RoyalDeluxe,PrestigeSuite,ExclusiveRetreat
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)


# ?MODELS NOT DONE ROOMS
def check_no_rooms(ndid, hId, type):
    try:
        logging.info(f"{ndid},{type}")
        delux = db.Rooms.find_one({"ndid": ndid, "hId": hId, "roomType": type})
        logging.info(f"{delux}")
        return int(delux.get("noOfRooms")) if delux != None else 0
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)

# ?MODELS NOT REQUIRED
def calculate_booking_total(booking_details, ndid, hId):
    try:
        logging.info(f"{booking_details},{ndid}")
        check_in_str = booking_details.get("checkIn")
        check_out_str = booking_details.get("checkOut")
        print(booking_details)
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d")
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d")
        room_type = booking_details.get("roomType")
        room_type_name = constants.room_type_name.get(room_type)
        room = room_usecase.get_room(ndid, hId, room_type_name)
        if room:
            if room.get("isWeekendFormat"):
                weekend, weekday = count_weekdays_and_weekends(check_in, check_out)
                weekend_price = room.get("changedPrice").get("weekend") if room.get(
                    "changedPrice").get("weekend") else room.get("price")
                weekday_price = room.get("changedPrice").get("weekday") if room.get(
                    "changedPrice").get("weekday") else room.get("price")
                total_price = weekend * int(weekend_price) + \
                    weekday * int(weekday_price)
            else:
                total_price = 0
                while check_in < check_out:
                    total_price += int(room.get("changedPrice").get(str(check_in.date()))) if room.get(
                        "changedPrice").get(str(check_in.date())) else int(room.get("price"))
                    check_in += timedelta(days=1)

            price = total_price
            addTax=db.BookingEngineData.find_one({"hId":hId,"ndid":ndid}).get("addTax")
            if addTax:
                gst = 0.18*price
            else:
                gst=0
            Totalprice = gst+price
            logging.info(f"{price},{total_price},{gst}")
            return {"Price": price, "TotalPrice": Totalprice, "Tax": gst}
        else:
            return {"Price": 0, "TotalPrice": 0, "Tax": 0}
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)

# ?MODELS NOT DONE UNABLE TO DO
def get_dates_range_booking(booking_details):
    try:
        logging.info(f"{booking_details}")
        token = booking_details.get("token")
        checkin = booking_details.get("checkIn")
        checkout = booking_details.get("checkOut")
        hId = booking_details.get("hId")
        ndid = utils.get_ndid(token)
        query = {
            "hId": hId,
            "ndid": ndid,
            "checkIn": {
                "$gte": checkin
            },
            "checkOut": {
                "$lte": checkout
            }
        }
        # print(query)

        bookings = db.Bookings.find(query)
        booking_list = [booking for booking in bookings]
        logging.info(f"{booking_list}")
        return True, booking_list
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT DONE UNABLE TO DO
def get_bookingid_range_booking(booking_details):
    try:
        logging.info(f"{booking_details}")
        token = booking_details.get("token")
        bookingId = booking_details.get("bookingId")
        hId = booking_details.get("hId")
        ndid = utils.get_ndid(token)
        query = {
            "hId": hId,
            "ndid": ndid,
            "bookingId": bookingId
        }

        bookings = db.Bookings.find(query)
        Booking_list = [booking for booking in bookings]
        logging.info(f"{Booking_list}")
        return True, Booking_list
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT DONE UNABLE TO DO
def booking_on_filter_peyment_status(status, token, hId):
    try:
        logging.info(f"{status},{token}")
        ndid = utils.get_ndid(token)
        if status == '1':
            bookings = db.Bookings.find(
                {"ndid": ndid, "payment.Status": "PENDING", "hId": hId})
        if status == '2':
            bookings = db.Bookings.find(
                {"ndid": ndid, "payment.Status": "ADVANCED", "hId": hId})
        if status == '3':
            bookings = db.Bookings.find(
                {"ndid": ndid, "payment.Status": "SUCCESS", "hId": hId})

        Booking_list = [booking for booking in bookings]
        logging.info(f"{Booking_list}")
        return True, Booking_list
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS DONE
def cancel_booking_payment_status(token, booking_id, status, hId):
    try:
        logging.info(f"{token},{booking_id},{status}")
        ndid = utils.get_ndid(token)
        print(ndid)
        print(hId)
        print(booking_id)
        booking_exists = db.Bookings.find_one({"ndid": ndid, "bookingId": booking_id,"hId":hId})
        if status == "SUCCESS" or status == "ADVANCED":
            print(1)
            print(booking_exists)
            if (booking_exists["payment"].get("Status") == "PENDING" or booking_exists["payment"].get("Status") == "CANCELLED"):
                # update
                print(2)
                checkindate = booking_exists.get("checkIn")
                checkoutdate = booking_exists.get("checkOut")
                bookings = []
                for ele in booking_exists.get("Bookings"):
                    bookings.append(ele)
                # update Inventory
                print(2)
                room_Number_allocation(hId,ndid,bookings,checkindate,checkoutdate,booking_id)
                updateInventory_decrease(
                    checkindate, checkoutdate, bookings, ndid, hId)
            
            db.Bookings.find_one_and_update({"ndid": ndid, "hId": hId, "bookingId": booking_id}, {
                                            "$set":{
                                                "payment.Status":status,
                                                "payment.payId":"USER DASHBOARD"
                                            }})
            if status=="SUCCESS":
                total=db.Bookings.find_one({"ndid": ndid, "hId": hId, "bookingId": booking_id})["price"]["Total"]
                db.Bookings.find_one_and_update({"ndid": ndid, "hId": hId, "bookingId": booking_id},{"$set":{"price.amountPay":total}})
        else:
            db.Bookings.find_one_and_update({"ndid": ndid, "hId": hId, "bookingId": booking_id}, {
                                            "$set": {
                                                "payment.Status":status
                                            }})
        logging.info("True")
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS DONE
def change_booking_checked_in_out_status(token, booking_id, isCheckedin, isCheckout, hId):
    try:
        logging.info(f"{token},{booking_id},{isCheckedin},{isCheckout},{hId}")
        if isCheckedin == "false":
            logging.info("False")
            return False
        else:
            ndid = utils.get_ndid(token)
            booking_exist = Bookings.from_dict(db.Bookings.find_one(
                {"ndid": ndid, "hId": hId, "bookingId": booking_id}))
            booking_exist.isCheckedIn = isCheckedin=="true"
            booking_exist.isCheckedOut = isCheckout== "true"
            db.Bookings.find_one_and_update({"ndid": ndid, "hId": hId, "bookingId": booking_id}, {
                                            "$set": Bookings.to_dict(booking_exist)})
            logging.info(f"True")
            return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS DONE
def cancel_booking_usecase(token, bookingid, hId):
    try:
        logging.info(f"{token},{bookingid}")
        ndid = utils.get_ndid(token)
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
        room_Number_deallocation(hId,ndid,bookingid)
        updateInventory_increase(
            checkindate, checkoutdate, bookings, ndid, hId)
        logging.info(f"True")
        return True
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT REQUIRED
def is_weekend(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        return date.weekday() in [5, 6]
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)

# ?MODELS NOT REQUIRED
def count_weekdays_and_weekends(start_date, end_date):
    try:
        logging.info(f"{start_date},{end_date}")
        weekdays_count = weekends_count = 0
        while start_date < end_date:
            if is_weekend(start_date.strftime("%Y-%m-%d")):
                weekends_count += 1
            else:
                weekdays_count += 1
            start_date += timedelta(days=1)
        logging.info(f"{weekdays_count} ,{weekends_count}")
        return weekdays_count, weekends_count
    except Exception as ex:
        logging.error(f"{ex}")
        return None, "{}".format(ex)

# ?MODELS NOT REQUIRED
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

# ?MODELS NOT REQUIRED
def avaiblity_of_rooms(booking_details):
    try:
        logging.info(f"{booking_details}")
        ndid = booking_details.get("ndid")
        hId = booking_details.get("hId")
        checkin = booking_details.get("checkin")
        checkout = booking_details.get("checkout")
        deluxrooms = check_no_rooms(ndid, hId, "1")
        superdeluxrooms = check_no_rooms(ndid, hId, "2")
        suiterooms = check_no_rooms(ndid, hId, "3")
        premiumrooms = check_no_rooms(ndid, hId, "4")
        premiereRetreatrooms=check_no_rooms(ndid, hId, "5")
        eliteSuiterooms=check_no_rooms(ndid, hId, "6")
        grandDeluxerooms=check_no_rooms(ndid, hId, "7")
        imperialSuiterooms=check_no_rooms(ndid, hId, "8")
        supremeRetreatrooms=check_no_rooms(ndid, hId, "9")
        royalDeluxerooms=check_no_rooms(ndid, hId, "10")
        prestigeSuiterooms=check_no_rooms(ndid, hId, "11")
        exclusiveRetreatrooms=check_no_rooms(ndid, hId, "12")
        
        delux, superdelux, suite, premium,premiereRetreat,eliteSuite,grandDeluxe,imperialSuite,supremeRetreat,royalDeluxe,prestigeSuite,exclusiveRetreat = check_list_of_bookings(
            ndid, hId, checkin, checkout)
        print(delux, superdelux, suite, premium)
        available = {
            "DELUX": deluxrooms-delux if deluxrooms-delux > 0 else 0,
            "SUPERDELUX": superdeluxrooms-superdelux if superdeluxrooms-superdelux > 0 else 0,
            "SUITE": suiterooms-suite if suiterooms-suite > 0 else 0,
            "PREMIUM": premiumrooms-premium if premiumrooms-premium > 0 else 0,
            "PremiereRetreat": premiereRetreatrooms-premiereRetreat if premiereRetreatrooms-premiereRetreat > 0 else 0,
            "EliteSuite": eliteSuiterooms-eliteSuite if eliteSuiterooms-eliteSuite > 0 else 0,
            "GrandDeluxe": grandDeluxerooms-grandDeluxe if grandDeluxerooms-grandDeluxe > 0 else 0,
            "ImperialSuite": imperialSuiterooms-imperialSuite if imperialSuiterooms-imperialSuite > 0 else 0,
            "SupremeRetreat": supremeRetreatrooms-supremeRetreat if supremeRetreatrooms-supremeRetreat > 0 else 0,
            "RoyalDeluxe": royalDeluxerooms-royalDeluxe if royalDeluxerooms-royalDeluxe > 0 else 0,
            "PrestigeSuite": prestigeSuiterooms-prestigeSuite if prestigeSuiterooms-prestigeSuite > 0 else 0,
            "ExclusiveRetreat": exclusiveRetreatrooms-exclusiveRetreat if exclusiveRetreatrooms-exclusiveRetreat > 0 else 0
        }
        return True, available
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

# ?MODELS NOT REQUIRED
def get_dates_in_range(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        # Calculate the number of days between start_date and end_date
        delta = end_date - start_date
        # Generate a list of dates within the date range
        date_list = [start_date + timedelta(days=i) for i in range(delta.days)]
        return date_list
    except Exception as e:
        logging.error(f"Error in getting date in range:{e}")


def getGateways(ndid,hid):
    try:
        # print(ndid)
        # print(hid)
        engine = db.BookingEngineData.find_one({"ndid":ndid,"hId":hid})
        # print(engine)
        # print(engine["Details"]["Gateway"])
        gateway = engine["Details"]["Gateway"]
        return gateway.get("Type"), gateway.get("API_KEY"),gateway.get("SECRET_KEY")
    except Exception as e:
        logging.error(f"Error in getting data:{e}")

def getBookingDetailForCancellation(ndid,hId,bookingId):
    try:
        data=db.Bookings.find_one({"bookingId":bookingId,"hId":hId,"ndid":ndid})
        obj={
            "Adults":data["Adults"],
            "roomNumbers":data["roomNumbers"],
            "bookingId":data["bookingId"],
            "bookingDetails":[],
            "guestInfo":data["guestInfo"],
            "Kids":data["Kids"],
            "paymentMode":data["payment"]["Mode"],
            "paymentStatus":data["payment"]["Status"],
            "price":data["price"],
            "bookingDate":data["bookingDate"]
        }
        for val in data["Bookings"]:
            if val["Qty"]>0:
                print(constants.room_type_name[val["RoomType"]])
                obj["bookingDetails"].append({"RoomType":constants.room_type_name[val["RoomType"]],"Quantity":val["Qty"]})
            # obj["bookingDetails"].append({constants.room_type_name[val["RoomType"]]})
            # print(val)
        return True,obj
    except Exception as ex:
        return False,None
    

def successPaymentGetData(ndid,hid,bookingId):
    try:
        data=db.Bookings.find_one({"hId":hid,"ndid":ndid,"bookingId":bookingId})
        bookingenginedata=db.BookingEngineData.find_one({"hId":hid,"ndid":ndid})
        logo=bookingenginedata.get("Details").get("Footer").get("Logo")
        hotelname=bookingenginedata.get("Details").get("HotelName")
        return True,data,logo,hotelname
    except Exception as ex:
        return False