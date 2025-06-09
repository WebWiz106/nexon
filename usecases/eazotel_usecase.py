import utils
import constants
import pymongo
import json
import string
import settings
import logging
import uuid
import requests
import hashlib
from bs4 import BeautifulSoup
from bson import ObjectId
import urllib.request
import os
from urllib.parse import urljoin
import math
from bson import json_util
from usecases import mail_usecase
from pathlib import Path
import re
import base64
from bson.binary import Binary
import shortuuid
import random
from usecases import mail_usecase
from datetime import datetime, date, timedelta, timezone
from usecases import room_usecase

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

from utils import db


def getGoogleEmbeddedCode(maintain_data):
    hotel_name = maintain_data.get("hotelName", "")
    hotel_address = maintain_data.get("hotelAddress", "")
    hotel_state = maintain_data.get("hotelState", "")
    hotel_city = maintain_data.get("hotelCity", "")
    hotel_country = maintain_data.get("hotelCountry", "")

    # URL encode the values to handle spaces
    encoded_hotel_name = urllib.parse.quote(hotel_name)
    encoded_hotel_address = urllib.parse.quote(hotel_address)
    encoded_hotel_state = urllib.parse.quote(hotel_state)
    encoded_hotel_city = urllib.parse.quote(hotel_city)
    encoded_hotel_country = urllib.parse.quote(hotel_country)

    return f"https://www.google.com/maps/embed/v1/place?key={settings.GOOGLE_API_KEY}&q={encoded_hotel_name}+{encoded_hotel_address}+{encoded_hotel_state}+{encoded_hotel_city}+{encoded_hotel_country}"


banner_heading = [
    "Exquisite Comfort at",
    "Unparalleled Tranquility at",
    "Opulent Living at",
    "Where Luxury Meets Hospitality at",
    "Exclusive Accommodation at",
    "Timeless Elegance at",
    "Elevated Hospitality at",
    "Heavenly Comfort Awaits at",
    "Unforgettable Stays at",
    "Sophisticated Living at",
    "Unrivaled Luxury at",
    "Impeccable Hospitality at",
    "Where Every Guest is Royalty at",
    "Elegant Lodgings at",
    "Indulgent Escapes at",
    "Luxe Living at",
    "Where Luxury Knows No Bounds at",
    "Exemplary Hospitality",
    "Unmatched Comfort and Style at",
]

about = [
    "Nestled in the heart of [hotelCity], [hotelName] stands as a beacon of luxury and refinement, offering discerning travelers a haven of unparalleled sophistication. From the moment you step through our doors, you're greeted by an ambiance that seamlessly blends timeless elegance with contemporary allure. Each facet of [hotelName], from our meticulously appointed rooms to our world-class amenities, is designed to exceed the expectations of even the most discerning guests. Indulge in the epitome of relaxation at our exclusive spa, where skilled therapists transport you to a realm of serenity with an array of rejuvenating treatments. Meanwhile, our culinary offerings tantalize the palate with a fusion of global flavors, crafted with the freshest local ingredients and presented with impeccable artistry. At [hotelName], we invite you to immerse yourself in a world of refined luxury, where every moment is crafted to inspire and delight.",
    "Experience the vibrant pulse of [hotelCity] from the unparalleled comfort of [hotelName]. Situated amidst the bustling energy of the city, our hotel offers a retreat like no other, where guests can immerse themselves in the cultural richness and dynamic spirit of their surroundings. Whether you're exploring the historic landmarks that dot the cityscape or indulging in a shopping spree at nearby boutiques, [hotelName] serves as your luxurious home base, providing a sanctuary of tranquility amidst the urban hustle. After a day of adventure, unwind in the elegant comfort of our well-appointed accommodations, where every detail is meticulously curated to ensure a restful stay. From our attentive concierge service to our array of bespoke amenities, we strive to elevate your experience at every turn, creating memories that linger long after your departure.",
    "Discover the epitome of luxury and hospitality at [hotelName], a beacon of elegance in the heart of [hotelCity]. Boasting an unrivaled location, exquisite accommodations, and unparalleled service, our hotel offers discerning travelers an unforgettable experience from the moment they arrive. Step into our opulent lobby and be transported to a world of refined indulgence, where every detail is meticulously curated to exceed your expectations. Whether you're unwinding in one of our sumptuously appointed guest rooms, indulging in a gourmet meal at our acclaimed restaurant, or pampering yourself with a rejuvenating spa treatment, [hotelName] promises a stay that is nothing short of extraordinary. From business travelers seeking a sophisticated retreat to leisure guests looking to immerse themselves in the vibrant energy of [hotelCity], our hotel caters to every need with unparalleled grace and style.",
    "At [hotelName], located in the heart of [hotelCity], we redefine the notion of luxury with our unwavering commitment to personalized service and attention to detail. Our dedicated team of hospitality professionals stands ready to anticipate your every need, ensuring that your stay with us is nothing short of perfection. Whether you're visiting for business or pleasure, our goal is to exceed your expectations at every turn, leaving you with cherished memories that linger long after your departure.",
    "Immerse yourself in the rich tapestry of [hotelCity] while staying at [hotelName], where our prime location offers unparalleled access to the city's most iconic landmarks and attractions. From strolling through historic neighborhoods to sampling local delicacies at bustling markets, the possibilities for exploration are endless. And when it's time to retreat from the hustle and bustle of the city, [hotelName] welcomes you back with open arms, offering a serene oasis where you can recharge and rejuvenate in utmost comfort and style.",
    "Indulge in the ultimate culinary experience at [hotelName], where our world-class restaurants showcase the finest in local and international cuisine. From innovative fusion dishes to classic favorites reimagined with a modern twist, our talented chefs tantalize your taste buds with every bite. Pair your meal with a selection from our extensive wine list or signature cocktails crafted by our skilled mixologists, and elevate your dining experience to new heights. Whether you're savoring a leisurely breakfast overlooking the city skyline or enjoying a romantic dinner under the stars, dining at [hotelName] is an experience to remember.",
    "At [hotelName], we believe that true luxury lies in the details. From the plush linens adorning your bed to the carefully curated artwork that graces our walls, every element of your stay is designed to evoke a sense of indulgence and sophistication. Our commitment to excellence extends to every corner of our property, ensuring that each moment spent with us is infused with elegance and charm.",
    "Step into our sanctuary of serenity at [hotelName], where our tranquil spa offers a blissful escape from the stresses of everyday life. Let our expert therapists pamper you with a range of holistic treatments and therapies, each designed to restore balance and harmony to your mind, body, and soul. Whether you opt for a soothing massage, a rejuvenating facial, or a blissful body wrap, you'll emerge feeling refreshed, rejuvenated, and ready to take on the world.",
    "Experience the height of indulgence with our exclusive suite accommodations at [hotelName]. From expansive living areas and private balconies to luxurious amenities and personalized service, our suites offer a sanctuary of comfort and refinement unlike any other. Whether you're traveling for business or pleasure, our suites provide the perfect retreat, where you can unwind in style and immerse yourself in unparalleled luxury.",
    "Embark on a culinary journey like no other at [hotelName], where our diverse dining options cater to every palate and preference. Start your day with a hearty breakfast buffet featuring an array of international delicacies, or enjoy a leisurely lunch by the pool with fresh salads and grilled specialties. In the evening, savor the flavors of the Mediterranean at our signature restaurant, where expertly crafted dishes and a carefully curated wine list promise an unforgettable dining experience.",
    "Unwind in style at our rooftop bar, where panoramic views of the city skyline provide the perfect backdrop for an evening of relaxation and revelry. Sip on handcrafted cocktails crafted by our skilled mixologists as you soak in the ambiance, or sample a selection of premium spirits and wines from around the world. With live music and a vibrant atmosphere, our rooftop bar is the ideal spot to toast to life's special moments and create memories that last a lifetime.",
    "At [hotelName], we understand that travel is about more than just a destination – it's about the journey. That's why we go above and beyond to create experiences that inspire and delight, from personalized welcome amenities to curated local experiences that showcase the best of [hotelCity]. Whether you're exploring the city's vibrant arts scene or embarking on a culinary adventure through its bustling markets, we're here to help you make the most of your time with us and create memories that last a lifetime.",
    "Elevate your stay with our array of personalized services and amenities at [hotelName]. From valet parking and luggage assistance to 24-hour room service and turndown service, our dedicated team is on hand to ensure that your every need is met with the utmost care and attention. Whether you're celebrating a special occasion or simply seeking a relaxing getaway, we're here to make your stay with us truly unforgettable.",
]


# Register -> website + Booking -> Only Booking engine


def test_register_user_eazotel(maintenance_details):
    emailId = maintenance_details.get("emailId")
    userName = maintenance_details.get("userName")
    accesskey = maintenance_details.get("accesskey")
    password = hashlib.sha256(accesskey.encode("utf-8")).hexdigest()
    accessScope = {
        "cms": True,
        "bookingEngine": True,
        "socialMedia": True,
        "reservationDesk": True,
        "frontDesk": True,
        "channelManager": True,
        "seoManager": True,
        "foodManager": True,
        "themes": True,
        "gatewayManager": True,
        "humanResourceManagement": True,
        "guestRequestManagement": True,
        "enquiriesManagement": True,
    }

    users = db.Zucks_users.find_one({"emailId": emailId, "accesskey": password})
    if users == None:
        data = {"Email": emailId}

        token = utils.create(data)
        ndid = str(uuid.uuid4())
        db.Zucks_users.insert_one(
            {
                "emailId": emailId,
                "ndid": ndid,
                "displayName": userName,
                "userName": userName,
                "accesskey": password,
                "role": "superadmin",
                "isAdmin": True,
                "accessScope": accessScope,
                "createdAt": str(datetime.now()),
            }
        )
        return True, token, "Registered Successfully"

    else:
        token = "-"
        return False, token, "User Already Registered"


# def register_user_eazotel(maintenance_details):
#     emailId = maintenance_details.get("emailId")
#     userName = maintenance_details.get("userName")
#     accesskey = maintenance_details.get("accesskey")
#     password = hashlib.sha256(accesskey.encode("utf-8")).hexdigest()
#     accessScope = {
#         "cms": True,
#         "bookingEngine": True,
#         "socialMedia": True,
#         "reservationDesk": True,
#         "frontDesk": True,
#         "channelManager": True,
#         "seoManager": True,
#         "foodManager": True,
#         "themes": True,
#         "gatewayManager": True,
#     }

#     users = db.Zucks_users.find_one({"emailId": emailId, "accesskey": password})
#     if users == None:
#         data = {"Email": emailId}

#         token = utils.create(data)
#         ndid = str(uuid.uuid4())
#         db.Zucks_users.insert_one(
#             {
#                 "emailId": emailId,
#                 "ndid": ndid,
#                 "displayName": userName,
#                 "userName": userName,
#                 "accesskey": password,
#                 "isAdmin": True,
#                 "accessScope": accessScope,
#                 "createdAt": str(datetime.now()),
#             }
#         )
#         return True, token, "Registered Successfully"

#     else:
#         token = "-"
#         return False, token, "User Already Registered"


def login_user_eazotel(maintenance_details):
    try:
        username = maintenance_details.get("emailId")
        password = maintenance_details.get("accesskey")
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        users = db.Zucks_users.find_one({"emailId": username, "accesskey": password})
        # print(users)

        if users != None:
            data = {"Email": username}
            # print(data)

            token = utils.create(data)
            # print(token)
            return True, token, "Login Successfully"

        else:
            token = "-"
            return False, token, "Invalid Combinations"

    except:
        token = "-"
        return False, token, "Invalid Combinations"


def updatepassword_user(maintenance_details):
    token = maintenance_details.get("token")
    emailid = utils.get_email(token)

    oldpass = maintenance_details.get("oldAccessId")
    newpass = maintenance_details.get("newAccessId")

    oldpass = hashlib.sha256(oldpass.encode("utf-8")).hexdigest()
    newpass = hashlib.sha256(newpass.encode("utf-8")).hexdigest()

    users = db.Zucks_users.find_one({"emailId": emailid, "accesskey": oldpass})
    if users != None:
        db.Zucks_users.find_one_and_update(
            {"emailId": emailid, "accesskey": oldpass}, {"$set": {"accesskey": newpass}}
        )

        return True, "Password Changed Successfully"

    else:
        return False, "Invalid Combination"


def get_users_info(ndid, email):
    user = db.Zucks_users.find_one({"ndid": ndid})
    return user.get("isAdmin"), user.get("accessScope")


def get_users_profile(ndid):
    try:
        profile = db.Zucks_profile.find_one({"uId": ndid})
        return profile, profile["plan"].get("name")
    except:
        return {}, {}


def get_user_links(ndid):
    try:
        data = db.Zucks_hotellinks.find_one({"ndid": ndid})
        return data
    except:
        return {}


def get_user_plan(name):
    try:
        data = db.Zucks_plans.find_one({"planName": name})
        return data.get("planfeatures")
    except:
        return {}


def randomDigits():
    lower_bound = 10 ** (8 - 1)
    upper_bound = 10**8 - 1
    return random.randint(lower_bound, upper_bound)


def randomDomainName(HotelName):
    randomeDomain = "".join(HotelName.split(" "))
    randomeDomain = randomeDomain.lower()
    print(randomeDomain)
    try:
        existsCheck = db.WebsiteData.find_one({"Domain": randomeDomain})
    except:
        existsCheck = None

    if existsCheck != None:
        digit = randomDigits()
        domain = randomeDomain + str(digit)
        domain = domain.lower()
    else:
        domain = randomeDomain

    return domain


def createHotelId():
    lower_bound = 10 ** (8 - 1)
    upper_bound = 10**8 - 1
    return str(random.randint(lower_bound, upper_bound))


def createimage(category, img_count):
    return [
        "https://images.unsplash.com/photo-1701566352550-98f803b3c675?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1627750673161-02af15c7c722?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1570560258879-af7f8e1447ac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1462539405390-d0bdb635c7d1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1662982693758-f69fcb81e7d2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1698254855636-c14c68945a17?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1505275350441-83dcda8eeef5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1698389213387-999b528dde86?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1658387574197-74efe5041d4c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1479044769763-c28e05b5baa5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1695094411862-0e047fbddcb1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1657456322310-8dd2ac05e6ba?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1619676907714-0b9d46a0e764?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1668353750392-fa92b3dbb6de?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1554774853-5fb9f93ff5e7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1533540499377-cf2dec26c3d7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1701566688193-138f26394b07?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1701567428465-4fe0848022ed?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1525610553991-2bede1a236e2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1706438229836-98f3720dbfc6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1629349931327-b9880d7f5bc9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1651376589993-e0b37872f3e7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1559329007-40df8a9345d8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1615136611527-83067f351b23?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1662982692905-c1309625fa49?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1597106525363-7916ebf5b083?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1671663707612-c60dd5d7501b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1632766557709-696303805973?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
        "https://images.unsplash.com/photo-1700588084990-8913403426c5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjA3MDl8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MDkyODk0NzR8&ixlib=rb-4.0.3&q=80&w=1080",
    ]
    # access_key = "7F_cPoscQMU0orGyWlKTuqJKaxLXa_-EnAEbwotdMws"

    # # Set the keyword you want to search for
    # keyword = category

    # # Set the number of images you want to retrieve
    # num_images = img_count

    # # Make a request to the Unsplash API to search for images
    # url = f"https://api.unsplash.com/photos/random"
    # params = {
    #     "query": keyword,
    #     "count": num_images,
    #     "client_id": access_key
    # }
    # response = requests.get(url, params=params)
    # arr=[]
    # # Check if the request was successful
    # if response.status_code == 200:
    #     # Parse the JSON response
    #     images = response.json()

    #     # Print the URLs of the images
    #     for i, image in enumerate(images):
    #         image_url = image["urls"]["regular"]
    #         arr.append(image_url)
    #         # print(f"Image {i + 1} URL: {image_url}")
    #     return arr
    # else:
    #     print(f"Failed to retrieve images. Status code: {response.status_code}")


