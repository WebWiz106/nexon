import json
import settings
import razorpay
import utils
from bson import json_util
from usecases import sports_usecase
from flask import Blueprint,jsonify, request
from datetime import datetime,date,timedelta

sports = Blueprint('sports', __name__)

@sports.route("/hi")
def hi():
    return json.dumps({"mesage":"hi"})



@sports.route("/checkenduser/number/<number>",methods=["GET"])
def checkUserwithNumber(number):
    try:
        status=sports_usecase.getEndUserDetailsfromNumber(number)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False}) 

@sports.route("/checkenduser/<token>",methods=["GET"])
def checkEnduserdata(token):
    try:
        status,isadmin=sports_usecase.getEndUserfromDatabase(token)
        return jsonify({"Status":status,"isAdmin":isadmin})
    except Exception as ex:
        return jsonify({"Status":False,"isAdmin":None})

@sports.route("/signupenduser",methods=["POST"])
def createEnduserdata():
    try:
        data=request.get_json(force=True)
        status=sports_usecase.addEndUserToDatabase(data)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})

@sports.route("/signinenduser",methods=["POST"])
def updateEnduserdata():
    try:
        data=request.get_json(force=True)
        status,token=sports_usecase.updateEndUserToDatabase(data)
        return jsonify({"Status":status,"Token":token})
    except Exception as ex:
        return jsonify({"Status":False,"Token":None})

@sports.route("/getprofile/hotel/<seid>",methods=["GET"])
def getProfileSeid(seid):
    try:
        data=sports_usecase.getProfileofUser(seid)
        return jsonify({"Status":True,"Details":json.loads(json_util.dumps(data))})
    except Exception as ex:
        return jsonify({"Status":False,"Details":None})
        


@sports.route("/getprofile/<id>",methods=["GET"])
def getprofile(id):
    try:
        data=sports_usecase.getProfileUser(id)
        return jsonify({"Status":True,"Details":json.loads(json_util.dumps(data))})
    except Exception as ex:
        return jsonify({"Status":False,"Details":None})

@sports.route("/createprofile",methods=["POST"])
def createProfileuser():
    try:
        data=request.get_json(force=True)
        status,message,token=sports_usecase.addProfile(data)
        return jsonify({"Status":status,"Message":message,"Token":token})
    except Exception as ex:
        return jsonify({"Status":False,"Message":None,"Token":None})
        

@sports.route("/logindashboard",methods=["POST"])
def LoginProfileuser():
    try:
        data=request.get_json(force=True)
        status,message,token,detail,userdetail=sports_usecase.LoginProfile(data)
        return jsonify({"Status":status,"Message":message,"Token":token,"Information":json.loads(json_util.dumps(detail)),"User":json.loads(json_util.dumps(userdetail))})
    except Exception as ex:
        return jsonify({"Status":False,"Message":None,"Token":None,"Information":None,"User":None})


@sports.route("/checkauthusertoken/<token>",methods=["GET"])
def TokenLoginDashboard(token):
    try:
        status,message,token,detail,userdetail=sports_usecase.LoginProfileWithDashboard(token)
        return jsonify({"Status":status,"Message":message,"Token":token,"Information":json.loads(json_util.dumps(detail)),"User":json.loads(json_util.dumps(userdetail))})
    except:
        return jsonify({"Status":False,"Message":"Server breaks"})


@sports.route("/updatePassword",methods=["POST"])
def UpdateProfileUser():
    try:
        data=request.get_json(force=True)
        status,message=sports_usecase.UpdateProfilePassword(data)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return jsonify({"Status":False,"Message":None})





@sports.route("/<token>",methods=["GET"])
def GetallUserDashboard(token):
    try:
        status,message=sports_usecase.allUsersDashboard(token)
        return jsonify({"Status":status,"Details":message})
    except Exception as ex:
        return jsonify({"Status":False,"Details":None})


@sports.route("/addnewuser/<token>",methods=["POST"])
def AddnewUserDashboard(token):
    try:
        data=request.get_json(force=True)
        status,message=sports_usecase.addProfileDashboard(data,token)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return jsonify({"Status":False,"Message":None})



@sports.route("/deleteuser/<token>",methods=["POST"])
def DeletenewUserDashboard(token):
    try:
        data=request.get_json(force=True)
        status,message=sports_usecase.deleteProfileDashboard(data,token)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return jsonify({"Status":False,"Message":None})



# Sports


@sports.route("/createBooking",methods=["POST"])
def sportBooking():
    data=request.get_json(force=True)
    status,orderId=sports_usecase.createBooking(data)
    if status:
        return jsonify({"Status":True,'orderId':orderId})
    return jsonify({"Status":False})


@sports.route("/getForDate/<date>/<sports>",methods=["GET"])
def getsportForBooking(date,sports):
    try:
        data=sports_usecase.getForDateAndSport(date,sports)
        if data!=None:
            return jsonify({"Status":True,"data":data})
        return jsonify({"Status":True,"data":{}})
    except Exception as ex:
        return jsonify({"Status":False,"data":{}})
    

