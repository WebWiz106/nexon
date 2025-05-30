import json
import logging
from bson import json_util
from flask import Blueprint, request, jsonify
from usecases import admin_usecase,eazotel_usecase
from flask_cors import CORS, cross_origin


admin_controller = Blueprint('admin', __name__)


@admin_controller.route("/hi")
def hello():
    return json.dumps({"message": "hi"})

#* Login Admin
@admin_controller.route("/login",methods=["POST"])
def adminLogin():
    try:
        data = request.get_json(force=True)
        status,token,information = admin_usecase.login_super_admin(data)
        return jsonify({"Status":status,"Token":token,"Information":json.loads(json_util.dumps(information))})
    except:
        return jsonify({"Status":False})


#* Add Admin(Only Owners can add)
@admin_controller.route("/add/admin",methods=["POST"])
def adminAdd():
    try:
        data = request.get_json(force=True)
        status,message = admin_usecase.add_super_admin(data)
        return jsonify({"Status":status,"Message":message})
    except:
        return jsonify({"Status":False})
    
#* Edit Admin(Only Owners can add)
@admin_controller.route("/edit/admin",methods=["POST"])
def adminEdit():
    try:
        data = request.get_json(force=True)
        status,message = admin_usecase.edit_super_admin(data)
        return jsonify({"Status":status,"Message":message})
    except:
        return jsonify({"Status":False})
    

#* Delete Admin 
@admin_controller.route("/delete/admin",methods=["POST"])
def adminDelete():
    try:
        data = request.get_json(force=True)
        status,message = admin_usecase.delete_super_admin(data)
        return jsonify({"Status":status,"Message":message})
    except:
        return jsonify({"Status":False})
    

#*:- Get All Admins
@admin_controller.route("/<token>",methods=["GET"])
def getAllAdmins(token):
    try:
        status,data = admin_usecase.getAllAdmins_super_admin(token)
        return jsonify({"Status":status,"Admins":json.loads(json_util.dumps(data))})
    except:
        return jsonify({"Status":False})
    
    
#?????????????????????????Clients
#*:- Get All Clients
@admin_controller.route("/clients/<token>",methods=["GET"])
def getAllClients(token):
    try:
        status,message = admin_usecase.getAllClients_super_admin(token)
        return jsonify({"Status":status,"Clients":json.loads(json_util.dumps(message))})
    except:
        return jsonify({"Status":False})
    

#*:- Get All Clients-Website data
@admin_controller.route("/clients/websitedata/<token>",methods=["GET"])
def getAllClients_Websitedata(token):
    try:
        status,message,websitedata= admin_usecase.getAllClients_Websitedata_super_admin(token)
        return jsonify({"Status":status,"Message":message,"Websitedata":json.loads(json_util.dumps(websitedata))})
    except:
        return jsonify({"Status":False,"Message":"something went wrong"})
    


#*:- Get All OTADetails data
@admin_controller.route("/clients/OTADetails/<token>",methods=["GET"])
def getAllClients_OtaDetails(token):
    try:
        status,message,OTADetails= admin_usecase.getAllclient_OTADetails_super_admin(token)
        return jsonify({"Status":status,"Message":message,"Otadetails":json.loads(json_util.dumps(OTADetails))})
    except:
        return jsonify({"Status":False})
    

#*:- Fetch All users
@admin_controller.route("/clients/getallusers/<token>",methods=["GET"])
def getallusers(token):
    try:
        status,message,users = admin_usecase.getallUsers(token)
        return jsonify({"Status":status,"Message":message,"Users":json.loads(json_util.dumps(users))})
    except:
        return jsonify({"status":False,"Message":"Something went wrong"})
    

#*:-Get all details of analysis
@admin_controller.route("/clients/getallanalysis/<token>/<domain>",methods=["GET"])
def getallAnalysis(token,domain):
    try:
        status,message,details = admin_usecase.getDomainAnalysis(domain,token)
        return jsonify({"Status":status,"Message":message,"Details":details})
    except:
        return jsonify({"status":False,"Message":"Something went wrong"})   



#*:- Fetch Individual details
@admin_controller.route("/clients/getindividualdetail/<token>/<domain>",methods=["GET"])
def getIndividualDomainOtaDetail(token,domain):
    try:
        status,response,message = admin_usecase.OtadetailofDomain(domain,token)
        return jsonify({"Status":status,"Message":message,"Details":json.loads(json_util.dumps(response))})
    except:
        return jsonify({"status":False,"Message":"Something went wrong"})
    

@admin_controller.route("/getAllEazotelClientQuery/<token>",methods=["GET"])
def getAllClientQUery(token):
    try:
        status,data=admin_usecase.getALlClientQuery(token)
        return jsonify({"Status":status,"data":data})
    except Exception as ex:
        return jsonify({"Status":False})
    

@admin_controller.route("/editEazotelClientQuery/<token>",methods=["POST"])
def editClientQUery(token):
    try:
        data = request.get_json(force=True)
        status=admin_usecase.editClientQuery(data,token)
        return jsonify({"Status":status})
    except Exception as ex:
        return jsonify({"Status":False})