from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin

from usecases import bookingengineloginUsecase
# cms_controller = Blueprint('cms', __name__)
bookingEngineLogin_controller = Blueprint('bookingEngineLogin', __name__)


@bookingEngineLogin_controller.route("/hi")
def hello1():
    return {"Message":"Hi"}


#*CHECK TOKEN FOR USER IF USER EXISTS WITH SYSTEM OR NOT
@bookingEngineLogin_controller.route("/getuser/<ndid>/<hId>/<token>",methods=["GET"])
def EngineLoginCheck(ndid,hId,token):
    try:
        status=bookingengineloginUsecase.Check_User_Engine_Login(ndid,hId,token)
        return jsonify({"Status":status})
    except:
        return jsonify({"Status":False})



#*SINGUP API FOR USER TO SIGNUP TO SYSTEM WITH ONLY HOTELID AND NDID COMBINATIONS
#*LOGIN API FOR USER TO LOGIN TO SYSTEM WITH HOTELID AND NDID COMBINATIONS
@bookingEngineLogin_controller.route("/signup",methods=["POST"])
def EngineSignup():
    try:
        bodyData = request.get_json(force=True)
        if(bodyData.get("register")):
            status,message=bookingengineloginUsecase.register_User_Engine_Login(data=bodyData)
        else:
            status,message=bookingengineloginUsecase.login_User_Engine_Login(data=bodyData)
        return jsonify({"Status":status,"Message":message})
    except:
        return jsonify({"Status":False})
    


#*CHECK NUMBER FOR USER AND VALIDATE OTP AND CONFIRM IF VERIFIED
@bookingEngineLogin_controller.route("/otp-verify",methods=["POST"])
def VerifyOtpProcess():
    try:
        bodyData = request.get_json(force=True)
        status,token=bookingengineloginUsecase.checkotp_User_Engine_Login(data=bodyData)
        return jsonify({"Status":status,"Token":token})
    except:
        return jsonify({"Status":False})
        

@bookingEngineLogin_controller.route("/getPrevBookings/<ndid>/<hId>/<token>",methods=["GET"])
def getPrevBookings(ndid,hId,token):
    try:
        data=bookingengineloginUsecase.getPrevBookings(ndid,hId,token)
        return jsonify({"Status":True,"data":data})
    except:
        return jsonify({"Status":False})



@bookingEngineLogin_controller.route("/getFutureBookings/<ndid>/<hId>/<token>",methods=["GET"])
def getFutureBookings(ndid,hId,token):
    try:
        data=bookingengineloginUsecase.getFutureBooking(ndid,hId,token)
        return jsonify({"Status":True,"data":data})
    except:
        return jsonify({"Status":False})


@bookingEngineLogin_controller.route("/cancelBooking/<ndid>/<hId>/<token>/<bookingId>",methods=["POST"])
def cancelBookingByUser(ndid,hId,token,bookingId):
    try:
        data=bookingengineloginUsecase.cancelBookingByUser(ndid,hId,token,bookingId)
        return jsonify({"Status":data})
    except:
        return jsonify({"Status":False})
    

@bookingEngineLogin_controller.route("/getUserByPhoneNo/<token>",methods=["GET"])
def getUserByPhoneNo(token):
    try:
        data=bookingengineloginUsecase.getUserByPhoneNo(token)
        return jsonify({"Status":True,"user":data})
    except:
        return jsonify({"Status":False})