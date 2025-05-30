import base64
import jsons
import requests
import shortuuid
import pymongo
import settings
from usecases import booking_usecase
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from utils import db
########################## HELPER FUNCTION ################################
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def calculate_sha256_string(input_string):
    # Create a hash object using the SHA-256 algorithm
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Update hash with the encoded string
    sha256.update(input_string.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return sha256.finalize().hex()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def base64_encode(input_dict):
    # Convert the dictionary to a JSON string
    json_data = jsons.dumps(input_dict)
    # Encode the JSON string to bytes
    data_bytes = json_data.encode('utf-8')
    # Perform Base64 encoding and return the result as a string
    return base64.b64encode(data_bytes).decode('utf-8')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def pay(data,merchantid,saltkey,hid,ndid):
    merchantid = merchantid
    SALTKEY = saltkey

    amount = int(data.get("amount"))*100
    print(amount)
    mobilenumber=data["guestInfo"].get("Phone")
    merchantTransactionId = shortuuid.uuid()
    print(merchantTransactionId)

    MAINPAYLOAD = {
        "merchantId": merchantid,
        "merchantTransactionId": merchantTransactionId,
        "merchantUserId": "MUID123",
        "amount": amount,
        "redirectUrl": "https://nexon.eazotel.com/phonepe/postpaymentredirect",
        "redirectMode": "POST",
        "callbackUrl": "https://nexon.eazotel.com/phonepe/postpaymentredirect",
        "mobileNumber": mobilenumber,
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SETTING
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    INDEX = "1"
    ENDPOINT = "/pg/v1/pay"
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    base64String = base64_encode(MAINPAYLOAD)
    mainString = base64String + ENDPOINT + SALTKEY
    sha256Val = calculate_sha256_string(mainString)
    checkSum = sha256Val + '###' + INDEX
    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # # Payload Send
    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checkSum,
        'accept': 'application/json',
    }
    json_data = {
        'request': base64String,
    }
    response = requests.post('https://api.phonepe.com/apis/hermes/pg/v1/pay', headers=headers, json=json_data)
    responseData = response.json()
    transaction_id = responseData["data"]["merchantTransactionId"]
    redirect_link = responseData["data"]["instrumentResponse"]["redirectInfo"]["url"]
    
    print(transaction_id)

    print(redirect_link)
    return transaction_id,redirect_link


def payment_post_return(form_data):
    print(form_data)
    data=db.Bookings.find_one({"payment.RefNo":form_data.get("transactionId")})
    hId=data.get("hId")
    ndid=data.get("ndid")
    type,merchantid,secretkey = booking_usecase.getGateways(ndid,hId)
    INDEX = "1"
    SALTKEY = secretkey
    merchantid = merchantid
    merchantTid = form_data.get('transactionId', None)
    print(merchantTid)
    if merchantTid:
        # request_url = 'https://api.phonepe.com/apis/hermes/pg/v1/status/'+merchantid+'/' + merchantTid
        # sha256_Pay_load_String = '/pg/v1/status/'+merchantid+'/' + merchantTid + SALTKEY
        # sha256_val = calculate_sha256_string(sha256_Pay_load_String)
        # checksum = sha256_val + '###' + INDEX
        # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # # Payload Send
        # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # headers = {
        #     'Content-Type': 'application/json',
        #     'X-VERIFY': checksum,
        #     'X-MERCHANT-ID': merchantTid,
        #     'accept': 'application/json',
        # }
        # response = requests.get(request_url, headers=headers)
        # #page_respond_data=form_data_dict, page_respond_data_varify=response.text
        # # print(response.json)
        # response=response.json()
        # print(response)
        if  form_data.get("code")=="PAYMENT_SUCCESS":
            my_dict={
                "ndid":ndid,
                "hId":hId,
                "orderid":form_data.get("transactionId"),
                "paymentid":form_data.get("providerReferenceId"),
                "Status":"SUCCESS" if data["price"]["amountPay"]==data["price"]["Total"] else "ADVANCED"
            }
            print(my_dict)
            if(data["payment"].get("Status")== "PENDING"):
                booking_usecase.update_booking(my_dict)
            
            data=db.Bookings.find_one({"hId":hId,"ndid":ndid,"payment.RefNo":my_dict.get("orderid"),"payment.payId":my_dict.get("paymentid")})
            bookingenginedata=db.BookingEngineData.find_one({"hId":hId,"ndid":ndid})
            logo=bookingenginedata.get("Details").get("Footer").get("Logo")
            hotelname=bookingenginedata.get("Details").get("HotelName")
            return True,data,logo,hotelname
    return False,None,None,None



def payment_return(form_data,saltkey,merchantid):
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SETTING
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    INDEX = "1"
    SALTKEY = saltkey
    merchantid = merchantid
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Access form data in a POST request
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Convert form data to a dictionary
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    transaction_id = form_data.get('transactionId', None)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 1.In the live please match the amount you get byamount you send also so that hacker can't pass static value.
    # 2.Don't take Marchent ID directly validate it with yoir Marchent ID
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if transaction_id:
        request_url = 'https://api.phonepe.com/apis/hermes/pg/v1/status/'+merchantid+'/' + transaction_id
        sha256_Pay_load_String = '/pg/v1/status/'+merchantid+'/' + transaction_id + SALTKEY
        sha256_val = calculate_sha256_string(sha256_Pay_load_String)
        checksum = sha256_val + '###' + INDEX
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Payload Send
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
            'X-MERCHANT-ID': transaction_id,
            'accept': 'application/json',
        }
        response = requests.get(request_url, headers=headers)
        #page_respond_data=form_data_dict, page_respond_data_varify=response.text
    return {'output': response.text}
