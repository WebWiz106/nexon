from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
import utils
import json
import pymongo
import settings
from bson import json_util
from usecases import eazotel_usecase, otas_usecase

eazotel_controller = Blueprint("eazotel", __name__)


from utils import db


@eazotel_controller.route("/hi")
def hello1():
    return {"Message": "Hi"}


@eazotel_controller.route("/getuser/<token>")
def getUserEazotel(token):
    try:
        ndid = utils.get_ndid(token)
        email = utils.get_email(token)
        admin, access = eazotel_usecase.get_users_info(ndid, email)
        profile, planName = eazotel_usecase.get_users_profile(ndid)
        data = eazotel_usecase.get_user_links(ndid)
        plan = eazotel_usecase.get_user_plan(planName)

        return jsonify(
            {
                "Status": True,
                "Admin": admin,
                "Data": json.loads(json_util.dumps(data)),
                "Profile": json.loads(json_util.dumps(profile)),
                "Plan": plan,
                "Access": access,
            }
        )
    except:
        return jsonify({"Status": False})


@eazotel_controller.route("/ceateuser", methods=["POST"])
def createUser():
    try:
        maintenance_details = request.get_json(force=True)
        if maintenance_details.get("register") == "true":
            # status, token, message = eazotel_usecase.register_user_eazotel(
            #     maintenance_details
            # )
            status, token, message = eazotel_usecase.test_register_user_eazotel(
                maintenance_details
            )
            return jsonify({"Status": status, "Message": message, "Token": token})
        else:
            status, token, message = eazotel_usecase.login_user_eazotel(
                maintenance_details
            )

            # print(status, message, token)
            return jsonify({"Status": status, "Message": message, "Token": token})
    except:
        return jsonify({"Status": False})


@eazotel_controller.route("/edit/password", methods=["POST"])
def editUser_password():
    try:
        maintenance_details = request.get_json(force=True)
        status, message = eazotel_usecase.updatepassword_user(maintenance_details)
        return jsonify({"Status": status, "Message": message})
    except:
        return jsonify({"Status": False})


@eazotel_controller.route("/createwebsite", methods=["POST"])
def createWebsiteEazotel():
    try:
        maintenance_details = request.get_json(force=True)

        # =======Domain Generate==========
        domain = eazotel_usecase.randomDomainName(maintenance_details.get("hotelName"))
        plandetail = db.Zucks_plans.find_one(
            {"planName": maintenance_details.get("planName")}
        )
        locationid = eazotel_usecase.createHotelId()
        ndid = utils.get_ndid(maintenance_details.get("Token"))

        # Check for website already exists with user
        try:
            isexists = db.Zucks_hotellinks.find_one({"ndid": ndid})
        except:
            isexists = None

        if isexists != None:
            return jsonify(
                {
                    "Status": False,
                    "Message": "You have already created wesbite with us.",
                }
            )

        else:
            website = "https://" + domain + ".eazotel.com"

            if plandetail.get("bookingEngine"):
                engineLink = (
                    "https://engine.eazotel.com?id=" + ndid + "&hid=" + locationid
                )
            else:
                engineLink = "None"
            status = True
            message = ""
            otas_usecase.otas_create_usecase(maintenance_details, ndid, locationid)
            # return jsonify({"status":"true"})
            if plandetail.get("website"):
                status1, message1 = eazotel_usecase.dataforwebsiteExtract(
                    maintenance_details, domain, locationid, ndid, engineLink
                )
                status = status or status1
                message = message1

            if plandetail.get("bookingEngine"):
                if plandetail.get("website"):
                    status1, message1 = (
                        eazotel_usecase.data_to_create_for_bookingengine(
                            ndid, locationid, maintenance_details
                        )
                    )
                    status = status or status1
                    message = message + " and " + message1
                    return jsonify(
                        {
                            "Status": status,
                            "Message": message,
                            "websiteLink": website,
                            "engineLink": engineLink,
                        }
                    )
                else:
                    status1, message1 = eazotel_usecase.createOnlyBookingEgnine(
                        maintenance_details, locationid, ndid, domain
                    )
                    status = status or status1
                    message = message1
                    return jsonify(
                        {"Status": status, "Message": message, "engineLink": engineLink}
                    )
            else:
                return jsonify(
                    {"Status": status, "Message": message, "websiteLink": website}
                )
    except:
        return jsonify(
            {"Status": False, "Message": "Website And Booking Engine Creation Failed"}
        )


@eazotel_controller.route("/createonlybooking", methods=["POST"])
def createBookingEngine():
    try:
        maintenance_details = request.get_json(force=True)
        domain = eazotel_usecase.randomDomainName(maintenance_details.get("hotelName"))
        locationid = eazotel_usecase.createHotelId()
        ndid = utils.get_ndid(maintenance_details.get("Token"))
        engineLink = ("https://engine.eazotel.com?id=" + ndid + "hid=" + locationid,)
        # website,bookhigenginer
        status, message = eazotel_usecase.createOnlyBookingEgnine(
            maintenance_details, locationid, ndid, domain
        )
        if status == False:
            return jsonify({"Status": False, "Message": message})
        return jsonify(
            {
                "Status": True,
                "Message": message,
                "engineLink": engineLink,
            }
        )
    except:
        return jsonify({"Status": False, "Message": "Booking Engine Not created"})


# for grm
def createGuestRequestManagement():
    return {}


@eazotel_controller.route("/updateDomain", methods=["POST"])
def updateDomain():
    try:
        maintenance_details = request.get_json(force=True)
        hId = maintenance_details.get("hId")
        ndid = utils.get_ndid(maintenance_details.get("token"))
        newDomain = maintenance_details.get("newDomain")
        status, message = eazotel_usecase.updateDomain(ndid, hId, newDomain)
        return jsonify({"Status": status, "Message": message})
    except:
        return jsonify({"Status": False, "Message": "Updation of domain failed"})


