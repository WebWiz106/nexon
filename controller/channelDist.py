import json
import settings
import razorpay
import utils
from bson import json_util

from usecases import otas_usecase
from flask import Blueprint, jsonify, request
from datetime import datetime, date, timedelta
import logging
channel_distribution = Blueprint('channelDist', __name__)


@channel_distribution.route("/hi")
def hi():
    return json.dumps({"mesage": "hi"})


@channel_distribution.route("/<token>/<hId>")
def getDistributionInformation(token,hId):
    try:
        details = otas_usecase.getOTAinformations(token,hId)
        return jsonify({"Status":True,"Details":json.loads(json_util.dumps(details))})
    except:
        return jsonify({"Status":False,"Details":{}})