def createvideo(category, img_count):
    return [
        "https://player.vimeo.com/external/404899265.sd.mp4?s=6c82fd45ab3c75523b630b363b4aa3327dd3b579&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.hd.mp4?s=8780713219a8cf3996a8383d95b90d25e161ba7a&profile_id=171&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.hd.mp4?s=8780713219a8cf3996a8383d95b90d25e161ba7a&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.hd.mp4?s=8780713219a8cf3996a8383d95b90d25e161ba7a&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.sd.mp4?s=6c82fd45ab3c75523b630b363b4aa3327dd3b579&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.hd.mp4?s=8780713219a8cf3996a8383d95b90d25e161ba7a&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.sd.mp4?s=6c82fd45ab3c75523b630b363b4aa3327dd3b579&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.hd.mp4?s=8780713219a8cf3996a8383d95b90d25e161ba7a&profile_id=173&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.hd.mp4?s=8780713219a8cf3996a8383d95b90d25e161ba7a&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/404899265.hd.mp4?s=8780713219a8cf3996a8383d95b90d25e161ba7a&profile_id=169&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961390.hd.mp4?s=06808316fcd352fae0618103b8014ff86025554d&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961390.sd.mp4?s=ccf3897d8484e3e02e041f418cc18d1c8f39d4df&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961390.sd.mp4?s=ccf3897d8484e3e02e041f418cc18d1c8f39d4df&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961390.hd.mp4?s=06808316fcd352fae0618103b8014ff86025554d&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961390.sd.mp4?s=ccf3897d8484e3e02e041f418cc18d1c8f39d4df&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961390.hd.mp4?s=06808316fcd352fae0618103b8014ff86025554d&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961390.hd.mp4?s=06808316fcd352fae0618103b8014ff86025554d&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/455703289.hd.mp4?s=d0fe668c136db6312be26a931ea09389c7f4b9cb&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/455703289.sd.mp4?s=ff75c85eb8c31c2f5821da04b0995d3d1b73b2ae&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/455703289.sd.mp4?s=ff75c85eb8c31c2f5821da04b0995d3d1b73b2ae&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/455703289.hd.mp4?s=d0fe668c136db6312be26a931ea09389c7f4b9cb&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/455703289.sd.mp4?s=ff75c85eb8c31c2f5821da04b0995d3d1b73b2ae&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/559960857.sd.mp4?s=9df9704445969827242d3984bad045738ea5a99b&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/559960857.hd.mp4?s=3bedf9dfb48fd100de76940ec75ac9ecc8f7bdd8&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/559960857.hd.mp4?s=3bedf9dfb48fd100de76940ec75ac9ecc8f7bdd8&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/559960857.sd.mp4?s=9df9704445969827242d3984bad045738ea5a99b&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962103.hd.mp4?s=756ed0e182076a58cadf12d7e30bdaedbdf1ccf9&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962103.sd.mp4?s=fce432f037327a633c1ff8ce7ec4ba03df8dfa6d&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962103.hd.mp4?s=756ed0e182076a58cadf12d7e30bdaedbdf1ccf9&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962103.hd.mp4?s=756ed0e182076a58cadf12d7e30bdaedbdf1ccf9&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962103.hd.mp4?s=756ed0e182076a58cadf12d7e30bdaedbdf1ccf9&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962103.sd.mp4?s=fce432f037327a633c1ff8ce7ec4ba03df8dfa6d&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962103.sd.mp4?s=fce432f037327a633c1ff8ce7ec4ba03df8dfa6d&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/449661269.hd.mp4?s=88faf1a6b3fc8de815f2e9c9cff8d1897ea22936&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/449661269.sd.mp4?s=689e32481a04a538088652bad2516ee773e53416&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/449661269.sd.mp4?s=689e32481a04a538088652bad2516ee773e53416&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/449661269.sd.mp4?s=689e32481a04a538088652bad2516ee773e53416&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/449661269.hd.mp4?s=88faf1a6b3fc8de815f2e9c9cff8d1897ea22936&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961773.sd.mp4?s=f0659d20d63d163531b66cf1f1616f819ee63454&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961773.sd.mp4?s=f0659d20d63d163531b66cf1f1616f819ee63454&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961773.hd.mp4?s=9522af7fbde10cc0956ffd9e4b8852c5a90bedad&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961773.hd.mp4?s=9522af7fbde10cc0956ffd9e4b8852c5a90bedad&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961773.sd.mp4?s=f0659d20d63d163531b66cf1f1616f819ee63454&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961773.hd.mp4?s=9522af7fbde10cc0956ffd9e4b8852c5a90bedad&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961773.hd.mp4?s=9522af7fbde10cc0956ffd9e4b8852c5a90bedad&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484719017.hd.mp4?s=9f7347954cfe939f0ab6a09d01d89b73c5eb8af6&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484719017.sd.mp4?s=53de0fbd06aca07e3a28a52a0ca7b9bc756735d0&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484719017.sd.mp4?s=53de0fbd06aca07e3a28a52a0ca7b9bc756735d0&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484719017.hd.mp4?s=9f7347954cfe939f0ab6a09d01d89b73c5eb8af6&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484719017.hd.mp4?s=9f7347954cfe939f0ab6a09d01d89b73c5eb8af6&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484719017.sd.mp4?s=53de0fbd06aca07e3a28a52a0ca7b9bc756735d0&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484719017.hd.mp4?s=9f7347954cfe939f0ab6a09d01d89b73c5eb8af6&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/474375103.hd.mp4?s=17b5710ab2e2d13065d43d65b196bedcd570c5f2&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/474375103.sd.mp4?s=28dddb040a2d5283a1b34ddd351ec4c0a404117b&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/474375103.hd.mp4?s=17b5710ab2e2d13065d43d65b196bedcd570c5f2&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/474375103.sd.mp4?s=28dddb040a2d5283a1b34ddd351ec4c0a404117b&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/474375103.sd.mp4?s=28dddb040a2d5283a1b34ddd351ec4c0a404117b&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452869553.hd.mp4?s=6f83bcb52cbfb918f57d60dfd55cddd3420e2c59&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452869553.sd.mp4?s=5afd0fab08c78360ee143865527b00e83b3231e3&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452869553.hd.mp4?s=6f83bcb52cbfb918f57d60dfd55cddd3420e2c59&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452869553.sd.mp4?s=5afd0fab08c78360ee143865527b00e83b3231e3&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452869553.sd.mp4?s=5afd0fab08c78360ee143865527b00e83b3231e3&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962128.hd.mp4?s=21c36978d0ab251217f97f481fe3bb840072498d&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962128.hd.mp4?s=21c36978d0ab251217f97f481fe3bb840072498d&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962128.sd.mp4?s=0458fe2f3476b1b1615c59ecc1b46126fa5c07ac&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962128.sd.mp4?s=0458fe2f3476b1b1615c59ecc1b46126fa5c07ac&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962128.hd.mp4?s=21c36978d0ab251217f97f481fe3bb840072498d&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962128.sd.mp4?s=0458fe2f3476b1b1615c59ecc1b46126fa5c07ac&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458962128.hd.mp4?s=21c36978d0ab251217f97f481fe3bb840072498d&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/377149197.sd.mp4?s=0923ca5f9f3ad9225159c0ad2d464cf89162d37e&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/377149197.hd.mp4?s=f2a08cba2074eff1c9743ae7748ceddec2ca5a2b&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/377149197.hd.mp4?s=f2a08cba2074eff1c9743ae7748ceddec2ca5a2b&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/377149197.sd.mp4?s=0923ca5f9f3ad9225159c0ad2d464cf89162d37e&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/377149197.sd.mp4?s=0923ca5f9f3ad9225159c0ad2d464cf89162d37e&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448365.hd.mp4?s=25440c2591e381d4b614d0d2b0ea9e4a241ae178&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448365.hd.mp4?s=25440c2591e381d4b614d0d2b0ea9e4a241ae178&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448365.hd.mp4?s=25440c2591e381d4b614d0d2b0ea9e4a241ae178&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448365.hd.mp4?s=25440c2591e381d4b614d0d2b0ea9e4a241ae178&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448365.sd.mp4?s=a71bf01e8d389561973f0a28d5f3a05d2094d77e&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448365.sd.mp4?s=a71bf01e8d389561973f0a28d5f3a05d2094d77e&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458540361.hd.mp4?s=18409204c903d4eaa7ad609aebb8b5c19b53f801&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458540361.hd.mp4?s=18409204c903d4eaa7ad609aebb8b5c19b53f801&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458540361.sd.mp4?s=a69a1411d47cf4cc1468b0113f22b204d4b94e2a&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458540361.sd.mp4?s=a69a1411d47cf4cc1468b0113f22b204d4b94e2a&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458540361.sd.mp4?s=a69a1411d47cf4cc1468b0113f22b204d4b94e2a&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458540361.hd.mp4?s=18409204c903d4eaa7ad609aebb8b5c19b53f801&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458540361.hd.mp4?s=18409204c903d4eaa7ad609aebb8b5c19b53f801&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961319.hd.mp4?s=73188dffc077dac86b08a56cdab8fec3e0ae2664&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961319.sd.mp4?s=db8eaca64fa3fbe4a3779174e9fdcc02b281ba24&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961319.hd.mp4?s=73188dffc077dac86b08a56cdab8fec3e0ae2664&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961319.sd.mp4?s=db8eaca64fa3fbe4a3779174e9fdcc02b281ba24&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961319.sd.mp4?s=db8eaca64fa3fbe4a3779174e9fdcc02b281ba24&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961319.hd.mp4?s=73188dffc077dac86b08a56cdab8fec3e0ae2664&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458961319.hd.mp4?s=73188dffc077dac86b08a56cdab8fec3e0ae2664&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484715419.hd.mp4?s=892d696e52cd119b53f2e9dbed47dbe405502022&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484715419.hd.mp4?s=892d696e52cd119b53f2e9dbed47dbe405502022&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484715419.sd.mp4?s=92c8b2f31ca34a874a88bb2df03423c533f3f1b7&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484715419.sd.mp4?s=92c8b2f31ca34a874a88bb2df03423c533f3f1b7&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484715419.sd.mp4?s=92c8b2f31ca34a874a88bb2df03423c533f3f1b7&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484715419.hd.mp4?s=892d696e52cd119b53f2e9dbed47dbe405502022&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/484715419.hd.mp4?s=892d696e52cd119b53f2e9dbed47dbe405502022&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/482490968.hd.mp4?s=132541dee5241eb3389033d96b9057c755448c7a&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/482490968.hd.mp4?s=132541dee5241eb3389033d96b9057c755448c7a&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/482490968.sd.mp4?s=3d23c3e93ce44ad74d0345c279bc62a9b05fe2f7&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/482490968.hd.mp4?s=132541dee5241eb3389033d96b9057c755448c7a&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/482490968.sd.mp4?s=3d23c3e93ce44ad74d0345c279bc62a9b05fe2f7&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/482490968.sd.mp4?s=3d23c3e93ce44ad74d0345c279bc62a9b05fe2f7&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/482490968.hd.mp4?s=132541dee5241eb3389033d96b9057c755448c7a&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528246537.hd.mp4?s=870a6e779bd5e280aca54eeb0da4ba750f6a379c&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528246537.hd.mp4?s=870a6e779bd5e280aca54eeb0da4ba750f6a379c&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528246537.hd.mp4?s=870a6e779bd5e280aca54eeb0da4ba750f6a379c&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528246537.hd.mp4?s=870a6e779bd5e280aca54eeb0da4ba750f6a379c&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528246537.sd.mp4?s=5162671d1dd1febf72b7f5a543659141c576e5ea&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528246537.sd.mp4?s=5162671d1dd1febf72b7f5a543659141c576e5ea&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528258469.hd.mp4?s=cd56dbddad22edf17b8c6c8d43bfae3678c7162f&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528258469.hd.mp4?s=cd56dbddad22edf17b8c6c8d43bfae3678c7162f&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528258469.hd.mp4?s=cd56dbddad22edf17b8c6c8d43bfae3678c7162f&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528258469.hd.mp4?s=cd56dbddad22edf17b8c6c8d43bfae3678c7162f&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528258469.sd.mp4?s=67f06e1ce26fc7b7e1186d2ccd56d07ca340c40f&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528258469.sd.mp4?s=67f06e1ce26fc7b7e1186d2ccd56d07ca340c40f&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257811.hd.mp4?s=e6483c4396b2be267aca7a77990ecbd371d3c227&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257811.hd.mp4?s=e6483c4396b2be267aca7a77990ecbd371d3c227&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257811.hd.mp4?s=e6483c4396b2be267aca7a77990ecbd371d3c227&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257811.hd.mp4?s=e6483c4396b2be267aca7a77990ecbd371d3c227&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257811.sd.mp4?s=34ca5c82f1d38289564168d1d08c542db14690cc&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257811.sd.mp4?s=34ca5c82f1d38289564168d1d08c542db14690cc&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533865454.hd.mp4?s=8c0e30b0c71b83eb1afec4a51dd52ef152c8fa6a&profile_id=171&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533865454.sd.mp4?s=b0cdf401fe7bad7f10fcae35e8c4eafe32d83967&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533865454.hd.mp4?s=8c0e30b0c71b83eb1afec4a51dd52ef152c8fa6a&profile_id=169&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533865454.hd.mp4?s=8c0e30b0c71b83eb1afec4a51dd52ef152c8fa6a&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533865454.hd.mp4?s=8c0e30b0c71b83eb1afec4a51dd52ef152c8fa6a&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533865454.hd.mp4?s=8c0e30b0c71b83eb1afec4a51dd52ef152c8fa6a&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533865454.sd.mp4?s=b0cdf401fe7bad7f10fcae35e8c4eafe32d83967&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/400027346.hd.mp4?s=40eece225e0103121fe8e4d3aa8ddc5405e9191c&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/400027346.hd.mp4?s=40eece225e0103121fe8e4d3aa8ddc5405e9191c&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/400027346.hd.mp4?s=40eece225e0103121fe8e4d3aa8ddc5405e9191c&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/400027346.hd.mp4?s=40eece225e0103121fe8e4d3aa8ddc5405e9191c&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/400027346.sd.mp4?s=777811e27f85ac355806fe4aae69ad112a49793e&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/400027346.sd.mp4?s=777811e27f85ac355806fe4aae69ad112a49793e&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/400027346.sd.mp4?s=777811e27f85ac355806fe4aae69ad112a49793e&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579459234.hd.mp4?s=e9ed9a82cdcdf183ba95a1a1d1141d2a957b9694&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579459234.hd.mp4?s=e9ed9a82cdcdf183ba95a1a1d1141d2a957b9694&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579459234.hd.mp4?s=e9ed9a82cdcdf183ba95a1a1d1141d2a957b9694&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579459234.hd.mp4?s=e9ed9a82cdcdf183ba95a1a1d1141d2a957b9694&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579459234.sd.mp4?s=4cda25a8ce2d66960f867e49b8d504a824bfb6b6&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579459234.sd.mp4?s=4cda25a8ce2d66960f867e49b8d504a824bfb6b6&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/546668544.hd.mp4?s=9bf13acff5f02f71a84747409857bb8111ebd393&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/546668544.sd.mp4?s=0d246103023741f336a5ec753ed687a8a6fb680d&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/546668544.hd.mp4?s=9bf13acff5f02f71a84747409857bb8111ebd393&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/546668544.sd.mp4?s=0d246103023741f336a5ec753ed687a8a6fb680d&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447623.sd.mp4?s=4d56e2a5cc5a836673da343b9d730635192017f2&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447623.hd.mp4?s=365edf6601965c5627ad85c6e0f5c8bc4e820e67&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447623.hd.mp4?s=365edf6601965c5627ad85c6e0f5c8bc4e820e67&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447623.hd.mp4?s=365edf6601965c5627ad85c6e0f5c8bc4e820e67&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447623.sd.mp4?s=4d56e2a5cc5a836673da343b9d730635192017f2&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447623.hd.mp4?s=365edf6601965c5627ad85c6e0f5c8bc4e820e67&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448391.hd.mp4?s=b93535cdb8d115e8693f2cb8909779d8115954eb&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448391.sd.mp4?s=12a212c8121fd574ab077bb7771fc2e24a5ccf6f&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448391.hd.mp4?s=b93535cdb8d115e8693f2cb8909779d8115954eb&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448391.hd.mp4?s=b93535cdb8d115e8693f2cb8909779d8115954eb&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448391.hd.mp4?s=b93535cdb8d115e8693f2cb8909779d8115954eb&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448391.sd.mp4?s=12a212c8121fd574ab077bb7771fc2e24a5ccf6f&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448183.hd.mp4?s=ace54fdf64d7ab8a24e7a50d6f739309476a0a9a&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448183.hd.mp4?s=ace54fdf64d7ab8a24e7a50d6f739309476a0a9a&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448183.sd.mp4?s=cf9c1679ec38f87b4e10881c65e6c3533dbab7c0&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448183.hd.mp4?s=ace54fdf64d7ab8a24e7a50d6f739309476a0a9a&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448183.hd.mp4?s=ace54fdf64d7ab8a24e7a50d6f739309476a0a9a&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579448183.sd.mp4?s=cf9c1679ec38f87b4e10881c65e6c3533dbab7c0&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458543048.hd.mp4?s=4a60efbc70ac02c0087d2b33256d1ca1d7b93c0f&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458543048.sd.mp4?s=e737bb759535991a16e816c268514b6231a20dd2&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458543048.hd.mp4?s=4a60efbc70ac02c0087d2b33256d1ca1d7b93c0f&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458543048.hd.mp4?s=4a60efbc70ac02c0087d2b33256d1ca1d7b93c0f&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458543048.sd.mp4?s=e737bb759535991a16e816c268514b6231a20dd2&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458543048.hd.mp4?s=4a60efbc70ac02c0087d2b33256d1ca1d7b93c0f&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/458543048.sd.mp4?s=e737bb759535991a16e816c268514b6231a20dd2&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257193.hd.mp4?s=5fdcb23478d16f02ac4ad17f5711aa79cae39cc2&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257193.hd.mp4?s=5fdcb23478d16f02ac4ad17f5711aa79cae39cc2&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257193.hd.mp4?s=5fdcb23478d16f02ac4ad17f5711aa79cae39cc2&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257193.sd.mp4?s=fc062acc3b44641002ba9fb21d48d40f3173bacf&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257193.hd.mp4?s=5fdcb23478d16f02ac4ad17f5711aa79cae39cc2&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/528257193.sd.mp4?s=fc062acc3b44641002ba9fb21d48d40f3173bacf&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/485533524.hd.mp4?s=8aa07f9f863d2d49832fb276c252586b58b31e05&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/485533524.sd.mp4?s=9850084882a38039fd1951d1029d64ba12e99202&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/485533524.hd.mp4?s=8aa07f9f863d2d49832fb276c252586b58b31e05&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/485533524.hd.mp4?s=8aa07f9f863d2d49832fb276c252586b58b31e05&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/485533524.sd.mp4?s=9850084882a38039fd1951d1029d64ba12e99202&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/485533524.hd.mp4?s=8aa07f9f863d2d49832fb276c252586b58b31e05&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/485533524.sd.mp4?s=9850084882a38039fd1951d1029d64ba12e99202&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/546667363.hd.mp4?s=0f251cea10c97b741bdabe03dc13bf55cb03842c&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/546667363.sd.mp4?s=86b6015c7f7e82f37639380fb55d45b31b9edba4&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/546667363.sd.mp4?s=86b6015c7f7e82f37639380fb55d45b31b9edba4&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/546667363.hd.mp4?s=0f251cea10c97b741bdabe03dc13bf55cb03842c&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447535.sd.mp4?s=fb15ee9a7eb9ce3ec390df86cdce548c36bb16b6&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447535.hd.mp4?s=531943398d9b6c012f5722c1fc34aa7034c1a2ca&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447535.hd.mp4?s=531943398d9b6c012f5722c1fc34aa7034c1a2ca&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447535.sd.mp4?s=fb15ee9a7eb9ce3ec390df86cdce548c36bb16b6&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447535.hd.mp4?s=531943398d9b6c012f5722c1fc34aa7034c1a2ca&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447535.hd.mp4?s=531943398d9b6c012f5722c1fc34aa7034c1a2ca&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447409.hd.mp4?s=0b8559e223f09c5208d8b3431ee572b538ff83bd&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447409.hd.mp4?s=0b8559e223f09c5208d8b3431ee572b538ff83bd&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447409.sd.mp4?s=615a1f458faba7e72e1a28106a0b57119b690f44&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447409.hd.mp4?s=0b8559e223f09c5208d8b3431ee572b538ff83bd&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447409.hd.mp4?s=0b8559e223f09c5208d8b3431ee572b538ff83bd&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/579447409.sd.mp4?s=615a1f458faba7e72e1a28106a0b57119b690f44&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452859309.hd.mp4?s=45264f8d3a9522ab815123299dbcb50c4f520c0c&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452859309.sd.mp4?s=4301749dfd69ef7412d13053dbe5dbbb2d5b658c&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452859309.hd.mp4?s=45264f8d3a9522ab815123299dbcb50c4f520c0c&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452859309.sd.mp4?s=4301749dfd69ef7412d13053dbe5dbbb2d5b658c&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/452859309.sd.mp4?s=4301749dfd69ef7412d13053dbe5dbbb2d5b658c&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530198594.hd.mp4?s=8ceaa17427c5475cb63050a03cd2d35a5ceffea6&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530198594.sd.mp4?s=45e30a87c67fc9f2c048c066c337f59de0be0b77&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530198594.hd.mp4?s=8ceaa17427c5475cb63050a03cd2d35a5ceffea6&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530198594.hd.mp4?s=8ceaa17427c5475cb63050a03cd2d35a5ceffea6&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530198594.sd.mp4?s=45e30a87c67fc9f2c048c066c337f59de0be0b77&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530198594.hd.mp4?s=8ceaa17427c5475cb63050a03cd2d35a5ceffea6&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.hd.mp4?s=fab1d34f66627b6c189f21504635c6519d2c9613&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.hd.mp4?s=fab1d34f66627b6c189f21504635c6519d2c9613&profile_id=169&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.hd.mp4?s=fab1d34f66627b6c189f21504635c6519d2c9613&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.hd.mp4?s=fab1d34f66627b6c189f21504635c6519d2c9613&profile_id=171&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.sd.mp4?s=b0125c33636dd64adf24ee59bbeb9ecdacdb4d24&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.hd.mp4?s=fab1d34f66627b6c189f21504635c6519d2c9613&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.sd.mp4?s=b0125c33636dd64adf24ee59bbeb9ecdacdb4d24&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.hd.mp4?s=fab1d34f66627b6c189f21504635c6519d2c9613&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.sd.mp4?s=b0125c33636dd64adf24ee59bbeb9ecdacdb4d24&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430869192.hd.mp4?s=fab1d34f66627b6c189f21504635c6519d2c9613&profile_id=173&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201145.sd.mp4?s=0e1aacef8d343bef6d7605b76067cb59317c55d4&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201145.hd.mp4?s=77623fa6f82011e2ecdee0a3cb415f716b70d97f&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201145.hd.mp4?s=77623fa6f82011e2ecdee0a3cb415f716b70d97f&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201145.hd.mp4?s=77623fa6f82011e2ecdee0a3cb415f716b70d97f&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201145.sd.mp4?s=0e1aacef8d343bef6d7605b76067cb59317c55d4&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201145.hd.mp4?s=77623fa6f82011e2ecdee0a3cb415f716b70d97f&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/439033126.sd.mp4?s=336d87985f3acdaf5e98ec134a96031ae1ea9730&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/439033126.hd.mp4?s=d2e341b3d01ef6bd2591af2c562cb341c810e91c&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/439033126.hd.mp4?s=d2e341b3d01ef6bd2591af2c562cb341c810e91c&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/439033126.sd.mp4?s=336d87985f3acdaf5e98ec134a96031ae1ea9730&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/439033126.sd.mp4?s=336d87985f3acdaf5e98ec134a96031ae1ea9730&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.hd.mp4?s=7a80b33c197bf7f99fb5d1c740a867ad746948bd&profile_id=169&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.sd.mp4?s=91ea1597ee301ce5e88e6f56e3a4f56851931ab1&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.hd.mp4?s=7a80b33c197bf7f99fb5d1c740a867ad746948bd&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.hd.mp4?s=7a80b33c197bf7f99fb5d1c740a867ad746948bd&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.sd.mp4?s=91ea1597ee301ce5e88e6f56e3a4f56851931ab1&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.hd.mp4?s=7a80b33c197bf7f99fb5d1c740a867ad746948bd&profile_id=171&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.hd.mp4?s=7a80b33c197bf7f99fb5d1c740a867ad746948bd&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.hd.mp4?s=7a80b33c197bf7f99fb5d1c740a867ad746948bd&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.sd.mp4?s=91ea1597ee301ce5e88e6f56e3a4f56851931ab1&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412407926.hd.mp4?s=7a80b33c197bf7f99fb5d1c740a867ad746948bd&profile_id=173&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/487726084.hd.mp4?s=59be52ca5852749237014fe44a4b872bbd0b25a9&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/487726084.sd.mp4?s=e44e47cf8a0a645cef81f06474e8fe1f53cd4aff&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/487726084.hd.mp4?s=59be52ca5852749237014fe44a4b872bbd0b25a9&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/487726084.sd.mp4?s=e44e47cf8a0a645cef81f06474e8fe1f53cd4aff&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/487726084.sd.mp4?s=e44e47cf8a0a645cef81f06474e8fe1f53cd4aff&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/448048609.hd.mp4?s=91c939b7efa078d391ef13da6d08c12d0985f2df&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/448048609.hd.mp4?s=91c939b7efa078d391ef13da6d08c12d0985f2df&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/448048609.hd.mp4?s=91c939b7efa078d391ef13da6d08c12d0985f2df&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/448048609.sd.mp4?s=11dc989cb40a69e3453d00fcf4c73ba1c7a11969&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/448048609.hd.mp4?s=91c939b7efa078d391ef13da6d08c12d0985f2df&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/448048609.sd.mp4?s=11dc989cb40a69e3453d00fcf4c73ba1c7a11969&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/448048609.sd.mp4?s=11dc989cb40a69e3453d00fcf4c73ba1c7a11969&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201183.sd.mp4?s=a2cf7e81d4ae205fd70a621bce75a21760fcd095&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201183.hd.mp4?s=c3bf66913e46aaeaa9efec0e94508cb8d57ad5e3&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201183.hd.mp4?s=c3bf66913e46aaeaa9efec0e94508cb8d57ad5e3&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201183.hd.mp4?s=c3bf66913e46aaeaa9efec0e94508cb8d57ad5e3&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201183.hd.mp4?s=c3bf66913e46aaeaa9efec0e94508cb8d57ad5e3&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/530201183.sd.mp4?s=a2cf7e81d4ae205fd70a621bce75a21760fcd095&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/494391854.sd.mp4?s=006e47eefaaef1f96f2df59654717ccc9a228fb1&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/494391854.sd.mp4?s=006e47eefaaef1f96f2df59654717ccc9a228fb1&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/494391854.hd.mp4?s=1d9c829f9464da48325644ad9e4bf399b58c659b&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/494391854.hd.mp4?s=1d9c829f9464da48325644ad9e4bf399b58c659b&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/494391854.hd.mp4?s=1d9c829f9464da48325644ad9e4bf399b58c659b&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/494391854.sd.mp4?s=006e47eefaaef1f96f2df59654717ccc9a228fb1&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/494391854.hd.mp4?s=1d9c829f9464da48325644ad9e4bf399b58c659b&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.sd.mp4?s=c7e87fb7226a259fdbe10d15167786399a3aab4a&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.hd.mp4?s=49ad494f28c0df45103ca8a6ebfaed6188a6d870&profile_id=171&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.hd.mp4?s=49ad494f28c0df45103ca8a6ebfaed6188a6d870&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.hd.mp4?s=49ad494f28c0df45103ca8a6ebfaed6188a6d870&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.sd.mp4?s=c7e87fb7226a259fdbe10d15167786399a3aab4a&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.hd.mp4?s=49ad494f28c0df45103ca8a6ebfaed6188a6d870&profile_id=173&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.sd.mp4?s=c7e87fb7226a259fdbe10d15167786399a3aab4a&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.hd.mp4?s=49ad494f28c0df45103ca8a6ebfaed6188a6d870&profile_id=169&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.hd.mp4?s=49ad494f28c0df45103ca8a6ebfaed6188a6d870&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/412408254.hd.mp4?s=49ad494f28c0df45103ca8a6ebfaed6188a6d870&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533877168.sd.mp4?s=4b35944422d35c96988ad46670f22dafca790396&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533877168.hd.mp4?s=823c3d0fefbeb4eacf530a463f83cc3bcafc7706&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533877168.hd.mp4?s=823c3d0fefbeb4eacf530a463f83cc3bcafc7706&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/533877168.sd.mp4?s=4b35944422d35c96988ad46670f22dafca790396&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.hd.mp4?s=b3883fe7dab3b1f79ea182f5d451b3a190e25f71&profile_id=173&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.hd.mp4?s=b3883fe7dab3b1f79ea182f5d451b3a190e25f71&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.sd.mp4?s=7426bc6c41e7e05661cdde0bc15de1c52abea15c&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.hd.mp4?s=b3883fe7dab3b1f79ea182f5d451b3a190e25f71&profile_id=171&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.hd.mp4?s=b3883fe7dab3b1f79ea182f5d451b3a190e25f71&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.hd.mp4?s=b3883fe7dab3b1f79ea182f5d451b3a190e25f71&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.sd.mp4?s=7426bc6c41e7e05661cdde0bc15de1c52abea15c&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.sd.mp4?s=7426bc6c41e7e05661cdde0bc15de1c52abea15c&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.hd.mp4?s=b3883fe7dab3b1f79ea182f5d451b3a190e25f71&profile_id=169&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419828832.hd.mp4?s=b3883fe7dab3b1f79ea182f5d451b3a190e25f71&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/451496538.hd.mp4?s=11981034c9a824019d46bece87d496cd870d752c&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/451496538.hd.mp4?s=11981034c9a824019d46bece87d496cd870d752c&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/451496538.hd.mp4?s=11981034c9a824019d46bece87d496cd870d752c&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/451496538.sd.mp4?s=99054cf3f10833c0951bd46cdd29b0d4dbe4ba09&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/451496538.sd.mp4?s=99054cf3f10833c0951bd46cdd29b0d4dbe4ba09&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/451496538.hd.mp4?s=11981034c9a824019d46bece87d496cd870d752c&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/451496538.sd.mp4?s=99054cf3f10833c0951bd46cdd29b0d4dbe4ba09&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/357872394.hd.mp4?s=f000128fae8aa60c142d7a38fe04fb2a830ea930&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/357872394.hd.mp4?s=f000128fae8aa60c142d7a38fe04fb2a830ea930&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/357872394.hd.mp4?s=f000128fae8aa60c142d7a38fe04fb2a830ea930&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/357872394.hd.mp4?s=f000128fae8aa60c142d7a38fe04fb2a830ea930&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/357872394.sd.mp4?s=2c4ed9368cbb10ab2f54ecef27b5674195be8ce8&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/357872394.sd.mp4?s=2c4ed9368cbb10ab2f54ecef27b5674195be8ce8&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/357872394.sd.mp4?s=2c4ed9368cbb10ab2f54ecef27b5674195be8ce8&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.sd.mp4?s=a6cef4ba0051f0e95f0a3ee3e42d766f8fd72bbb&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.hd.mp4?s=d676937cd574def22d656be405bf3f67cd7c3dd7&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.hd.mp4?s=d676937cd574def22d656be405bf3f67cd7c3dd7&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.sd.mp4?s=a6cef4ba0051f0e95f0a3ee3e42d766f8fd72bbb&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.hd.mp4?s=d676937cd574def22d656be405bf3f67cd7c3dd7&profile_id=173&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.sd.mp4?s=a6cef4ba0051f0e95f0a3ee3e42d766f8fd72bbb&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.hd.mp4?s=d676937cd574def22d656be405bf3f67cd7c3dd7&profile_id=169&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.hd.mp4?s=d676937cd574def22d656be405bf3f67cd7c3dd7&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.hd.mp4?s=d676937cd574def22d656be405bf3f67cd7c3dd7&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/419951948.hd.mp4?s=d676937cd574def22d656be405bf3f67cd7c3dd7&profile_id=171&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.hd.mp4?s=b3538b74126c8b6a7dedd8455f8b977bd71c8e5b&profile_id=169&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.hd.mp4?s=b3538b74126c8b6a7dedd8455f8b977bd71c8e5b&profile_id=170&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.sd.mp4?s=f85099131d6933ef47766c891cb1862c91cc7233&profile_id=139&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.hd.mp4?s=b3538b74126c8b6a7dedd8455f8b977bd71c8e5b&profile_id=174&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.hd.mp4?s=b3538b74126c8b6a7dedd8455f8b977bd71c8e5b&profile_id=172&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.hd.mp4?s=b3538b74126c8b6a7dedd8455f8b977bd71c8e5b&profile_id=171&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.sd.mp4?s=f85099131d6933ef47766c891cb1862c91cc7233&profile_id=164&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.hd.mp4?s=b3538b74126c8b6a7dedd8455f8b977bd71c8e5b&profile_id=175&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.sd.mp4?s=f85099131d6933ef47766c891cb1862c91cc7233&profile_id=165&oauth2_token_id=57447761",
        "https://player.vimeo.com/external/430711671.hd.mp4?s=b3538b74126c8b6a7dedd8455f8b977bd71c8e5b&profile_id=173&oauth2_token_id=57447761",
    ]
    # api_key = 'Nc9L4flgxNcToZZdkUCUtIvm6qQVtXYmEsR5UUg6oHJ7Z3h5aJT9Q9K7'

    # # API endpoint
    # url = f"https://api.pexels.com/videos/search?query={category}&per_page={img_count}"
    # # Query parameters
    # query = category
    # per_page = int(math.ceil(img_count/7))
    # # print(query,per_page)
    # # Headers
    # headers = {'Authorization': api_key}

    # # Parameters
    # params = {'query': query, 'per_page': per_page}

    # # Make GET request
    # response = requests.get(url, headers=headers)
    # arr=[]
    # # Check if request was successful
    # if response.status_code == 200:
    #     data = response.json()
    #     # print(data["videos"])
    #     for obj in data["videos"]:
    #         for innerobj in obj["video_files"]:
    #             arr.append(innerobj["link"])
    # else:
    #     print("Failed to fetch videos. Status code:", response.status_code)
    # return arr


