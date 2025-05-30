import json
import settings
import razorpay
import utils
from bson import json_util

from usecases import analytics_usecase
from flask import Blueprint, jsonify, request
from datetime import datetime, date, timedelta
import logging
analytics_controller = Blueprint('analytics', __name__)


@analytics_controller.route("/getinhouseandtodayoccup/<token>/<hId>")
def hello1(token,hId):
    try:
        status,data=analytics_usecase.inHouse_and_todayOccupied(token,hId)
        return jsonify({"status":status,"data":data})
    except Exception as ex:
        return jsonify({"status":False})