import json
import logging
from bson import json_util
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from usecases import user_usecase
import utils

user_controller = Blueprint("users", __name__)


@user_controller.route("/hi")
def hello():
    return json.dumps({"message": "hi"})


@user_controller.route("/<token>", methods=["GET"])
def get_all_user(token):
    try:
        user_list = user_usecase.get_all_user(token)
        return jsonify({"data": json.loads(json_util.dumps(user_list)), "Status": True})
    except Exception as ex:
        logging.error({""})
        return ({"Message": "{}".format(ex), "Status": False}), 500


@user_controller.route("/user-details", methods=["GET"])
def get_user_details():
    try:
        if "Authorization" in request.headers:
            bearer_token = request.headers.get("Authorization")
            token = bearer_token.split(" ")[1]
            user_email = utils.get_email(token)

            # print("fghjk", user_email) 
            user = user_usecase.get_user(user_email)

            # print(user)
            if user:
                logging.info(f"User in /userdetails: {user}")
                response_data = {"Status": True, "User": user}
                return jsonify(response_data), 200

            # logging.error(f"User does not exist with this email id")
            return (
                {
                    "Message": "No User exist with this email id",
                    "Status": False,
                }
            ), 200

        else:
            return {"Status": False, "Message": "Token not found"}, 401    
         
    except Exception as ex:
        logging.error(f"Error occured in /user-details")
        return (
            {
                "Message": "{}".format(ex),
                "Status": False,
            }
        ), 500


# @user_controller.route("/userdetails", methods=["POST"])
# def get_user():
    try:
        content = request.get_json(force=True)
        email = content.get("emailId")
        user = user_usecase.get_user(email)
        if user:
            logging.info(f"User in /userdetails: {user}")
            response_data = {"Status": True, "User": user}
            return jsonify(response_data), 200

        logging.error(f"User does not exist with this email id")
        return (
            {
                "Message": "No User exist with this email id",
                "Status": False,
            }
        ), 200
    except Exception as ex:
        logging.error(f"Error occured in /userdetails")
        return (
            {
                "Message": "{}".format(ex),
                "Status": False,
            }
        ), 500


@user_controller.route("/create/<token>", methods=["POST"])
def create_user(token):
    try:
        content = request.get_json(force=True)
        logging.info(f"{content}")

        # print("hdkfsd", content)
        # result = user_usecase.add_user(content, token)
        result = user_usecase.test_add_user(content, token)

        if result["Status"]:
            return jsonify({"Message": result["Message"], "Status": True}), 201
        else:
            return jsonify({"Message": result["Message"], "Status": False}), 400
    except Exception as ex:
        logging.error(f"{ex}")
        return jsonify({"Message": "{}".format(ex), "Status": False}), 500


@user_controller.route("/edit/<token>", methods=["POST"])
def edit_user(token):
    try:
        content = request.get_json(force=True)
        # print(content)
        message = user_usecase.test_edit_user(content, token)
        logging.info(f"{content}")
        return jsonify({"Message": message, "Status": True}), 201
        # return {}
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex), "Status": False}), 500


@user_controller.route("/delete/<email>", methods=["POST"])
def delete_user(email):
    try:
        message = user_usecase.delete_user(email)
        logging.info(f"{email} deleted")
        return jsonify({"Message": message, "Status": True}), 201
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex), "Status": False}), 500


@user_controller.route("/websitedata/<ndid>", methods=["GET"])
def websiteData(ndid):
    try:
        data = user_usecase.getWebsiteData(ndid)
        return jsonify({"Details": data}), 201
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "{}".format(ex)}), 500
