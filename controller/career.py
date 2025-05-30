import json
import logging
from bson import json_util
from flask import Blueprint, request, jsonify
from utils import db
from flask_cors import CORS, cross_origin
from usecases import career_usecase

career_controller = Blueprint("career", __name__)


@career_controller.route("/hi")
def hello():
    return json.dumps({"Message": "career page"})


@career_controller.route("/create", methods=["POST"])
def create_career():
    try:
        career_data = request.get_json(force=True)
        status, data = career_usecase.create_career(career_data)
        return jsonify({"Data": data, "Status": status})
    except Exception as ex:
        return (
            jsonify({"Message": "Error submitting application", "Status": False}),
            500,
        )


@career_controller.route("/get-applications", methods=["GET"])
def get_career():
    try:
        bearer_token = request.headers.get("Authorization")
        token = bearer_token.split(" ")[1]
        status, data = career_usecase.get_career(token)
        return jsonify({"Data": data, "Status": status}), 200
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "Error getting career", "Status": False}), 500