def extract_social_media_urls(url):
    # Fetch HTML content of the website
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Regular expressions to match social media URLs
    social_media_regex = {
        "twitter": re.compile(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/\w+"),
        "facebook": re.compile(r"(?:https?:\/\/)?(?:www\.)?facebook\.com\/\w+"),
        "instagram": re.compile(r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/\w+"),
        "linkedin": re.compile(r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/\w+"),
        "youtube": re.compile(r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/\w+"),
        "pinterest": re.compile(r"(?:https?:\/\/)?(?:www\.)?pinterest\.com\/\w+"),
        "reddit": re.compile(r"(?:https?:\/\/)?(?:www\.)?reddit\.com\/\w+"),
        "tumblr": re.compile(r"(?:https?:\/\/)?(?:www\.)?tumblr\.com\/\w+"),
        "snapchat": re.compile(r"(?:https?:\/\/)?(?:www\.)?snapchat\.com\/\w+"),
        "whatsapp": re.compile(r"(?:https?:\/\/)?(?:www\.)?whatsapp\.com\/\w+"),
        "tripadvisor": re.compile(r"(?:https?:\/\/)?(?:www\.)?tripadvisor\.com\/\w+"),
    }

    social_media_links = []

    # Find all links on the webpage
    links = soup.find_all("a", href=True)

    # Extract social media URLs from links
    for link in links:
        href = link.get("href")
        for platform, regex in social_media_regex.items():
            if regex.match(href):
                social_media_links.append({platform: href})

    # Remove duplicates and return unique social media links
    social_media_links = list(
        {link[list(link.keys())[0]]: link for link in social_media_links}.values()
    )

    return social_media_links


def checker(ndid):
    find = db.Zucks_hotellinks.find_one({"ndid": ndid})
    if find == None:
        return False
    return True


def createRoom(roomCategories, token, hId):
    for obj in roomCategories:
        obj["hId"] = hId
        room_usecase.add_room(obj, token)


def dataforwebsiteExtract(maintain_data, domain, locationid, ndid, engineLink):
    # try:
    # if website already exists check
    if checker(ndid):

        return False, "Website Already Exists For this user"

    # if(hid)

    img_count = 50

    # if (maintain_data.get("oldWebsite")==""):
    arr = []
    socialmedia = [
        "twitter",
        "facebook",
        "instagram",
        "linkedin",
        "youtube",
        "pinterest",
        "reddit",
        "tumblr",
        "snapchat",
        "whatsapp",
        "tripadvisor",
    ]
    for obj in socialmedia:
        arr.append(
            {
                obj: f"https://www.{obj}.com/{maintain_data.get('hotelName').replace(' ', '')}"
            }
        )
    # else:
    #     arr = extract_social_media_urls(maintain_data.get("oldWebsite"))

    images = createimage(maintain_data.get("category"), img_count)
    videos = createvideo(maintain_data.get("category"), img_count)

    data_to_create_for_website(
        arr,
        images,
        domain,
        locationid,
        ndid,
        engineLink,
        maintain_data.get("hotelName"),
        videos,
        maintain_data,
    )

    create_profile(ndid, locationid, maintain_data, domain)
    hotelLink(maintain_data.get("planName"), ndid, locationid, domain)
    create_otpStorage(ndid)
    return True, "Website And Booking Engine Created Successfully"


# except Exception as ex:
#     print(ex)
#     return False,"Website And Booking Engine Creation Failed"


def getAboutText(hotelName, hotelCity):
    randIdx = random.sample(range(0, len(about) - 1), 2)
    about_1 = about[randIdx[0]].replace("[hotelName]", hotelName)
    about_1 = about_1.replace("[hotelCity]", hotelCity)
    about_2 = about[randIdx[1]].replace("[hotelName]", hotelName)
    about_2 = about_2.replace("[hotelCity]", hotelCity)
    return about_1 + "\n" + about_2


def create_binary_from_base64(base64_string, base):
    # Decode base64 string
    decoded_bytes = base64.b64decode(base64_string)

    # Convert the decoded bytes to an integer with the specified base
    binary_value = int.from_bytes(decoded_bytes, byteorder="big", signed=False)

    return binary_value


# this is for the testing purpose only
def website_comman_object(
    socialMedia,
    images,
    domain,
    locationid,
    ndid,
    engineLink,
    hotelName,
    videos,
    maintain_data,
):
    Details = {
        "Navbar": {
            "Home": True,
            "About": True,
            "Gallery": True,
            "Nearby": True,
            "Blogs": True,
            "Restaurant": True,
            "Room": True,
            "Facilities": True,
            "Service": True,
            "Contact": True,
        },
        "Banner": [
            {
                "Heading": banner_heading[random.randint(0, len(banner_heading) - 1)]
                + " "
                + hotelName,
                "Subhead": "",
                "url": images[random.randint(0, len(images) - 1)],
                "video": (
                    maintain_data.get("bannerVideo")
                    if (maintain_data.get("bannerVideo") != "")
                    else videos[random.randint(0, len(videos) - 1)]
                ),
            },
            {
                "Heading": banner_heading[random.randint(0, len(banner_heading) - 1)]
                + " "
                + hotelName,
                "Subhead": "",
                "url": images[random.randint(0, len(images) - 1)],
                "video": videos[random.randint(0, len(videos) - 1)],
            },
            {
                "Heading": banner_heading[random.randint(0, len(banner_heading) - 1)]
                + " "
                + hotelName,
                "Subhead": "",
                "url": images[random.randint(0, len(images) - 1)],
                "video": videos[random.randint(0, len(videos) - 1)],
            },
        ],
        "HotelAdvr": {
            "heading": banner_heading[random.randint(0, len(banner_heading) - 1)],
            "video": videos[random.randint(0, len(videos) - 1)],
            "Image": images[random.randint(0, len(images) - 1)],
        },
        "Links": {},
        "Engine": engineLink,
        "Footer": {
            "Address": maintain_data.get("hotelAddress"),
            "Phone": maintain_data.get("hotelPhone"),
            "WhatsApp": maintain_data.get("hotelPhone"),
            "City": maintain_data.get("hotelCity"),
            "Email": maintain_data.get("hotelEmail"),
            "AboutText": "At our Hotel you will feel great to stay and have a good fun",
            "NewsLetterText": "Hi this text is for newsletter",
            "Logo": (
                maintain_data.get("logo")
                if (maintain_data.get("logo") != "")
                else "https://www.nicepng.com/png/full/111-1111079_logo-templates-png-download-template-logo-png.png"
            ),
        },
        "About": {
            "Heading": "About " + maintain_data.get("hotelName"),
            "Text": getAboutText(
                maintain_data.get("hotelName"),
                maintain_data.get("hotelCity"),
            ),
            "url": images[random.randint(0, len(images) - 1)],
            "video_url": "",
        },
        "Facilities": {
            "FrontDesk": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Wifi": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Board": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Rooftop_Cafe": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Health_Club": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Express_checks": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Wave_Bar": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Conference_Hall": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Alchemy": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Suncafe": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Doctor": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Spa": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Babysitting": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Electricity": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Concierge": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Conditinoer": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Security": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "TravelTour": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Currency_Exchange": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Laundry": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Casino": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Parking": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Elevator": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Jacuzzi": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Room_Service": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Accept_Cards": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Child_Care": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Conference_Rooms": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Fitness_Center": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Health_&_Beauty": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Restaurant": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Swimming_Pool": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Housekeep": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "cofeemaker": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "minibar": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "Evpoint": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
            "SaunaStream": (
                True
                if maintain_data.get("Facilities").get("FrontDesk") == "true"
                else False
            ),
        },
        "Images": [],
        "Faq": [
            {
                "Question": "What is the check-in/check-out time?",
                "Answer": "Guests typically check in after 3:00 PM and check out before 11:00 AM. However, these times can vary, so it's always good to check with the specific hotel.",
            },
            {
                "Question": "Is Wi-Fi available, and is it free?",
                "Answer": "Most hotels offer Wi-Fi, but some may charge a fee. Confirm the Wi-Fi details at check-in.",
            },
            {
                "Question": "Do you provide parking facilities?",
                "Answer": "Inquire about parking options, whether they have on-site parking, valet services, or partnerships with nearby garages.",
            },
            {
                "Question": "Are pets allowed?",
                "Answer": "Check the hotel's pet policy, including any fees, restrictions, and amenities for guests with pets.",
            },
            {
                "Question": "Can I request a late check-out?",
                "Answer": "Some hotels may accommodate late check-outs based on availability. Confirm the policy and any associated fees.",
            },
            {
                "Question": "What amenities are included in the room?",
                "Answer": "Clarify what is provided in the room, such as toiletries, towels, a hairdryer, and if there's a minibar or coffee maker.",
            },
        ],
        "TermsConditions": [
            {"Privacy": "Privacy policy Data"},
            {"Cancellation": "Cancellation policy Data"},
            {"TermsServices": "TermsServices policy Data"},
        ],
        "Menu": [
            {
                "Image": "https://c.ndtvimg.com/2020-09/if4pp5j8_vegetarian_625x300_30_September_20.jpg",
                "Name": "",
                "Price": "",
                "Description": "",
            },
            {
                "Image": "https://media.istockphoto.com/id/1040749178/photo/thali-meal-indian-food.jpg?s=612x612&w=0&k=20&c=rFN8W5zVH-lCOLzf3n_wLWXBvOOIX4WP2Jh3bZ0YAgU=",
                "Name": "",
                "Price": "",
                "Description": "",
            },
            {
                "Image": "https://assets.zeezest.com/blogs/PROD_Veg-Food-Banner_1645021052320_thumb_1200.jpeg",
                "Name": "",
                "Price": "",
                "Description": "",
            },
            {
                "Image": "https://www.gigadocs.com/blog/wp-content/uploads/2020/03/istock-955998758.jpg",
                "Name": "",
                "Price": "",
                "Description": "",
            },
            {
                "Image": "https://media.istockphoto.com/id/186087388/photo/thali-with-rice-and-vegetables-on-green-painted-wooden-table.jpg?s=612x612&w=0&k=20&c=XSo8ePZ8Iy3Y1JGPK68uEmMeTx9S6tkTFaqTbsBc-no=",
                "Name": "",
                "Price": "",
                "Description": "",
            },
            {
                "Image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/South_Indian_non-veg_Meals.jpg/800px-South_Indian_non-veg_Meals.jpg",
                "Name": "",
                "Price": "",
                "Description": "",
            },
        ],
        "Gallery": [
            {
                "Category": "Events",
                "Required": True,
                "Images": [
                    "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8ZXZlbnR8ZW58MHx8MHx8fDA%3D"
                ],
            },
            {
                "Category": "Restaurants",
                "Required": True,
                "Images": [
                    "https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg"
                ],
            },
            {
                "Category": "Hotels",
                "Required": True,
                "Images": [
                    "https://cdn.britannica.com/96/115096-050-5AFDAF5D/Bellagio-Hotel-Casino-Las-Vegas.jpg"
                ],
            },
            {
                "Category": "Nearby",
                "Required": True,
                "Images": [
                    "https://cdn.britannica.com/96/115096-050-5AFDAF5D/Bellagio-Hotel-Casino-Las-Vegas.jpg"
                ],
            },
            {
                "Category": "View",
                "Required": True,
                "Images": [
                    "https://cdn.britannica.com/96/115096-050-5AFDAF5D/Bellagio-Hotel-Casino-Las-Vegas.jpg"
                ],
            },
            {
                "Category": "Rooms",
                "Required": True,
                "Images": [
                    "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
                ],
            },
            {
                "Category": "Lobby",
                "Required": True,
                "Images": [
                    "https://novoxinc.com/cdn/shop/articles/novox_5_hotel_lobby_design_ideas_that_will_inspire-you_hero_image_1024x576px_1024x.jpg?v=1659361242"
                ],
            },
            {
                "Category": "Bar",
                "Required": True,
                "Images": [
                    "https://images.pexels.com/photos/63633/bar-local-cong-ireland-63633.jpeg"
                ],
            },
            {
                "Category": "Playzone",
                "Required": True,
                "Images": ["https://funcity.in/image/playzone4.jpeg"],
            },
        ],
        "Services": [
            {
                "Title": "Service 1",
                "Text": "",
                "Image": "https://thumbs.dreamstime.com/b/all-you-need-waitress-uniform-delivering-tray-food-room-hotel-room-service-focus-tableware-waitress-174457737.jpg",
            },
            {
                "Title": "Service 2",
                "Text": "",
                "Image": "https://media.istockphoto.com/id/139984085/photo/luggage-in-hotel-room.jpg?s=612x612&w=0&k=20&c=C8HVRQLlDmYiVOYczyxuYGYV39ekWXS6K1wqD77mp_k=",
            },
            {
                "Title": "Service 3",
                "Text": "",
                "Image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Boon_Hotel_%2B_Spa_-_Sarah_Stierch_-_April_2019_-_9.jpg/800px-Boon_Hotel_%2B_Spa_-_Sarah_Stierch_-_April_2019_-_9.jpg",
            },
            {
                "Title": "Service 4",
                "Text": "",
                "Image": "https://grandpalaceriga.com/wp-content/uploads/2015/04/Seasons-1_compressed-min.jpg",
            },
            {
                "Title": "Service 5",
                "Text": "",
                "Image": "https://arcmaxarchitect.com/sites/default/files/resort_hotel_design_sample_-11.jpg",
            },
        ],
        "Restaurant": [
            {
                "Heading": "Restaurant1",
                "Image": "",
                "Text": "",
                "Timeslot": "",
            }
        ],
        "Team": [],
        "Nearby": [
            {
                "Image": "https://media-cdn.tripadvisor.com/media/photo-s/0f/6d/c1/00/mayfair-darjeeling.jpg",
                "Place": "",
                "Description": "",
            },
            {
                "Image": "https://media-cdn.tripadvisor.com/media/photo-s/04/2d/01/30/mayfair-darjeeling.jpg",
                "Place": "",
                "Description": "",
            },
            {
                "Image": "https://www.journeyera.com/wp-content/uploads/2020/05/best-hotels-in-agra-near-taj-mahal-with-view-47406152.jpg",
                "Place": "",
                "Description": "",
            },
            {
                "Image": "https://i0.wp.com/bangalorerealestates.in/wp-content/uploads/2015/06/d1.jpg?fit=1024%2C400&ssl=1",
                "Place": "",
                "Description": "",
            },
            {
                "Image": "https://images.squarespace-cdn.com/content/v1/52da9677e4b03d314575985a/1425872191027-NAJO6DITOGJ9VCFOFB0C/Ramada+Downtown+Dubai+Hotel+near+Burj+Khalifa.jpg",
                "Place": "",
                "Description": "",
            },
        ],
        "Blogs": [],
        "Advertisnment": [
            {
                "Heading": "Head",
                "Text": "text",
                "Image": "Imagelink",
                "Required": True,
            }
        ],
        "PromotionalPopups": {
            "Heading": "head",
            "Text": "text",
            "Image": "image",
            "Required": True,
        },
        "SeoOptimisation": [
            {
                "PageName": "Home",
                "Data": {
                    "Title": "Home Page",
                    "Description": "Home  description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "About",
                "Data": {
                    "Title": "About Page",
                    "Description": "About description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Contact",
                "Data": {
                    "Title": "Contact Page",
                    "Description": "Contact description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Nearby Attraction",
                "Data": {
                    "Title": "Nearby Page",
                    "Description": "Nearby description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Facilities",
                "Data": {
                    "Title": "Facilities Page",
                    "Description": "Facilities description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Gallery",
                "Data": {
                    "Title": "Gallery Page",
                    "Description": "Gallery description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Rooms",
                "Data": {
                    "Title": "Rooms Page",
                    "Description": "Rooms description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Reservations",
                "Data": {
                    "Title": "Reservations",
                    "Description": "Reservations",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Terms and condition",
                "Data": {
                    "Title": "Terms Page",
                    "Description": "Terms description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Services",
                "Data": {
                    "Title": "Services Page",
                    "Description": "Services description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Restaurants",
                "Data": {
                    "Title": "Restaurants Page",
                    "Description": "Restaurants description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Testimonials",
                "Data": {
                    "Title": "Testimonials Page",
                    "Description": "Testimonials description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Teams",
                "Data": {
                    "Title": "Teams Page",
                    "Description": "Teams description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Blogs",
                "Data": {
                    "Title": "Blogs",
                    "Description": "Blogs description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Faq",
                "Data": {
                    "Title": "Faq page",
                    "Description": "Blogs description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Cancellation",
                "Data": {
                    "Title": "Terms and Condition",
                    "Description": "Blogs description",
                    "keyword": "Keyword",
                },
            },
            {
                "PageName": "Privacy",
                "Data": {
                    "Title": "Privacy Policy",
                    "Description": "Privacy policy description",
                    "keyword": "Keyword",
                },
            },
        ],
        "Location": getGoogleEmbeddedCode(maintain_data),
        "NewsletterData": [],
        "Reviews": {
            "Write": "",
            "Google": "",
            "Tripadvisors": "",
            "Instagram": "",
            "Facebook": "",
            "Clarity": "",
            "TagManager": "",
            "Console": "",
            "Pixel": "",
            "Analytics": "",
            "Pagespeed": "",
            # Add more key-value pairs as needed
        },
        "Contacts": [],
        "SectionsVisible": {
            "Home": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "About": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Rooms": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Blogs": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Gallery": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Facility": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Contact": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Reservation": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Booking": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Nearby": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Restaurant": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Spa": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Faq": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Services": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Teams": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "TermsConditions": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
            "Testimonial": {
                "Banner": True,
                "Rooms": True,
                "Facilities": True,
                "Nearby": True,
                "HotelAd": True,
                "YoutubeVideo": True,
                "Insta": True,
                "Testimonials": True,
                "AboutUs": True,
                "Images": True,
                "Map": True,
                "Whatsapp": True,
                "Teams": True,
                "Blogs": True,
            },
        },
        "DataToarrange": [
            {
                "Heading": "Things To Do",
                "Text": "Right Here Data",
                "Images": [
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                ],
            },
            {
                "Heading": "The Restaurant",
                "Text": "Right Here Data",
                "Images": [
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                ],
            },
            {
                "Heading": "The Dining",
                "Text": "Right Here Data",
                "Images": [
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                ],
            },
            {
                "Heading": "How To find Hotel",
                "Text": "Right Here Data",
                "Images": [
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                ],
            },
            {
                "Heading": "Contact Query",
                "Text": "Right Here Data",
                "Images": [
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                ],
            },
            {
                "Heading": "Arranged Data",
                "Text": "Right Here Data",
                "Images": [
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                ],
            },
            {
                "Heading": "Arrange",
                "Text": "Right Here Data",
                "Images": [
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                ],
            },
            {
                "Heading": "Scheme_code",
                "Text": "<script></script>",
                "Images": [
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                    {
                        "Image": images[random.randint(0, len(images) - 1)],
                        "Heading": "",
                        "Text": "",
                    },
                ],
            },
        ],
        "Chefs": [
            {
                "Name": "Tim",
                "Image": images[random.randint(0, len(images) - 1)],
                "Text": "text",
            }
        ],
        "Events": [],
        "SectionTitles": {
            "About": {"Title": "About", "Description": "Descrpition"},
            "Rooms": {
                "Title": "ROOMS ACCOMMODATION",
                "Description": "Utmost Luxury at Mandrem Retreat Beach Resort",
            },
            "Nearby": {
                "Title": "NEARBY PLACES",
                "Description": "Explore Wonders of food, fashion, and forts, just steps away from your accommodation in Mandrem.",
            },
            "Gallery": {
                "Title": "GALLERY",
                "Description": "Explore our world captured through lenses",
            },
            "Facilities": {
                "Title": "RESORT FACILITIES",
                "Description": "Relax in comfort and style at your mandrem retreat with our facilities by the pool.",
            },
            "OurRooms": {
                "Title": "OUR ROOMS",
                "Description": "Comfortable Retreats for Every Traveller at SPARV resort in Mandrem.",
            },
            "Services": {
                "Title": "Sevices",
                "Description": "Service Description",
            },
            "Bookings": {
                "Title": "Booking",
                "Description": "Booking Description",
            },
            "Testimonial": {
                "Title": "Testimonials",
                "Description": "Testimonials Description",
            },
            "Insta": {"Title": "Insta", "Description": "Insta Description"},
            "1": {"Title": "Checkin", "Description": "01:00 PM"},
            "2": {"Title": "Checkout", "Description": "10:00 AM"},
            "3": {"Title": "Rules", "Description": ""},
            "4": {"Title": "", "Description": ""},
            "5": {"Title": "", "Description": ""},
            "6": {"Title": "", "Description": ""},
            "7": {"Title": "", "Description": ""},
            "8": {"Title": "", "Description": ""},
        },
        "PagesTitles": {
            "About": {
                "Title": "THE HOTEL",
                "Description": "OUR PLACE, OUR SERVICES & OUR TEAM",
                "Image": images[0],
                "Video": "",
            },
            "Rooms": {
                "Title": "ROOMS & SUITES",
                "Description": "WHERE COMFORT MEETS CONVENIENCE",
                "Image": images[1],
                "Video": "",
            },
            "Nearby": {
                "Title": "NEARBY PLACES",
                "Description": "Explore Wonders of food, fashion, and forts, just steps away from your accommodation in Mandrem.",
                "Image": images[2],
                "Video": "",
            },
            "Gallery": {
                "Title": "GALLERY",
                "Description": "WHERE OPEN SKIES BECOME YOUR HORIZON",
                "Image": images[3],
                "Video": "",
            },
            "Facilities": {
                "Title": "FACILITIES",
                "Description": "ELEVATING YOUR EXPERIENCE",
                "Image": images[4],
                "Video": "",
            },
            "Our Rooms": {
                "Title": "OUR ROOMS",
                "Description": "Comfortable Retreats for Every Traveller at SPARV resort in Mandrem.",
                "Image": images[5],
                "Video": "",
            },
            "Contact": {
                "Title": "CONTACT",
                "Description": "OUR PLACE, OUR SERVICES & OUR TEAMS",
                "Image": images[6],
                "Video": "",
            },
            "Services": {
                "Title": "Services",
                "Description": "Service Description",
                "Image": images[7],
                "Video": "",
            },
            "Bookings": {
                "Title": "Booking Here",
                "Description": "Booking Description",
                "Image": images[8],
                "Video": "",
            },
            "Terms": {
                "Title": "TERMS & CONDITIONS",
                "Description": "THE PLACE, OUR SERVICES & OUR TEAM",
                "Image": images[9],
                "Video": "",
            },
            "Privacy": {
                "Title": "PRIVACY POLICY",
                "Description": "THE PLACE, OUR SERVICES & OUR TEAM",
                "Image": images[10],
                "Video": "",
            },
            "Cancellation": {
                "Title": "CANCELLATION POLICY",
                "Description": "THE PLACE, OUR SERVICES & OUR TEAM",
                "Image": images[11],
                "Video": "",
            },
            "Restaurant": {
                "Title": "Restaurant",
                "Description": "Restaurant Description",
                "Image": images[12],
                "Video": "",
            },
            "Teams": {
                "Title": "Teams",
                "Description": "Teams Description",
                "Image": images[13],
                "Video": "",
            },
            "Testimonial": {
                "Title": "Testimonials",
                "Description": "Testimonial Description",
                "Image": images[14],
                "Video": "",
            },
            "Blogs": {
                "Title": "Blogs",
                "Description": "Blogs Description",
                "Image": images[15],
                "Video": "",
            },
            "Faq": {
                "Title": "Faq",
                "Description": "Faq description",
                "Image": images[16],
                "Video": "",
            },
        },
        "Slugs": {
            "About": {
                "Slug": "About",
                "PageName": "about.html",
                "SeoData": 1,
                "sectionVisible": "About",
                "PageTitle": "About",
            },
            "Contact": {
                "Slug": "Contact",
                "PageName": "contact.html",
                "SeoData": 2,
                "sectionVisible": "Contact",
                "PageTitle": "Contact",
            },
            "Nearby_Attraction": {
                "Slug": "Nearby-Attraction",
                "PageName": "404.html",
                "SeoData": 3,
                "sectionVisible": "Nearby",
                "PageTitle": "Nearby",
            },
            "Facilities": {
                "Slug": "Facilities",
                "PageName": "facility.html",
                "SeoData": 4,
                "sectionVisible": "Facility",
                "PageTitle": "Facilities",
            },
            "Gallery": {
                "Slug": "Gallery",
                "PageName": "gallery1.html",
                "SeoData": 5,
                "sectionVisible": "Gallery",
                "PageTitle": "Gallery",
            },
            "Rooms": {
                "Slug": "Rooms",
                "PageName": "rooms-category.html",
                "SeoData": 6,
                "sectionVisible": "Rooms",
                "PageTitle": "Rooms",
            },
            "Reservations": {
                "Slug": "Reservations",
                "PageName": "404.html",
                "SeoData": 7,
                "sectionVisible": "Reservation",
                "PageTitle": "Gallery",
            },
            "Services": {
                "Slug": "Services",
                "PageName": "404.html",
                "SeoData": 9,
                "sectionVisible": "Services",
                "PageTitle": "Services",
            },
            "Restaurants": {
                "Slug": "Restaurants",
                "PageName": "404.html",
                "SeoData": 10,
                "sectionVisible": "Restaurant",
                "PageTitle": "Restaurant",
            },
            "Testimonials": {
                "Slug": "Testimonials",
                "PageName": "404.html",
                "SeoData": 11,
                "sectionVisible": "Testimonial",
                "PageTitle": "Testimonial",
            },
            "Teams": {
                "Slug": "Teams",
                "PageName": "404.html",
                "SeoData": 12,
                "sectionVisible": "Teams",
                "PageTitle": "Teams",
            },
            "Blogs": {
                "Slug": "Blogs",
                "PageName": "404.html",
                "SeoData": 13,
                "sectionVisible": "Blogs",
                "PageTitle": "Blogs",
            },
            "Faq": {
                "Slug": "Faq",
                "PageName": "404.html",
                "SeoData": 14,
                "sectionVisible": "Faq",
                "PageTitle": "Faq",
            },
            "Privacy": {
                "Slug": "Privacy-Policy",
                "PageName": "privacy.html",
                "SeoData": 8,
                "sectionVisible": "About",
                "PageTitle": "Privacy",
            },
            "Terms_and_condition": {
                "Slug": "Terms-And-Conditions",
                "PageName": "terms.html",
                "SeoData": 8,
                "sectionVisible": "About",
                "PageTitle": "Terms",
            },
            "Cancellation": {
                "Slug": "Cancellation-Policy",
                "PageName": "cancellation.html",
                "SeoData": 15,
                "sectionVisible": "About",
                "PageTitle": "Cancellation",
            },
        },
        "Colors": {
            "backgroundColor": maintain_data.get("colorCombination").get(
                "backgroundColor"
            ),
            "buttonColor": maintain_data.get("colorCombination").get("buttonColor"),
            "fontColor": maintain_data.get("colorCombination").get("fontColor"),
            "boardColor": maintain_data.get("colorCombination").get("boardColor"),
            "fontfamily": "Times New Roman",
        },
    }


def data_to_create_for_website(
    socialMedia,
    images,
    domain,
    locationid,
    ndid,
    engineLink,
    hotelName,
    videos,
    maintain_data,
):

    nearby_arr = createimage("Nearby of luxurious hotel", 5)
    services = createimage(maintain_data.get("category") + " services", 5)
    obj = {
        "Domain": domain,
        "Maintainance": False,
        "ndid": ndid,
        # "hId": locationid,
        "hotels": {
            locationid:{
                    "Navbar": {
                        "Home": True,
                        "About": True,
                        "Gallery": True,
                        "Nearby": True,
                        "Blogs": True,
                        "Restaurant": True,
                        "Room": True,
                        "Facilities": True,
                        "Service": True,
                        "Contact": True,
                    },
                    "Banner": [
                        {
                            "Heading": banner_heading[
                                random.randint(0, len(banner_heading) - 1)
                            ]
                            + " "
                            + hotelName,
                            "Subhead": "",
                            "url": images[random.randint(0, len(images) - 1)],
                            "video": (
                                maintain_data.get("bannerVideo")
                                if (maintain_data.get("bannerVideo") != "")
                                else videos[random.randint(0, len(videos) - 1)]
                            ),
                        },
                        {
                            "Heading": banner_heading[
                                random.randint(0, len(banner_heading) - 1)
                            ]
                            + " "
                            + hotelName,
                            "Subhead": "",
                            "url": images[random.randint(0, len(images) - 1)],
                            "video": videos[random.randint(0, len(videos) - 1)],
                        },
                        {
                            "Heading": banner_heading[
                                random.randint(0, len(banner_heading) - 1)
                            ]
                            + " "
                            + hotelName,
                            "Subhead": "",
                            "url": images[random.randint(0, len(images) - 1)],
                            "video": videos[random.randint(0, len(videos) - 1)],
                        },
                    ],
                    "HotelAdvr": {
                        "heading": banner_heading[
                            random.randint(0, len(banner_heading) - 1)
                        ],
                        "video": videos[random.randint(0, len(videos) - 1)],
                        "Image": images[random.randint(0, len(images) - 1)],
                    },
                    "Links": {},
                    "Engine": engineLink,
                    "Footer": {
                        "Address": maintain_data.get("hotelAddress"),
                        "Phone": maintain_data.get("hotelPhone"),
                        "WhatsApp": maintain_data.get("hotelPhone"),
                        "City": maintain_data.get("hotelCity"),
                        "Email": maintain_data.get("hotelEmail"),
                        "AboutText": "At our Hotel you will feel great to stay and have a good fun",
                        "NewsLetterText": "Hi this text is for newsletter",
                        "Logo": (
                            maintain_data.get("logo")
                            if (maintain_data.get("logo") != "")
                            else "https://www.nicepng.com/png/full/111-1111079_logo-templates-png-download-template-logo-png.png"
                        ),
                    },
                    "About": {
                        "Heading": "About " + maintain_data.get("hotelName"),
                        "Text": getAboutText(
                            maintain_data.get("hotelName"),
                            maintain_data.get("hotelCity"),
                        ),
                        "url": images[random.randint(0, len(images) - 1)],
                        "video_url": "",
                    },
                    "Facilities": {
                        "FrontDesk": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Wifi": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Board": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Rooftop_Cafe": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Health_Club": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Express_checks": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Wave_Bar": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Conference_Hall": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Alchemy": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Suncafe": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Doctor": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Spa": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Babysitting": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Electricity": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Concierge": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Conditinoer": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Security": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "TravelTour": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Currency_Exchange": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Laundry": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Casino": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Parking": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Elevator": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Jacuzzi": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Room_Service": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Accept_Cards": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Child_Care": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Conference_Rooms": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Fitness_Center": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Health_&_Beauty": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Restaurant": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Swimming_Pool": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Housekeep": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "cofeemaker": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "minibar": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "Evpoint": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                        "SaunaStream": (
                            True
                            if maintain_data.get("Facilities").get("FrontDesk")
                            == "true"
                            else False
                        ),
                    },
                    "Images": [],
                    "Faq": [
                        {
                            "Question": "What is the check-in/check-out time?",
                            "Answer": "Guests typically check in after 3:00 PM and check out before 11:00 AM. However, these times can vary, so it's always good to check with the specific hotel.",
                        },
                        {
                            "Question": "Is Wi-Fi available, and is it free?",
                            "Answer": "Most hotels offer Wi-Fi, but some may charge a fee. Confirm the Wi-Fi details at check-in.",
                        },
                        {
                            "Question": "Do you provide parking facilities?",
                            "Answer": "Inquire about parking options, whether they have on-site parking, valet services, or partnerships with nearby garages.",
                        },
                        {
                            "Question": "Are pets allowed?",
                            "Answer": "Check the hotel's pet policy, including any fees, restrictions, and amenities for guests with pets.",
                        },
                        {
                            "Question": "Can I request a late check-out?",
                            "Answer": "Some hotels may accommodate late check-outs based on availability. Confirm the policy and any associated fees.",
                        },
                        {
                            "Question": "What amenities are included in the room?",
                            "Answer": "Clarify what is provided in the room, such as toiletries, towels, a hairdryer, and if there's a minibar or coffee maker.",
                        },
                    ],
                    "TermsConditions": [
                        {"Privacy": "Privacy policy Data"},
                        {"Cancellation": "Cancellation policy Data"},
                        {"TermsServices": "TermsServices policy Data"},
                    ],
                    "Menu": [
                        {
                            "Image": "https://c.ndtvimg.com/2020-09/if4pp5j8_vegetarian_625x300_30_September_20.jpg",
                            "Name": "",
                            "Price": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://media.istockphoto.com/id/1040749178/photo/thali-meal-indian-food.jpg?s=612x612&w=0&k=20&c=rFN8W5zVH-lCOLzf3n_wLWXBvOOIX4WP2Jh3bZ0YAgU=",
                            "Name": "",
                            "Price": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://assets.zeezest.com/blogs/PROD_Veg-Food-Banner_1645021052320_thumb_1200.jpeg",
                            "Name": "",
                            "Price": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://www.gigadocs.com/blog/wp-content/uploads/2020/03/istock-955998758.jpg",
                            "Name": "",
                            "Price": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://media.istockphoto.com/id/186087388/photo/thali-with-rice-and-vegetables-on-green-painted-wooden-table.jpg?s=612x612&w=0&k=20&c=XSo8ePZ8Iy3Y1JGPK68uEmMeTx9S6tkTFaqTbsBc-no=",
                            "Name": "",
                            "Price": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/South_Indian_non-veg_Meals.jpg/800px-South_Indian_non-veg_Meals.jpg",
                            "Name": "",
                            "Price": "",
                            "Description": "",
                        },
                    ],
                    "Gallery": [
                        {
                            "Category": "Events",
                            "Required": True,
                            "Images": [
                                "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8ZXZlbnR8ZW58MHx8MHx8fDA%3D"
                            ],
                        },
                        {
                            "Category": "Restaurants",
                            "Required": True,
                            "Images": [
                                "https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg"
                            ],
                        },
                        {
                            "Category": "Hotels",
                            "Required": True,
                            "Images": [
                                "https://cdn.britannica.com/96/115096-050-5AFDAF5D/Bellagio-Hotel-Casino-Las-Vegas.jpg"
                            ],
                        },
                        {
                            "Category": "Nearby",
                            "Required": True,
                            "Images": [
                                "https://cdn.britannica.com/96/115096-050-5AFDAF5D/Bellagio-Hotel-Casino-Las-Vegas.jpg"
                            ],
                        },
                        {
                            "Category": "View",
                            "Required": True,
                            "Images": [
                                "https://cdn.britannica.com/96/115096-050-5AFDAF5D/Bellagio-Hotel-Casino-Las-Vegas.jpg"
                            ],
                        },
                        {
                            "Category": "Rooms",
                            "Required": True,
                            "Images": [
                                "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
                            ],
                        },
                        {
                            "Category": "Lobby",
                            "Required": True,
                            "Images": [
                                "https://novoxinc.com/cdn/shop/articles/novox_5_hotel_lobby_design_ideas_that_will_inspire-you_hero_image_1024x576px_1024x.jpg?v=1659361242"
                            ],
                        },
                        {
                            "Category": "Bar",
                            "Required": True,
                            "Images": [
                                "https://images.pexels.com/photos/63633/bar-local-cong-ireland-63633.jpeg"
                            ],
                        },
                        {
                            "Category": "Playzone",
                            "Required": True,
                            "Images": ["https://funcity.in/image/playzone4.jpeg"],
                        },
                    ],
                    "Services": [
                        {
                            "Title": "Service 1",
                            "Text": "",
                            "Image": "https://thumbs.dreamstime.com/b/all-you-need-waitress-uniform-delivering-tray-food-room-hotel-room-service-focus-tableware-waitress-174457737.jpg",
                        },
                        {
                            "Title": "Service 2",
                            "Text": "",
                            "Image": "https://media.istockphoto.com/id/139984085/photo/luggage-in-hotel-room.jpg?s=612x612&w=0&k=20&c=C8HVRQLlDmYiVOYczyxuYGYV39ekWXS6K1wqD77mp_k=",
                        },
                        {
                            "Title": "Service 3",
                            "Text": "",
                            "Image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Boon_Hotel_%2B_Spa_-_Sarah_Stierch_-_April_2019_-_9.jpg/800px-Boon_Hotel_%2B_Spa_-_Sarah_Stierch_-_April_2019_-_9.jpg",
                        },
                        {
                            "Title": "Service 4",
                            "Text": "",
                            "Image": "https://grandpalaceriga.com/wp-content/uploads/2015/04/Seasons-1_compressed-min.jpg",
                        },
                        {
                            "Title": "Service 5",
                            "Text": "",
                            "Image": "https://arcmaxarchitect.com/sites/default/files/resort_hotel_design_sample_-11.jpg",
                        },
                    ],
                    "Restaurant": [
                        {
                            "Heading": "Restaurant1",
                            "Image": "",
                            "Text": "",
                            "Timeslot": "",
                        }
                    ],
                    "Team": [],
                    "Nearby": [
                        {
                            "Image": "https://media-cdn.tripadvisor.com/media/photo-s/0f/6d/c1/00/mayfair-darjeeling.jpg",
                            "Place": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://media-cdn.tripadvisor.com/media/photo-s/04/2d/01/30/mayfair-darjeeling.jpg",
                            "Place": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://www.journeyera.com/wp-content/uploads/2020/05/best-hotels-in-agra-near-taj-mahal-with-view-47406152.jpg",
                            "Place": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://i0.wp.com/bangalorerealestates.in/wp-content/uploads/2015/06/d1.jpg?fit=1024%2C400&ssl=1",
                            "Place": "",
                            "Description": "",
                        },
                        {
                            "Image": "https://images.squarespace-cdn.com/content/v1/52da9677e4b03d314575985a/1425872191027-NAJO6DITOGJ9VCFOFB0C/Ramada+Downtown+Dubai+Hotel+near+Burj+Khalifa.jpg",
                            "Place": "",
                            "Description": "",
                        },
                    ],
                    "Blogs": [],
                    "Advertisnment": [
                        {
                            "Heading": "Head",
                            "Text": "text",
                            "Image": "Imagelink",
                            "Required": True,
                        }
                    ],
                    "PromotionalPopups": {
                        "Heading": "head",
                        "Text": "text",
                        "Image": "image",
                        "Required": True,
                    },
                    "SeoOptimisation": [
                        {
                            "PageName": "Home",
                            "Data": {
                                "Title": "Home Page",
                                "Description": "Home  description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "About",
                            "Data": {
                                "Title": "About Page",
                                "Description": "About description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Contact",
                            "Data": {
                                "Title": "Contact Page",
                                "Description": "Contact description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Nearby Attraction",
                            "Data": {
                                "Title": "Nearby Page",
                                "Description": "Nearby description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Facilities",
                            "Data": {
                                "Title": "Facilities Page",
                                "Description": "Facilities description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Gallery",
                            "Data": {
                                "Title": "Gallery Page",
                                "Description": "Gallery description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Rooms",
                            "Data": {
                                "Title": "Rooms Page",
                                "Description": "Rooms description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Reservations",
                            "Data": {
                                "Title": "Reservations",
                                "Description": "Reservations",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Terms and condition",
                            "Data": {
                                "Title": "Terms Page",
                                "Description": "Terms description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Services",
                            "Data": {
                                "Title": "Services Page",
                                "Description": "Services description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Restaurants",
                            "Data": {
                                "Title": "Restaurants Page",
                                "Description": "Restaurants description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Testimonials",
                            "Data": {
                                "Title": "Testimonials Page",
                                "Description": "Testimonials description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Teams",
                            "Data": {
                                "Title": "Teams Page",
                                "Description": "Teams description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Blogs",
                            "Data": {
                                "Title": "Blogs",
                                "Description": "Blogs description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Faq",
                            "Data": {
                                "Title": "Faq page",
                                "Description": "Blogs description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Cancellation",
                            "Data": {
                                "Title": "Terms and Condition",
                                "Description": "Blogs description",
                                "keyword": "Keyword",
                            },
                        },
                        {
                            "PageName": "Privacy",
                            "Data": {
                                "Title": "Privacy Policy",
                                "Description": "Privacy policy description",
                                "keyword": "Keyword",
                            },
                        },
                    ],
                    "Location": getGoogleEmbeddedCode(maintain_data),
                    "NewsletterData": [],
                    "Reviews": {
                        "Write": "",
                        "Google": "",
                        "Tripadvisors": "",
                        "Instagram": "",
                        "Facebook": "",
                        "Clarity": "",
                        "TagManager": "",
                        "Console": "",
                        "Pixel": "",
                        "Analytics": "",
                        "Pagespeed": "",
                        # Add more key-value pairs as needed
                    },
                    "Contacts": [],
                    "SectionsVisible": {
                        "Home": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "About": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Rooms": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Blogs": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Gallery": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Facility": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Contact": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Reservation": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Booking": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Nearby": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Restaurant": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Spa": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Faq": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Services": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Teams": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "TermsConditions": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                        "Testimonial": {
                            "Banner": True,
                            "Rooms": True,
                            "Facilities": True,
                            "Nearby": True,
                            "HotelAd": True,
                            "YoutubeVideo": True,
                            "Insta": True,
                            "Testimonials": True,
                            "AboutUs": True,
                            "Images": True,
                            "Map": True,
                            "Whatsapp": True,
                            "Teams": True,
                            "Blogs": True,
                        },
                    },
                    "DataToarrange": [
                        {
                            "Heading": "Things To Do",
                            "Text": "Right Here Data",
                            "Images": [
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                            ],
                        },
                        {
                            "Heading": "The Restaurant",
                            "Text": "Right Here Data",
                            "Images": [
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                            ],
                        },
                        {
                            "Heading": "The Dining",
                            "Text": "Right Here Data",
                            "Images": [
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                            ],
                        },
                        {
                            "Heading": "How To find Hotel",
                            "Text": "Right Here Data",
                            "Images": [
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                            ],
                        },
                        {
                            "Heading": "Contact Query",
                            "Text": "Right Here Data",
                            "Images": [
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                            ],
                        },
                        {
                            "Heading": "Arranged Data",
                            "Text": "Right Here Data",
                            "Images": [
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                            ],
                        },
                        {
                            "Heading": "Arrange",
                            "Text": "Right Here Data",
                            "Images": [
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                            ],
                        },
                        {
                            "Heading": "Scheme_code",
                            "Text": "<script></script>",
                            "Images": [
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                                {
                                    "Image": images[random.randint(0, len(images) - 1)],
                                    "Heading": "",
                                    "Text": "",
                                },
                            ],
                        },
                    ],
                    "Chefs": [
                        {
                            "Name": "Tim",
                            "Image": images[random.randint(0, len(images) - 1)],
                            "Text": "text",
                        }
                    ],
                    "Events": [],
                    "SectionTitles": {
                        "About": {"Title": "About", "Description": "Descrpition"},
                        "Rooms": {
                            "Title": "ROOMS ACCOMMODATION",
                            "Description": "Utmost Luxury at Mandrem Retreat Beach Resort",
                        },
                        "Nearby": {
                            "Title": "NEARBY PLACES",
                            "Description": "Explore Wonders of food, fashion, and forts, just steps away from your accommodation in Mandrem.",
                        },
                        "Gallery": {
                            "Title": "GALLERY",
                            "Description": "Explore our world captured through lenses",
                        },
                        "Facilities": {
                            "Title": "RESORT FACILITIES",
                            "Description": "Relax in comfort and style at your mandrem retreat with our facilities by the pool.",
                        },
                        "OurRooms": {
                            "Title": "OUR ROOMS",
                            "Description": "Comfortable Retreats for Every Traveller at SPARV resort in Mandrem.",
                        },
                        "Services": {
                            "Title": "Sevices",
                            "Description": "Service Description",
                        },
                        "Bookings": {
                            "Title": "Booking",
                            "Description": "Booking Description",
                        },
                        "Testimonial": {
                            "Title": "Testimonials",
                            "Description": "Testimonials Description",
                        },
                        "Insta": {"Title": "Insta", "Description": "Insta Description"},
                        "1": {"Title": "Checkin", "Description": "01:00 PM"},
                        "2": {"Title": "Checkout", "Description": "10:00 AM"},
                        "3": {"Title": "Rules", "Description": ""},
                        "4": {"Title": "", "Description": ""},
                        "5": {"Title": "", "Description": ""},
                        "6": {"Title": "", "Description": ""},
                        "7": {"Title": "", "Description": ""},
                        "8": {"Title": "", "Description": ""},
                    },
                    "PagesTitles": {
                        "About": {
                            "Title": "THE HOTEL",
                            "Description": "OUR PLACE, OUR SERVICES & OUR TEAM",
                            "Image": images[0],
                            "Video": "",
                        },
                        "Rooms": {
                            "Title": "ROOMS & SUITES",
                            "Description": "WHERE COMFORT MEETS CONVENIENCE",
                            "Image": images[1],
                            "Video": "",
                        },
                        "Nearby": {
                            "Title": "NEARBY PLACES",
                            "Description": "Explore Wonders of food, fashion, and forts, just steps away from your accommodation in Mandrem.",
                            "Image": images[2],
                            "Video": "",
                        },
                        "Gallery": {
                            "Title": "GALLERY",
                            "Description": "WHERE OPEN SKIES BECOME YOUR HORIZON",
                            "Image": images[3],
                            "Video": "",
                        },
                        "Facilities": {
                            "Title": "FACILITIES",
                            "Description": "ELEVATING YOUR EXPERIENCE",
                            "Image": images[4],
                            "Video": "",
                        },
                        "Our Rooms": {
                            "Title": "OUR ROOMS",
                            "Description": "Comfortable Retreats for Every Traveller at SPARV resort in Mandrem.",
                            "Image": images[5],
                            "Video": "",
                        },
                        "Contact": {
                            "Title": "CONTACT",
                            "Description": "OUR PLACE, OUR SERVICES & OUR TEAMS",
                            "Image": images[6],
                            "Video": "",
                        },
                        "Services": {
                            "Title": "Services",
                            "Description": "Service Description",
                            "Image": images[7],
                            "Video": "",
                        },
                        "Bookings": {
                            "Title": "Booking Here",
                            "Description": "Booking Description",
                            "Image": images[8],
                            "Video": "",
                        },
                        "Terms": {
                            "Title": "TERMS & CONDITIONS",
                            "Description": "THE PLACE, OUR SERVICES & OUR TEAM",
                            "Image": images[9],
                            "Video": "",
                        },
                        "Privacy": {
                            "Title": "PRIVACY POLICY",
                            "Description": "THE PLACE, OUR SERVICES & OUR TEAM",
                            "Image": images[10],
                            "Video": "",
                        },
                        "Cancellation": {
                            "Title": "CANCELLATION POLICY",
                            "Description": "THE PLACE, OUR SERVICES & OUR TEAM",
                            "Image": images[11],
                            "Video": "",
                        },
                        "Restaurant": {
                            "Title": "Restaurant",
                            "Description": "Restaurant Description",
                            "Image": images[12],
                            "Video": "",
                        },
                        "Teams": {
                            "Title": "Teams",
                            "Description": "Teams Description",
                            "Image": images[13],
                            "Video": "",
                        },
                        "Testimonial": {
                            "Title": "Testimonials",
                            "Description": "Testimonial Description",
                            "Image": images[14],
                            "Video": "",
                        },
                        "Blogs": {
                            "Title": "Blogs",
                            "Description": "Blogs Description",
                            "Image": images[15],
                            "Video": "",
                        },
                        "Faq": {
                            "Title": "Faq",
                            "Description": "Faq description",
                            "Image": images[16],
                            "Video": "",
                        },
                    },
                    "Slugs": {
                        "About": {
                            "Slug": "About",
                            "PageName": "about.html",
                            "SeoData": 1,
                            "sectionVisible": "About",
                            "PageTitle": "About",
                        },
                        "Contact": {
                            "Slug": "Contact",
                            "PageName": "contact.html",
                            "SeoData": 2,
                            "sectionVisible": "Contact",
                            "PageTitle": "Contact",
                        },
                        "Nearby_Attraction": {
                            "Slug": "Nearby-Attraction",
                            "PageName": "404.html",
                            "SeoData": 3,
                            "sectionVisible": "Nearby",
                            "PageTitle": "Nearby",
                        },
                        "Facilities": {
                            "Slug": "Facilities",
                            "PageName": "facility.html",
                            "SeoData": 4,
                            "sectionVisible": "Facility",
                            "PageTitle": "Facilities",
                        },
                        "Gallery": {
                            "Slug": "Gallery",
                            "PageName": "gallery1.html",
                            "SeoData": 5,
                            "sectionVisible": "Gallery",
                            "PageTitle": "Gallery",
                        },
                        "Rooms": {
                            "Slug": "Rooms",
                            "PageName": "rooms-category.html",
                            "SeoData": 6,
                            "sectionVisible": "Rooms",
                            "PageTitle": "Rooms",
                        },
                        "Reservations": {
                            "Slug": "Reservations",
                            "PageName": "404.html",
                            "SeoData": 7,
                            "sectionVisible": "Reservation",
                            "PageTitle": "Gallery",
                        },
                        "Services": {
                            "Slug": "Services",
                            "PageName": "404.html",
                            "SeoData": 9,
                            "sectionVisible": "Services",
                            "PageTitle": "Services",
                        },
                        "Restaurants": {
                            "Slug": "Restaurants",
                            "PageName": "404.html",
                            "SeoData": 10,
                            "sectionVisible": "Restaurant",
                            "PageTitle": "Restaurant",
                        },
                        "Testimonials": {
                            "Slug": "Testimonials",
                            "PageName": "404.html",
                            "SeoData": 11,
                            "sectionVisible": "Testimonial",
                            "PageTitle": "Testimonial",
                        },
                        "Teams": {
                            "Slug": "Teams",
                            "PageName": "404.html",
                            "SeoData": 12,
                            "sectionVisible": "Teams",
                            "PageTitle": "Teams",
                        },
                        "Blogs": {
                            "Slug": "Blogs",
                            "PageName": "404.html",
                            "SeoData": 13,
                            "sectionVisible": "Blogs",
                            "PageTitle": "Blogs",
                        },
                        "Faq": {
                            "Slug": "Faq",
                            "PageName": "404.html",
                            "SeoData": 14,
                            "sectionVisible": "Faq",
                            "PageTitle": "Faq",
                        },
                        "Privacy": {
                            "Slug": "Privacy-Policy",
                            "PageName": "privacy.html",
                            "SeoData": 8,
                            "sectionVisible": "About",
                            "PageTitle": "Privacy",
                        },
                        "Terms_and_condition": {
                            "Slug": "Terms-And-Conditions",
                            "PageName": "terms.html",
                            "SeoData": 8,
                            "sectionVisible": "About",
                            "PageTitle": "Terms",
                        },
                        "Cancellation": {
                            "Slug": "Cancellation-Policy",
                            "PageName": "cancellation.html",
                            "SeoData": 15,
                            "sectionVisible": "About",
                            "PageTitle": "Cancellation",
                        },
                    },
                    "Colors": {
                        "backgroundColor": maintain_data.get("colorCombination").get(
                            "backgroundColor"
                        ),
                        "buttonColor": maintain_data.get("colorCombination").get(
                            "buttonColor"
                        ),
                        "fontColor": maintain_data.get("colorCombination").get(
                            "fontColor"
                        ),
                        "boardColor": maintain_data.get("colorCombination").get(
                            "boardColor"
                        ),
                        "fontfamily": "Times New Roman",
                    },
                },
            }
    }

    for location_id, hotel in obj["hotels"].items():
        # Initialize nested dict if it doesn't exist
        hotel.setdefault("Details", {})
        hotel["Details"].setdefault("Links", {})
        hotel["Details"].setdefault("Images", [])

        # Add social media links
        for social_item in socialMedia:
            for key, value in social_item.items():
                capitalized_key = key[0].upper() + key[1:]
                hotel["Details"]["Links"][capitalized_key + "Required"] = True
                hotel["Details"]["Links"][capitalized_key] = value

        # Add images
        for img_url in images:
            hotel["Details"]["Images"].append({"Image": img_url})

    # SETTING SOCIAL MEDIA URLs
    # for val in socialMedia:
    #     for key in val.keys():
    #         value = val[key]
    #         obj['hotels']["Details"]["Links"][key[0].upper() + key[1:] + "Required"] = True
    #         obj["Details"]["Links"][key[0].upper() + key[1:]] = value

    # SETTING IMAGES
    # for img_url in images:
    #     obj["Details"]["Images"].append({"Image": img_url})
    # data_to_create_for_bookingengine(ndid,locationid,maintain_data,images,obj["Details"]["Links"])
    db.WebsiteData.insert_one(obj)


def data_to_create_for_bookingengine(ndid, hId, maintain_data):
    # if (maintain_data.get("oldWebsite")==""):
    socialMedia = []
    socialmedia = [
        "twitter",
        "facebook",
        "instagram",
        "linkedin",
        "youtube",
        "pinterest",
        "reddit",
        "tumblr",
        "snapchat",
        "whatsapp",
        "tripadvisor",
    ]
    for obj in socialmedia:
        socialMedia.append(
            {
                obj: f"https://www.{obj}.com/{maintain_data.get('hotelName').replace(' ', '')}"
            }
        )
    # else:
    #     socialMedia = extract_social_media_urls(maintain_data.get("oldWebsite"))
    link = {}
    for val in socialMedia:
        for key in val.keys():
            value = val[key]
            link[key[0].upper() + key[1:] + "Required"] = True
            link[key[0].upper() + key[1:]] = value
    img_count = 50
    images = createimage(maintain_data.get("category"), img_count)
    booking_engine = {
        "ndid": ndid,
        "hId": hId,
        "Details": {
            "HotelName": maintain_data.get("hotelName"),
            "BgImage": images[0],
            "Labels": {
                "ReserveBoard": "Reservation",
                "ReserveButton": "Look For Rooms",
                "ConfirmButton": "Book",
                "PayButton": "Pay Now",
            },
            "Colors": {
                "BackgroundColor": maintain_data.get("colorCombination").get(
                    "backgroundColor"
                ),
                "BoardColor": maintain_data.get("colorCombination").get("boardColor"),
                "FontColor": maintain_data.get("colorCombination").get("fontColor"),
                "ButtonColor": maintain_data.get("colorCombination").get("buttonColor"),
            },
            "Links": link,
            "Footer": {
                "Address": maintain_data.get("hotelAddress"),
                "Phone": maintain_data.get("hotelPhone"),
                "WhatsApp": maintain_data.get("hotelPhone"),
                "City": maintain_data.get("hotelCity"),
                "Email": maintain_data.get("hotelEmail"),
                "AboutText": "At our Hotel you will feel great to stay and have a good fun",
                "NewsLetterText": "Hi this text is for newsletter",
                "Logo": (
                    maintain_data.get("logo")
                    if (maintain_data.get("logo") != "")
                    else "https://www.nicepng.com/png/full/111-1111079_logo-templates-png-download-template-logo-png.png"
                ),
            },
            "Location": getGoogleEmbeddedCode(maintain_data),
            "AboutUs": "About us of booking engine",
            "PrivacyPolicy": "Privacy policy",
            "CancellationPolicy": "Cancellation policy",
            "TermsConditions": "TermsConditions policy",
            "Clarity": "",
            "isOnlinePayment": True,
            "isPayatHotel": False,
            "Gateway": {"Type": "", "SECRET_KEY": "", "API_KEY": ""},
            "isSemiPayment": False,
            "addTax": True,
        },
    }
    createRoom(maintain_data.get("roomCategories"), maintain_data.get("Token"), hId)
    db.BookingEngineData.insert_one(booking_engine)
    return True, "Booking Engine Created successfully"


def create_profile(ndid, hId, maintain_data, domain):
    current_date = datetime.now()
    future_date = current_date + timedelta(days=15)
    future_date_str = future_date.strftime("%y-%m-%d")
    obj = {
        "ndid": ndid,
        "domain": domain,
        "template": maintain_data.get("template", "1"),
        "plan": {
            "name": maintain_data.get("planName"),
            "activationDate": datetime.now().strftime("%y-%m-%d"),
            "expiryDate": future_date_str,
        },
        "onBoardinDate": datetime.now(),
        "hotelName": maintain_data.get("hotelName"),
        "hotelDescription": (
            maintain_data.get("hotelDescription")
            if (maintain_data.get("hotelDescription") != "")
            else "hotelDescription"
        ),
        "hotelEmail": maintain_data.get("hotelEmail"),
        "hotelPhone": maintain_data.get("hotelPhone"),
        "currency": maintain_data.get("currency"),
        # "hoteladdress": {
        #     "pinCode": maintain_data.get("hotelPinCode"),
        #     "city": maintain_data.get("hotelCity"),
        #     "State": maintain_data.get("hotelState"),
        #     "country": maintain_data.get("hotelCountry"),
        # },
        "isVerified": False,
        "dinabiteToken": {"access_token": "None"},
        "watiCreds": {"tenantId": "None", "watiAccessToken": "None"},
        "hotels": {
            hId: {
                # "location": maintain_data.get("hotelCity")
                # + " "
                # + maintain_data.get("hotelState"),
                # "pinCode": maintain_data.get("hotelPinCode"),
                "local": maintain_data.get("hotelAddress"),
                "city": maintain_data.get("hotelCity"),
                "state": maintain_data.get("hotelState"),
                "country": maintain_data.get("hotelCountry"),
                "pinCode": maintain_data.get("hotelPinCode"),
            }
        },
        "uId": ndid,
    }
    # Zucks_profile
    db.Zucks_profile.insert_one(obj)
    # print(obj)


def hotelLink(plan, ndid, hId, domain):
    plandetail = db.Zucks_plans.find_one({"planName": plan})
    links = db.Zucks_hotellinks.find()
    max = 0
    for i in links:
        if max < i.get("id"):
            max = i.get("id")

    obj = {
        "id": int(int(max) + 1),
        "ndid": ndid,
        "websiteLink": (
            "https://" + domain + ".eazotel.com"
            if plandetail.get("website")
            else "None"
        ),
        "bookingEngineLink": (
            "https://engine.eazotel.com?id=" + ndid + "&hid=" + hId
            if plandetail.get("bookingEngine")
            else "None"
        ),
        "dashboardLink": "None",
    }
    db.Zucks_hotellinks.insert_one(obj)
    print(obj)


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def create_otpStorage(ndid):
    # TODO
    # Zucks_otp_storage

    obj = {"ndid": ndid, "otp": generate_random_string(6)}
    db.Zucks_otp_storage.insert_one(obj)


def createOnlyBookingEgnine(maintain_data, locationid, ndid, domain):
    try:
        if checker(ndid):
            return False, "Booking Engine Already exists"
        img_count = 10
        # if maintain_data.get("oldWebsite") is None:
        arr = []
        socialmedia = [
            "twitter",
            "facebook",
            "instagram",
            "linkedin",
            "youtube",
            "pinterest",
            "reddit",
            "tumblr",
            "snapchat",
            "whatsapp",
            "tripadvisor",
        ]
        for obj in socialmedia:
            arr.append(
                {
                    obj: f"https://www.{obj}.com/{maintain_data.get('hotelName').replace(' ', '')}"
                }
            )
        # else:
        #     arr = extract_social_media_urls(maintain_data.get("oldWebsite"))
        link = {}
        for val in arr:
            for key in val.keys():
                value = val[key]
                link[key[0].upper() + key[1:] + "Required"] = True
                link[key[0].upper() + key[1:]] = value
        images = createimage(maintain_data.get("category"), img_count)
        create_profile(ndid, locationid, maintain_data, domain)
        hotelLink(maintain_data.get("planName"), ndid, locationid, domain)
        create_otpStorage(ndid)
        data_to_create_for_bookingengine(ndid, locationid, maintain_data, images, link)
        return True, "Booking Engine Created successfully"
    except Exception as ex:
        logging.error(f"Error creating only engine {ex}")
        return False, "Booking Engine Not Created"


def updateDomain(ndId, hId, newDomain):
    # Zucks_profile, WebsiteData
    try:
        dashboardlink = db.Zucks_hotellinks.find_one({"ndid": ndId}).get(
            "dashboardLink"
        )
        db.Zucks_profile.find_one_and_update(
            {"ndid": ndId}, {"$set": {"domain": newDomain}}
        )
        db.WebsiteData.find_one_and_update(
            {"hId": hId, "ndid": ndId}, {"$set": {"Domain": newDomain}}
        )
        db.Zucks_hotellinks.find_one_and_update(
            {"ndid": ndId},
            {"$set": {"websiteLink": "https://" + newDomain + ".eazotel.com"}},
        )
        if dashboardlink != None:
            db.Zucks_hotellinks.find_one_and_update(
                {"ndid": ndId},
                {"$set": {"dashboardLink": "https://" + newDomain + ".com"}},
            )
        logging.error(
            f"Successfully updated domain hId {hId} ndid {ndId} newdomain {newDomain}"
        )
        return True, "Successfully updated domain"
    except Exception as ex:
        logging.error(f"Error while updating domain {ex}")
        return False, "Error while updating domain"


def deleteData(ndId, hId):
    try:
        print(ndId)
        db.BookingEngineData.find_one_and_delete({"hId": hId, "ndid": ndId})
        db.WebsiteData.find_one_and_delete({"hId": hId, "ndid": ndId})
        db.Zucks_hotellinks.find_one_and_delete({"ndid": ndId})
        db.Zucks_otp_storage.find_one_and_delete({"hId": hId, "ndid": ndId})
        db.Zucks_profile.find_one_and_delete({"uId": ndId})
        return True, "Deleted Successfully"
    except Exception as ex:
        return False, "Deletion Of Data Failed"


def getdomainTemplatenumber(domain):
    try:
        profile = db.Zucks_profile.find_one({"domain": domain})
        number = profile.get("template")
        return True, number
    except:
        return False, "None"


def getdomainMaintain(domain):
    try:
        data = db.WebsiteData.find_one({"Domain": domain})
        ismaintain = data.get("Maintainance")
        return True, ismaintain
    except:
        return False, False


def updatenumberoftemplate(maintenance_details):
    try:
        token = maintenance_details.get("token")
        template = maintenance_details.get("template")
        ndid = utils.get_ndid(token)

        profile = db.Zucks_profile.find_one_and_update(
            {"ndid": ndid}, {"$set": {"template": template}}
        )

        return True, "Template Number Updated Successfully"
    except:
        return False, "Template Number Updation Failed"


def addColorCombination(maintain_data):
    try:
        print(maintain_data)
        allval = db.WebsiteData.find()

        for obj in allval:
            hId = obj["hId"]
            ndid = obj["ndid"]
            db.WebsiteData.find_one_and_update(
                {"hId": hId, "ndid": ndid},
                {
                    "$set": {
                        "Details.Colors": {
                            "backgroundColor": maintain_data.get("color").get(
                                "backgroundColor"
                            ),
                            "buttonColor": maintain_data.get("color").get(
                                "buttonColor"
                            ),
                            "fontColor": maintain_data.get("color").get("fontColor"),
                            "boardColor": "#0A3A75",
                        }
                    }
                },
            )

            db.BookingEngineData.find_one_and_update(
                {"hId": hId, "ndid": ndid},
                {
                    "$set": {
                        "Details.Colors.FontColor": maintain_data.get("color").get(
                            "fontColor"
                        )
                    }
                },
            )

            print(ndid, hId)
        return True, "Success"
    except Exception as ex:
        return False, "Failed"


def changetemplateofDomain(maintenance_details):
    pagetitle = {
        "About": "About",
        "Contact": "Contact",
        "Nearby_Attraction": "Nearby",
        "Facilities": "Facilities",
        "Gallery": "Gallery",
        "Rooms": "Rooms",
        "Reservations": "Bookings",
        "Services": "Services",
        "Restaurants": "Restaurant",
        "Testimonials": "Testimonial",
        "Teams": "Teams",
        "Blogs": "Blogs",
        "Faq": "Faq",
        "Privacy": "Privacy",
        "Terms_and_condition": "Terms",
        "Cancellation": "Cancellation",
    }

    sectiontitle = {
        "About": "About",
        "Contact": "Contact",
        "Nearby_Attraction": "Nearby",
        "Facilities": "Facility",
        "Gallery": "Gallery",
        "Rooms": "Rooms",
        "Reservations": "Booking",
        "Services": "Services",
        "Restaurants": "Restaurant",
        "Testimonials": "Testimonial",
        "Teams": "Teams",
        "Blogs": "Blogs",
        "Faq": "Faq",
        "Privacy": "TermsConditions",
        "Terms_and_condition": "TermsConditions",
        "Cancellation": "TermsConditions",
    }

    seodata = {
        "About": 1,
        "Contact": 2,
        "Nearby_Attraction": 3,
        "Facilities": 4,
        "Gallery": 5,
        "Rooms": 6,
        "Reservations": 7,
        "Services": 9,
        "Restaurants": 10,
        "Testimonials": 11,
        "Teams": 12,
        "Blogs": 13,
        "Faq": 14,
        "Privacy": 8,
        "Terms_and_condition": 8,
        "Cancellation": 15,
    }

    try:
        token = maintenance_details.get("Token")
        ndid = utils.get_ndid(token)
        template = maintenance_details.get("template")

        temp1 = {
            "About": "about.html",
            "Contact": "contact.html",
            "Nearby_Attraction": "404.html",
            "Facilities": "facility.html",
            "Gallery": "gallery1.html",
            "Rooms": "rooms-category.html",
            "Reservations": "404.html",
            "Services": "404.html",
            "Restaurants": "404.html",
            "Testimonials": "404.html",
            "Teams": "404.html",
            "Blogs": "404.html",
            "Faq": "404.html",
            "Privacy": "privacy.html",
            "Terms_and_condition": "terms.html",
            "Cancellation": "cancellation.html",
        }

        temp2 = {
            "About": "404.html",
            "Contact": "contact.html",
            "Nearby_Attraction": "nearby.html",
            "Facilities": "404.html",
            "Gallery": "gallery.html",
            "Rooms": "rooms.html",
            "Reservations": "booking.html",
            "Services": "services.html",
            "Restaurants": "restaurant.html",
            "Testimonials": "404.html",
            "Teams": "404.html",
            "Blogs": "404.html",
            "Faq": "404.html",
            "Privacy": "privacy.html",
            "Terms_and_condition": "terms.html",
            "Cancellation": "cancellation.html",
        }

        temp3 = {
            "About": "about-us.html",
            "Contact": "contact-us-hotel.html",
            "Nearby_Attraction": "nearby.html",
            "Facilities": "404.html",
            "Gallery": "gallery.html",
            "Rooms": "rooms.html",
            "Reservations": "404.html",
            "Services": "404.html",
            "Restaurants": "404.html",
            "Testimonials": "404.html",
            "Teams": "404.html",
            "Blogs": "404.html",
            "Faq": "404.html",
            "Privacy": "privacy.html",
            "Terms_and_condition": "terms.html",
            "Cancellation": "cancellation.html",
        }

        temp4 = {
            "About": "about.html",
            "Contact": "contact.html",
            "Nearby_Attraction": "nearby.html",
            "Facilities": "activity.html",
            "Gallery": "gallery.html",
            "Rooms": "rooms.html",
            "Reservations": "404.html",
            "Services": "glamper.html",
            "Restaurants": "parkcafe.html",
            "Testimonials": "404.html",
            "Teams": "404.html",
            "Blogs": "blog.html",
            "Faq": "404.html",
            "Privacy": "privacy.html",
            "Terms_and_condition": "terms.html",
            "Cancellation": "cancellation.html",
        }

        temp5 = {
            "About": "about.html",
            "Contact": "contact.html",
            "Nearby_Attraction": "nearby.html",
            "Facilities": "facilities.html",
            "Gallery": "gallery.html",
            "Rooms": "room.html",
            "Reservations": "404.html",
            "Services": "404.html",
            "Restaurants": "404.html",
            "Testimonials": "404.html",
            "Teams": "404.html",
            "Blogs": "blog.html",
            "Faq": "404.html",
            "Privacy": "privacy.html",
            "Terms_and_condition": "terms.html",
            "Cancellation": "cancellation.html",
        }

        temp6 = {
            "About": "about-us.html",
            "Contact": "contact.html",
            "Nearby_Attraction": "nearby.html",
            "Facilities": "facilities.html",
            "Gallery": "gallery.html",
            "Rooms": "rooms.html",
            "Reservations": "404.html",
            "Services": "404.html",
            "Restaurants": "404.html",
            "Testimonials": "404.html",
            "Teams": "404.html",
            "Blogs": "blog.html",
            "Faq": "404.html",
            "Privacy": "privacy.html",
            "Terms_and_condition": "terms.html",
            "Cancellation": "cancellation.html",
        }

        if template == "1":
            temp = temp1
        if template == "2":
            temp = temp2
        if template == "3":
            temp = temp3
        if template == "4":
            temp = temp4
        if template == "5":
            temp = temp5
        if template == "6":
            temp = temp6

        # print(temp)
        for t in temp:
            db.WebsiteData.find_one_and_update(
                {"ndid": ndid},
                {
                    "$set": {
                        "Details.Slugs." + t + ".PageName": temp[t],
                        "Details.Slugs." + t + ".PageTitle": pagetitle[t],
                        "Details.Slugs." + t + ".sectionVisible": sectiontitle[t],
                        "Details.Slugs." + t + ".SeoData": seodata[t],
                    }
                },
            )

        # update profile
        db.Zucks_profile.find_one_and_update(
            {"uId": ndid}, {"$set": {"template": template}}
        )
        return True
    except:
        return False


def changeMaintenance(data):
    try:
        db.WebsiteData.find_one_and_update(
            {"ndid": data.get("ndid"), "hId": data.get("hId")},
            {"$set": {"Maintainance": data.get("maintainance")}},
        )
        return True
    except Exception as ex:
        return False


def addInClientQuery(data):
    try:
        data["clientQueryId"] = shortuuid.uuid()
        data["flag"] = False
        data["remark"] = ""
        data["nextFollowUp"] = ""
        data["followUp"] = ""
        data["Stage"] = {
            "demoschedule": False,
            "messageSent": False,
            "OTAListing": False,
            "sentProposal": False,
        }
        db.EazotelClientQuery.insert_one(data)

        return True
    except Exception as ex:
        return False


def addContactsAndMail(data):
    try:
        Domain = data.get("Domain")
        email = data.get("email")
        Name = data.get("Name")
        Contact = data.get("Contact")
        Subject = data.get("Subject")
        Description = data.get("Description")
        created_from = data.get("created_from")

        profile = db.Zucks_profile.find_one({"domain": Domain})
        db.ContactUs.insert_one(
            {
                "ndid": profile.get("uId"),
                "Name": Name,
                "Contact": Contact,
                "Email": email,
                "Subject": Subject,
                "Message": Description,
                "Created_at": datetime.now(timezone.utc).isoformat(
                    timespec="milliseconds"
                ),
                "created_from": created_from,
                "status": "Open",
                "updated_at": datetime.now(timezone.utc).isoformat(
                    timespec="milliseconds"
                ),
                "is_convertable": True,
                "is_converted": False,
                "converted_by": "",
                "Remark": "",
            }
        )

        mail_usecase.sendContactUsQueryMail(
            profile.get("hotelName"),
            profile.get("hotelEmail"),
            Name,
            Contact,
            email,
            Subject,
            Description,
            created_from,
        )

        return True
    except:
        return False


def get_contact_us_queries(token, status_filter, name):
    try:
        ndid = utils.get_ndid(token)
        search_query = {"ndid": ndid}
        if status_filter:
            search_query["status"] = status_filter

        if name:
            search_query["$or"] = [
                {"Name": {"$regex": name, "$options": "i"}},
                {"Email": {"$regex": name, "$options": "i"}},
            ]

        queries = db.ContactUs.find(search_query)
        queries_list = []
        count = 0
        for query in queries:
            query["_id"] = str(query["_id"])
            queries_list.append(query)
            count = count + 1

        return True, queries_list, count

    except:
        return False, [], 0


def ReplyContactsAndMail(data):
    try:
        Token = data.get("Token")
        ndid = utils.get_ndid(Token)
        email = data.get("email")
        Name = data.get("Name")
        Contact = data.get("Contact")
        Subject = data.get("Subjec")
        Description = data.get("Description")
        reply = data.get("Reply")

        profile = db.Zucks_profile.find_one({"uId": ndid})

        mail_usecase.sendContactUsQueryReplyMail(
            profile.get("hotelName"),
            profile.get("hotelEmail"),
            Name,
            Contact,
            email,
            Subject,
            Description,
            reply,
        )

        return True
    except:
        return False


def delete_contact_queries(data):

    Token = data.get("token")
    ndid = utils.get_ndid(Token)
    id = data.get("id")

    # q = db.ContactUs.find_one({"ndid": ndid, "_id": ObjectId(id)})

    # print(q)
    db.ContactUs.find_one_and_delete({"ndid": ndid, "_id": ObjectId(id)})

    # print(ndid)

    return True, "Query deleted successfully"


def edit_status_contact_queries(data):
    Token = data.get("token")
    ndid = utils.get_ndid(Token)

    db.ContactUs.find_one_and_update(
        {"ndid": ndid, "_id": ObjectId(data.get("id"))},
        {"$set": {"status": data.get("status")}},
    )

    return True, "Query updated successfully"


def update_master_data_add_checkin_and_checkout_date():

    print("hbsjfds")

    update_result = db.Zucks_users.update_many(
        {
            # "ndid": "e50d8dc6-4cfc-4c87-b6c0-145ccdeb4121",
            "isAdmin": True,
        },  # Empty filter = all documents
        {
            "$set": {
                "accessScope.leadgenform": False,
                "accessScope.conversationaltool": False,
                "accessScope.eazobot": False,
                "accessScope.usermanagement": False,
                "accessScope.emailmarketing": False,
                "accessScope.whatsappmarketing": False,
                "accessScope.smsmarketing": False,
                "accessScope.analyticsandreporting": False,
            }
        },
    )
    return True, "Master data updated successfully"