#----------------------- DASHBOARD APIS --------------------------#



@sports.route("/createsport/<token>",methods=["POST"])
def createSport(token):
    try:
        data=request.get_json(force=True)
        status=sports_usecase.addSport(data,token)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})



@sports.route("/getSportsDashboard/<token>",methods=["GET"])
def getAllSportForDashboard(token):
    try:
        data=sports_usecase.getSportForDashboard(token)
        if data==None:
            return jsonify({"Status":False})
        return jsonify({"Status":True,"data":data})
    except Exception as ex:
        return jsonify({"Status":False})
    

@sports.route("/getTodayBooking/<token>",methods=["GET"])
def getTodayBooking(token):
    try:
        status,data=sports_usecase.getTodayBooking(token)
        return jsonify({"Status":status,"data":data})
    except Exception as ex:
        return jsonify({"Status":False})
    

@sports.route("/deleteSportsDashboard/<token>/<sportId>",methods=["DELETE"])
def deleteSport(token,sportId):
    try:
        status=sports_usecase.deleteSport(token,sportId)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})
    
@sports.route("/updateSportsDashboard/<token>/<sportId>",methods=["PUT"])
def updateSport(token,sportId):
    try:
        data=request.get_json(force=True)
        status=sports_usecase.updateSportDashboard(data,token,sportId)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})


   
@sports.route("/updateSlotsForDate/<token>/<sportName>",methods=["POST"])
def updateSlotsForDate(token,sportName):
    try:
        data=request.get_json(force=True)
        status=sports_usecase.updateSlotsForDateDashBoard(data,token,sportName)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})


# REMOVE THIS
@sports.route("/blockTurf/<token>",methods=["POST"])
def blockTurf(token):
    try:
        data=request.get_json(force=True)
        status=sports_usecase.blockTurf(data,token)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})





@sports.route("/blockTurfs",methods=["POST"])
def blockTurfs():
    try:
        data=request.get_json(force=True)
        status=sports_usecase.blockTurfs(data)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})


@sports.route("/holidayhandle/<token>",methods=["POST"])
def holidayhandle(token):
    try:
        data=request.get_json(force=True)
        status=sports_usecase.holidayhandle(token,data)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})



@sports.route("/getAllBlockedTurfs/<token>/<sportName>",methods=["GET"])
def getAllBlockedTurfs(token,sportName):
    try:
        status,data=sports_usecase.getAllBlockedTurfs(token,sportName)
        return jsonify({"Status":status,"data":data})
    except Exception as ex:
        return jsonify({"Status":status,"data":None})

@sports.route("/getAllBooking/<token>",methods=["GET"])
def getAllBookingDashBoard(token):
    try:
        print(token)
        date = request.args.get('date', None)
        print(date)
        data = sports_usecase.getAllBookingDashBoard(token,date=date)  
        return jsonify({"Status": True, "data": data})
    except Exception as ex:
        return jsonify({"Status":False})
    

@sports.route("/updateBooking",methods=["PUT"])
def updateBooking():
    try:
        data = request.get_json(force=True)
        res = sports_usecase.updateBookingDashBoard(data)  
        return jsonify({"Status": res})
    except Exception as ex:
        return jsonify({"Status":False})
    

@sports.route("/deleteBooking",methods=["POST"])
def DeleteBooking():
    try:
        data = request.get_json(force=True)
        res = sports_usecase.deleteBookingDashBoard(data)  
        return jsonify({"Status": res})
    except Exception as ex:
        return jsonify({"Status":False})


@sports.route("/updateBooking/razorpay",methods=["PUT"])
def updateBookingRazorpay():
    try:
        data = request.get_json(force=True)
        res,data = sports_usecase.updateBookingRazorpay(data)  
        return jsonify({"Status": res,"details":json.loads(json_util.dumps(data))})
    except Exception as ex:
        return jsonify({"Status":False})

   
@sports.route("/getSlotsForDate/<seid>/<date>",methods=["GET"])
def getAllSlotsForDate(seid,date):
    try:
        res = sports_usecase.getAllSlotsForDateDashBoard(seid,date)  
        return jsonify({"Status": True,"Data":res})
    except Exception as ex:
        return jsonify({"Status":False})

@sports.route("/getQRCode/<token>/<orderId>",methods=["GET"])
def getQRCode(token,orderId):
    try:
        res = sports_usecase.getQRCode(token,orderId)  
        return jsonify({"Status": True,"Data":res})
    except Exception as ex:
        return jsonify({"Status":False})

@sports.route("/makeBookingSuccess/<token>",methods=["POST"])
def makeBookingSuccess(token):
    try:
        data=request.get_json(force=True)
        res = sports_usecase.makeBookingSuccess(token,data)  
        return jsonify({"Status": res})
    except Exception as ex:
        return jsonify({"Status":False})