@eazotel_controller.route("/deletedata", methods=["POST"])
def deleteData():
    try:
        maintenance_details = request.get_json(force=True)
        hId = maintenance_details.get("hId")
        ndid = utils.get_ndid(maintenance_details.get("token"))
        status, message = eazotel_usecase.deleteData(ndid, hId)
        return jsonify({"Status": status, "Message": message})
    except Exception as ex:
        return jsonify({"Status": False, "Message": "Deletion Of Data Failed"})


@eazotel_controller.route("/get/templatenumber/<domain>", methods=["GET"])
def bringTemplateNumber(domain):
    try:
        status, template = eazotel_usecase.getdomainTemplatenumber(domain)
        return jsonify({"Status": status, "template": template})
    except:
        return jsonify({"Status": False, "Message": "Some Problem Occured"})


@eazotel_controller.route("/get/maintainstatus/<domain>", methods=["GET"])
def bringTemplateMaintain(domain):
    try:
        status, maintain = eazotel_usecase.getdomainMaintain(domain)
        return jsonify({"Status": status, "Maintain": maintain})
    except:
        return jsonify({"Status": False, "Message": "Some Problem Occured"})


@eazotel_controller.route("/updatetemplate", methods=["POST"])
def UpdateTemplateNumber():
    try:
        maintenance_details = request.get_json(force=True)
        status, message = eazotel_usecase.updatenumberoftemplate(maintenance_details)
        return jsonify({"Status": True, "Message": message})
    except:
        return jsonify(
            {"Status": False, "Message": "Updation of template Number Failed"}
        )


@eazotel_controller.route("/addColorCombForprev", methods=["POST"])
def addColorCombForprev():
    try:
        maintenance_details = request.get_json(force=True)
        status, message = eazotel_usecase.addColorCombination(maintenance_details)
        return jsonify({"Status": status, "Message": message})
    except:
        return jsonify({"Status": False, "Message": "Updation Failed"})


@eazotel_controller.route("/abhijeettesting", methods=["POST"])
def abhijeettesting():
    try:
        maintenance_details = request.get_json(force=True)
        locationid = ""
        ndid = ""
        status, message = otas_usecase.otas_create_usecase(
            maintenance_details, ndid, locationid
        )
        return jsonify({"Status": status, "Message": message})
    except:
        return jsonify(
            {"Status": False, "Message": "Website And Booking Engine Creation Failed"}
        )


@eazotel_controller.route("/changeTemplate", methods=["POST"])
def TemplateChangeClient():
    try:
        maintenance_details = request.get_json(force=True)
        data = eazotel_usecase.changetemplateofDomain(maintenance_details)
        return jsonify({"Status": data})
    except:
        return jsonify({"Status": False, "Message": "Failed"})


@eazotel_controller.route("/changeMaintenance", methods=["POST"])
def changeMaintenance():
    try:
        data = request.get_json(force=True)
        status = eazotel_usecase.changeMaintenance(data)
        return jsonify({"Status": status})
    except Exception as ex:
        return jsonify({"Status": False})


@eazotel_controller.route("/addEazotelClientQuery", methods=["POST"])
def addClientQUery():
    try:
        data = request.get_json(force=True)
        status = eazotel_usecase.addInClientQuery(data)
        return jsonify({"Status": status})
    except Exception as ex:
        return jsonify({"Status": False})


@eazotel_controller.route("/addcontacts", methods=["POST"])
def addContactsQueryfromclient():
    try:
        data = request.get_json(force=True)
        status = eazotel_usecase.addContactsAndMail(data)
        return jsonify({"Status": status})
    except Exception as ex:
        return jsonify({"Status": False})


@eazotel_controller.route("/get-all-contact-queries", methods=["GET"])
def get_all_contact_queries():
    try:
        bearer_token = request.headers.get("Authorization")
        token = bearer_token.split(" ")[1]
        status_filter = request.args.get("status")
        name = request.args.get("name")
        status, data, count = eazotel_usecase.get_contact_us_queries(
            token, status_filter, name
        )
        return jsonify({"Data": data, "Status": status, "Count": count})
    except Exception as ex:
        return jsonify({"Message": "Error fetching queries", "Status": False})


@eazotel_controller.route("/reply/addcontacts", methods=["POST"])
def ReplyContactsQuerytoclient():
    try:
        data = request.get_json(force=True)
        status = eazotel_usecase.ReplyContactsAndMail(data)
        return jsonify({"Status": status})
    except Exception as ex:
        return jsonify({"Status": False})


@eazotel_controller.route("/delete-contact-query", methods=["POST"])
def delete_contact_query():
    try:

        data = request.get_json(force=True)

        status, message = eazotel_usecase.delete_contact_queries(data)

        return jsonify({"Status": status, "Message": message})

    except Exception as ex:
        return jsonify({"Status": False})


@eazotel_controller.route("/edit-contact-query", methods=["POST"])
def edit_contact_query():
    # try:

    # Uncontacted , Mark as Contact, Converted

    data = request.get_json(force=True)

    status, message = eazotel_usecase.edit_status_contact_queries(data)
    return jsonify({"Status": status, "Message": message})


# except Exception as ex:
#     return jsonify({"Status": False})


@eazotel_controller.route("/update-all-query", methods=["GET"])
def update_all_docs():
    try:
        print("Updating all documents")
        status, msg = eazotel_usecase.update_master_data_add_checkin_and_checkout_date()
        return jsonify({"Status": status, "Message": msg})
        print("hkkdf")
    except Exception as ex:
        return jsonify({"Status": False, "Message": "Error updating documents"})
