from flask import Blueprint,request,jsonify
from usecases import leadmanagement_usecase
leadmanagement_controller = Blueprint('leadmanagement', __name__)

@leadmanagement_controller.route("/addSheetName",methods=["POST"])
def addSheetName():
    try:
        data=request.get_json(force=True)
        status,message=leadmanagement_usecase.addSheetname(data)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return jsonify({"Status":False,"Message":"Some Error Occured"})
    

@leadmanagement_controller.route("/getSheetName/<token>",methods=["GET"])
def getSheet(token):
    try:
        status,message=leadmanagement_usecase.getSheet(token)
        return jsonify({"Status":status,"data":message})
    except Exception as ex:
        return jsonify({"Status":False,"Message":"Some Error Occured"})
    


@leadmanagement_controller.route("/updategoogletokenleadmanagement",methods=["POST"])
def updateGoogleTokenLeadManagement():
    try:
        data=request.get_json(force=True)   
        googletoken=data["googleToken"]
        token=data["token"]
        status,message=leadmanagement_usecase.updateGoogleToken(googletoken,token)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return jsonify({"Status":False,"Message":"Some error Occured while updating google token"})
    
    
@leadmanagement_controller.route("/getSheetDetailLead/<token>/<sheetId>/<sheetName>",methods=["GET"])
def getSheetDetailLead(token,sheetId,sheetName):
    try:
        status,message=leadmanagement_usecase.getSheetDetailsforlead(sheetId,sheetName,token)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return jsonify({"Status":False,"Message":"Some error occured while fethcing sheet data"})



@leadmanagement_controller.route("/getsheetName/<spreadSheetId>/<token>")
def get_sheetName(spreadSheetId,token):
    try:
        print(spreadSheetId)
        status,data=leadmanagement_usecase.getAllSheetName(spreadSheetId,token)
        print(data)
        if status:
            return (jsonify(data))
        return jsonify({"Status":False,"Message":"Error occured while fetching sheet Names"})
    except Exception as ex:
        return jsonify({"Status":False,"Message":"Error occured while fetching sheet Names"})



@leadmanagement_controller.route("/getGoogltoken/<token>")
def getGoogleToken(token):
    try:
        status,data=leadmanagement_usecase.getGoogleToken(token)
        return jsonify({"Status":status,"Message":data})
    except Exception as ex:
        return jsonify({"Status":False,"Message":"None"})


@leadmanagement_controller.route("/updateSheet/<token>/<sheetId>/<sheetName>",methods=["PUT"])
def updateSheetController(token,sheetId,sheetName):
    data=request.get_json(force=True)   
    status=leadmanagement_usecase.updateSheetUsecase(token,sheetId,sheetName,data)
    return jsonify({"Status":status})