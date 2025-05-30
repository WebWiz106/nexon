import base64
import requests
from usecases import booking_usecase
import utils
import settings
import logging
import pymongo

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db


def create_headers(username, password):
    print(username, password)
    basic_auth = 'Basic ' + base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': basic_auth,
        # Optionally set other headers based on your needs
        'Content-Type': 'application/json',
        'Accept': 'application/json',  # Specify the expected response format
    }
    print("1")
    return headers

def edit_Gateway_dashboard(details):
    try:
        token = details.get("token")
        hId = details.get("hId")
        Type = details.get("type")
        API_KEY = details.get("API_KEY")
        SECRET_KEY = details.get("SECRET_KEY")

        ndid = utils.get_ndid(token)

        db.BookingEngineData.find_one_and_update({"ndid":ndid,"hId":hId},{"$set":{
            "Details.Gateway":{
                "Type":Type,
                "API_KEY":API_KEY,
                "SECRET_KEY":SECRET_KEY

            }
        }})


        return True, "Updated"
    except Exception as err:
        # Handle fetch error
        return False, "Not Updated"

def allPayment(details):
    try:
        token = details.get("token")
        ndid = utils.get_ndid(token)
        hid = details.get("hId")
        skip = details.get("skip")

        type,username,password = booking_usecase.getGateways(ndid,hid)
        headers = create_headers(username, password)
        if type=="Razorpay":
            # print(headers)
            razorpaylink = "https://api.razorpay.com/v1/payments?skip="+skip
            response = requests.get(razorpaylink, headers=headers)

            
            if "count" in response.json():
                return True, response.json()
            else:
                return False,{}
        else:
            # ONLY PHONE PE YET
            return True, {"count":0,"entity":"collection","items":[]}
    except Exception as err:
        # Handle fetch error
        return False, {}


def filterOrders(details):
    try:
        token = details.get("token")
        ndid = utils.get_ndid(token)
        hid = details.get("hId")
        orderid = details.get("orderid")

        type,username,password = booking_usecase.getGateways(ndid,hid)
        headers = create_headers(username, password)

        razorpaylink = "https://api.razorpay.com/v1/orders/"+orderid
        response = requests.get(razorpaylink, headers=headers)

        if "id" in response.json():
            return True, response.json()
        else:
            return False,{}
    except Exception as err:
        # Handle fetch error
        return False, {}


def filterPayments(details):
    try:
        token = details.get("token")
        ndid = utils.get_ndid(token)
        hid = details.get("hId")
        payid = details.get("payid")

        type,username,password = booking_usecase.getGateways(ndid,hid)
        headers = create_headers(username, password)

        razorpaylink = "https://api.razorpay.com/v1/payments/"+payid
        response = requests.get(razorpaylink, headers=headers)
        
        if "id" in response.json():
            return True, response.json()
        else:
            return False,{}
    except Exception as err:
        # Handle fetch error
        return False, {}