@sports.route("/changeStatusCheckInCheckOut/<token>/<sportBookingId>",methods=["PUT"])
def changeStatus(token,sportBookingId):
    try:
        data=request.get_json(force=True)
        res = sports_usecase.changeStatusBookingId(token,sportBookingId,data)  
        return jsonify({"Status": res})
    except Exception as ex:
        return jsonify({"Status":False})





@sports.route("/updateBookingDashboard/<token>",methods=["PUT"])
def updateBookingDashboard(token):
    try:
        data = request.get_json(force=True)
        res = sports_usecase.updateBookingDashBoardDashboard(token,data)  
        return jsonify({"Status": res})
    except Exception as ex:
        return jsonify({"Status":False})


@sports.route("/getAllBookingMonth/<token>",methods=["GET"])
def getAllBookingDashBoardMonth(token):
    try:
        data = sports_usecase.getAllBookingMonthDashBoard(token)  
        return jsonify({"Status": True, "data": data})
    except Exception as ex:
        return jsonify({"Status":False})
    


@sports.route("/getAllBookingPaymentStatus/<token>/<status>",methods=["GET"])
def getAllBookingPaymentStatus(token,status):
    try:
        data = sports_usecase.getAllBookingPaymentStatus(token,status)  
        return jsonify({"Status": True, "data": data})
    except Exception as ex:
        return jsonify({"Status":False})
 

@sports.route("/getAllBookingDateRange/<token>",methods=["POST"])
def getAllBookingDateRange(token):
    try:
        data=request.get_json(force=True)
        data = sports_usecase.getAllBookingDateRange(token,data)  
        return jsonify({"Status": True, "data": data})
    except Exception as ex:
        return jsonify({"Status":False})


@sports.route("/getParticularBooking/<token>",methods=["POST"])
def getParticularBooking(token):
    try:
        data=request.get_json(force=True)
        sportBookingId=data.get("sportBookingId")
        data = sports_usecase.getParticularBooking(token,sportBookingId)  
        if data==None:
            return jsonify({"Status":False})
        return jsonify({"Status": True, "data": data})
    except Exception as ex:
        return jsonify({"Status":False})


@sports.route("/addCustomPrice/<token>",methods=["POST"])
def addCustomPrice(token):
    try:
        data=request.get_json(force=True)
        status,message = sports_usecase.addCustomPrice(token,data)  
        return jsonify({"Status": status, "message": message})
    except Exception as ex:
        return jsonify({"Status":False,"message":"some error occured"})


@sports.route("/addCustomPriceDayBasis/<token>",methods=["POST"])
def addCustomPriceDayBasis(token):
    try:
        data=request.get_json(force=True)
        status,message = sports_usecase.addCustomPriceDayBasis(token,data)  
        return jsonify({"Status": status, "message": message})
    except Exception as ex:
        return jsonify({"Status":False,"message":"some error occured"})


@sports.route("/bulkUpdatePrice/<token>",methods=["PUT"])
def bulkUpdatePrice(token):
    try:
        data=request.get_json(force=True)
        status,message = sports_usecase.bulkUpdatePrice(token,data)  
        return jsonify({"Status": status, "message": message})
    except Exception as ex:
        return jsonify({"Status":False,"message":"some error occured"})


@sports.route("/getEightPrevAfter/<token>",methods=["POST"])
def getEightPrevAfter(token):
    try:
        data=request.get_json(force=True)
        data=sports_usecase.getEightPrevAfter(token,data)
        return jsonify({"Status":True,"data":data})
    except Exception as ex:
        return jsonify({"Status":False,"data":None})
    



#--------------------------- WEBSITE APIS ---------------------------#
# !WORK NEEDED
@sports.route("/getSportsWebsite/<seid>",methods=["GET"])
def getAllSportForWebsite(seid):
    try:
        data=sports_usecase.getSportForWebsite(seid)
        if data==None:
            return jsonify({"Status":False})
        return jsonify({"Status":True,"data":data})
    except Exception as ex:
        return jsonify({"Status":False,"data":None})
    

@sports.route("/getParticularSlot/<seid>/<sportId>/<querydate>",methods=["GET"])
def getparticularSlot(seid,sportId,querydate):
    try:
        data=sports_usecase.getParticularSlot(seid,sportId,querydate)
        if data!=None:
            return jsonify({"Status":True,"data":data})
        return jsonify({"Status":False,"Data":None})
    except Exception as ex:
        return jsonify({"Status":False,"Data":None})


@sports.route("/getAllUsersSports/<token>",methods=["GET"])
def getAllUsers(token):
    try:
        status,data=sports_usecase.getAllUsers(token)
        return jsonify({"Status":status,"Data":data})
    except Exception as ex:
        return jsonify({"Status":False,"Data":None})



@sports.route("/countervalue",methods=["POST"])
def counterValue():
    try:
        body=request.get_json(force=True)
        status,data=sports_usecase.CounterValue(body)
        return jsonify({"Status":status,"Data":data})
    except Exception as ex:
        return jsonify({"Status":status,"Data":None})



