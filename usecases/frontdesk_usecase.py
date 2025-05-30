import utils
import constants
import pymongo
import json
import settings
import logging
from datetime import datetime, timedelta

from bson import json_util
from usecases import booking_usecase
from model.dashboardpackages import DashboardPackage
from datetime import datetime, date, timedelta
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db


def incrementDayByOne(given_date_str):
    given_date = datetime.strptime(given_date_str, "%Y-%m-%d")
    next_day = given_date + timedelta(days=1)
    return next_day.strftime("%Y-%m-%d")


# if first time entry then date:(numberOfRooms-1) 
# else {key:val} ==> {key:val-1}
def add_inventory(hId, ndid, roomNumber, current_date):
    try:
        query = {"ndid": ndid, "hId": hId, "roomNumbers": {"$in": [roomNumber]}}
        room = db.Rooms.find_one(query)

        if room:
            inventory_status = room.get("inventoryStatus", {})
            no_of_rooms = int(room.get("noOfRooms", 0))
            if current_date in inventory_status:
                current_value = int(inventory_status[current_date])
                inventory_status[current_date] = max(current_value - 1, 0)
            else:
                inventory_status[current_date] = max(no_of_rooms - 1, 0)
            db.Rooms.update_one(query, {"$set": {"inventoryStatus": inventory_status}})
            print(f"Inventory updated for {current_date}: {inventory_status}")
        else:
            print("Room not found in the database")
    except Exception as ex:
        print(f"{ex}")


def add_maintenance_usecase(maintenance_details):
    try:
        logging.info(f"{maintenance_details}")
        token=maintenance_details.get("token")

        ndid = utils.get_ndid(token)
        roomNumber=maintenance_details.get("roomNumber")
        hId=maintenance_details.get("hId")
        Message=maintenance_details.get("Message")
        end=maintenance_details.get("end")
        query = {"ndid": ndid, "hId": hId, "roomNumbers": {"$in": [roomNumber]}}
        rooms = db.Rooms.find_one(query)
        start=incrementDayByOne(maintenance_details.get("start"))
        if rooms:
            # Add maintenance information to the 'maintenance' array field
            new_maintenance = {
                "roomNumber": roomNumber,
                "Message": Message,
                "start": start,
                "end": end
            }
            
            # Add new maintenance information to the 'inMaintenace' array field
            update_data = {"$push": {"inMaintanance": new_maintenance}}
            db.Rooms.update_one(query, update_data)
            current_date = start
            while current_date!=end:
                add_inventory(hId,ndid,roomNumber,current_date)
                current_date=incrementDayByOne(current_date)
            add_inventory(hId,ndid,roomNumber,current_date)
            print("Maintenance information added successfully.")
            logging.info("True")
            return True,"Maintenance Added Succesfully"
        else:
            return False,"Error Occured"
    except Exception as ex:
        LOGGER.error("Unabel to get engine datas:{}".format(ex))
        logging.error(f"{ex}")
        return False, "Error Occured"



def update_maintenance_usecase(maintenance_details):
    try:
        logging.info(f"{maintenance_details}")
        token=maintenance_details.get("token")
        ndid=utils.get_ndid(token)
        # {"roomNumber":"101","Message":"Electricity","start":"2024-01-04","end":"2024-01-08"}
        hId=maintenance_details.get("hId")
        oldroomNumber=maintenance_details.get("oldroomNumber")
        newroomNumber=maintenance_details.get("newroomNumber")
        oldstart=incrementDayByOne(maintenance_details.get("oldstart"))
        newstart=incrementDayByOne(maintenance_details.get("newstart"))
        oldend=maintenance_details.get("oldend")
        newend=maintenance_details.get("newend")
        Message=maintenance_details.get("Message")
        #pop
        current_date=oldstart
        while current_date!=oldend:
            remove_inventory(hId, ndid, oldroomNumber,current_date)
            current_date=incrementDayByOne(current_date)
        remove_inventory(hId, ndid, oldroomNumber,current_date)
        current_date=newstart
        while current_date!=newend:
            add_inventory(hId, ndid, newroomNumber,current_date)
            current_date=incrementDayByOne(current_date)
        add_inventory(hId, ndid, newroomNumber,current_date)
        query = {"ndid": ndid, "hId": hId, "roomNumbers": {"$in": [oldroomNumber]}}
        db.Rooms.update_one(query,{"$pull": {"inMaintanance": {"roomNumber": oldroomNumber,"Message": Message,"start": oldstart,"end": oldend}}})
        #push
        query = {"ndid": ndid, "hId": hId, "roomNumbers": {"$in": [newroomNumber]}}
        new_maintenance = {
                "roomNumber": newroomNumber,
                "Message": Message,
                "start": newstart,
                "end": newend
        }
        # Add new maintenance information to the 'inMaintenace' array field
        update_data = {"$push": {"inMaintanance": new_maintenance}}
        db.Rooms.update_one(query, update_data)
        return True,"Maintenance Updated Succesfully"
    except Exception as ex:
        LOGGER.error("Unabel to get engine datas:{}".format(ex))
        logging.error(f"{ex}")
        return False, "Error Occured"
    

def remove_inventory(hId,ndid,roomNumber,current_date):
    try:
        query = {"ndid": ndid, "hId": hId, "roomNumbers": {"$in": [roomNumber]}}
        room = db.Rooms.find_one(query)

        if room:
            #increase inventory_status[current_date] by 1 and if equal to no_of_room then remove it from inventoryStatus
            inventory_status = room.get("inventoryStatus", {})
            no_of_rooms = int(room.get("noOfRooms", 0))
            current_value = int(inventory_status[current_date])
            inventory_status[current_date]=min(no_of_rooms,current_value+1)
            db.Rooms.update_one(query, {"$set": {"inventoryStatus": inventory_status}})
            print(f"Inventory updated for {current_date}: {inventory_status}")
        else:
            print("Room not found in the database")
    except Exception as ex:
        print("Error in removing inventory")

