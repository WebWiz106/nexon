import requests
import logging

import gateway
import utils
import settings
import constants
import pymongo
from urllib.parse import quote

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db

def get_reviews(ndid):
    try:
        profile = gateway.get_profile(ndid)
        if profile:
            place_id = profile.get("Google")
            if place_id:
                url = constants.GOOGLE_BASE_URL + constants.GOOGLE_GET_REVIES
                params = {
                    'place_id': place_id,
                    'fields': 'reviews',
                    'key': settings.GOOGLE_API_KEY
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    reviews = data.get('result', {}).get('reviews', [])
                    details=[]
                    for review in reviews:
                        if(review.get('rating')>=3):
                            details.append(review)
                    return details
                else:
                    logging.INFO("Unable to hit", response)
            else:
                logging.INFO("No place id found")
        else:
            logging.INFO("Unable to get profile with the provided ndid")

        return []
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)
    
def get_reviews_domain(domain):
    try:
        pro = db.Zucks_profile.find_one({"domain":domain})
        profile = gateway.get_profile(pro.get("uId"))
        if profile:
            place_id = profile.get("Google")
            if place_id:
                url = constants.GOOGLE_BASE_URL + constants.GOOGLE_GET_REVIES
                params = {
                    'place_id': place_id,
                    'fields': 'reviews',
                    'key': settings.GOOGLE_API_KEY
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    reviews = data.get('result', {}).get('reviews', [])
                    details=[]
                    for review in reviews:
                        if(review.get('rating')>=3):
                            details.append(review)
                    return details
                else:
                    logging.INFO("Unable to hit", response)
            else:
                logging.INFO("No place id found")
        else:
            logging.INFO("Unable to get profile with the provided ndid")

        return []
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)

def getlighthousedata(data):
    api = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    parameters = {
        'url': quote(data.get("url")),
        "key": settings.GOOGLE_API_KEY,
    }
    print(parameters)
    query = f"{api}?"
    for key, value in parameters.items():
        query += f"{key}={value}&"
    response = requests.get(query)
    json_data = response.json()
    # return requests.get(query).json()
    obj={
        "First Contentful Paint":json_data["lighthouseResult"]["audits"]["first-contentful-paint"]["displayValue"],
        "Largest Contentful Paint":json_data["lighthouseResult"]["audits"]["largest-contentful-paint"]["displayValue"],
        "Speed Index":json_data["lighthouseResult"]["audits"]["speed-index"]["displayValue"],
        "Time To Interactive":json_data["lighthouseResult"]["audits"]["interactive"]["displayValue"],
        "First Meaningful Paint":json_data["lighthouseResult"]["audits"]["first-meaningful-paint"]["displayValue"],
        "Performance":json_data["lighthouseResult"]["categories"]["performance"]["score"],
        "cumulative-layout-shift":json_data["lighthouseResult"]["audits"]["cumulative-layout-shift"]["displayValue"]
    }
    return obj