def delete_maintenance_usecase(maintenance_details):
    try:
        token=maintenance_details.get("token")
        ndid=utils.get_ndid(token)
        hId=maintenance_details.get("hId")
        start=maintenance_details.get("start")
        end=maintenance_details.get("end")
        Message=maintenance_details.get("Message")
        roomNumber=maintenance_details.get("roomNumber")
        query = {"ndid": ndid, "hId": hId, "roomNumbers": {"$in": [roomNumber]}}
        db.Rooms.update_one(query,{"$pull": {"inMaintanance": {"roomNumber": roomNumber,"Message": Message,"start": start,"end": end}}})
        currdate=start
        while currdate!=end:
            remove_inventory(hId,ndid,roomNumber,currdate)
            currdate=incrementDayByOne(currdate)
        remove_inventory(hId,ndid,roomNumber,currdate)
        return True,"Maintenace Deleted Successfully"    
    except Exception as ex:
        logging.error(f"{ex}")
        return False,"Maintenace Not Deleted"    
    


def update_booking_checkin_checkout_usecase(maintenance_details):
    try:
        logging.info(f"{maintenance_details}")
        token=maintenance_details.get("token")
        ndid=utils.get_ndid(token)
        booking_id=maintenance_details.get("bookingId")
        # {"roomNumber":"101","Message":"Electricity","start":"2024-01-04","end":"2024-01-08"}
        hId=maintenance_details.get("hId")
        oldroomNumber=maintenance_details.get("oldroomNumber")
        newroomNumber=maintenance_details.get("newroomNumber")
        oldstart=incrementDayByOne(maintenance_details.get("oldstart"))
        newstart=incrementDayByOne(maintenance_details.get("newstart"))
        oldend=maintenance_details.get("oldend")
        newend=maintenance_details.get("newend")
        db.Bookings.update_one(
            {"hId": hId, "ndid": ndid, "bookingId": booking_id},
            {"$pull": {"roomNumbers": oldroomNumber}}
        )
        
        db.Bookings.update_one(
            {"hId": hId, "ndid": ndid, "bookingId": booking_id},
            {"$push": {"roomNumbers": newroomNumber}}
        )
        
        db.Bookings.update_one(
            {"hId": hId, "ndid": ndid, "bookingId": booking_id},
            {"$set": {"checkIn": newstart, "checkOut": newend}}
        )
        price = {"Principal": 0, "Total": 0, "Tax": 0,"amountPay":0}
        bookingsinfo=db.Bookings.find_one({"hId":hId,"ndid":ndid,"bookingId":booking_id}).get("Bookings")
        prevtotalprice=db.Bookings.find_one({"hId":hId,"ndid":ndid,"bookingId":booking_id}).get("price")["Total"]
        price["amountPay"]=db.Bookings.find_one({"hId":hId,"ndid":ndid,"bookingId":booking_id}).get("price")["amountPay"]
        for ele in bookingsinfo:
            qty=ele["Qty"]
            if qty!=0:
                booking_details = {
                    "checkIn": newstart,
                    "checkOut": newend,
                    "roomType": ele['RoomType']
                }
                amount = booking_usecase.calculate_booking_total(
                    booking_details, ndid, hId)
                price["Principal"]+=qty*amount["Price"]
                price["Tax"]+=qty*amount["Tax"]
                price["Total"]+=qty*amount["TotalPrice"]
        print(price)
        db.Bookings.update_one({"hId": hId, "ndid": ndid, "bookingId": booking_id}, {"$set": {"price": price}})
        #refund advanced or nothing
        #advanced refunded cancelled success
        currentTotal=price["Total"]
        amountpaid=price["amountPay"]
        print("cuurentTotal :",currentTotal)
        print("amountpaid :",amountpaid )
        if currentTotal>prevtotalprice:
            print("ADVANCED")
            db.Bookings.update_one({"hId": hId, "ndid": ndid, "bookingId": booking_id}, {"$set": {"payment.Status": "ADVANCED"}})
        elif currentTotal==prevtotalprice:
            print("DONT DO ANYTHING")
        else:
            if amountpaid<currentTotal:
                print("ADVANCED")
                db.Bookings.update_one({"hId": hId, "ndid": ndid, "bookingId": booking_id}, {"$set": {"payment.Status": "ADVANCED"}})
            elif amountpaid>currentTotal:
                print("REFUND")
                db.Bookings.update_one({"hId": hId, "ndid": ndid, "bookingId": booking_id}, {"$set": {"payment.Status": "REFUND"}})
            else:
                db.Bookings.update_one({"hId": hId, "ndid": ndid, "bookingId": booking_id}, {"$set": {"payment.Status": "SUCCESS"}})
                print("SUCCESS")

        # 
        current_date=oldstart
        while current_date!=oldend:
            remove_inventory(hId, ndid, oldroomNumber,current_date)
            current_date=incrementDayByOne(current_date)
        remove_inventory(hId, ndid, oldroomNumber,current_date)
        current_date=newstart
        while current_date!=newend:
            add_inventory(hId, ndid, newroomNumber,current_date)
            current_date=incrementDayByOne(current_date)
        add_inventory(hId, ndid, newroomNumber,current_date)
                
        # 
        return True,"Maintenance Updated Succesfully"
    except Exception as ex:
        LOGGER.error("Unabel to get engine datas:{}".format(ex))
        logging.error(f"{ex}")
        return False, "Error Occured"
    