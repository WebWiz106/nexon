import utils
import constants
import pymongo
import json
import settings
import logging

from bson import json_util
from usecases import mail_usecase


from datetime import datetime, date, timedelta, timezone

logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)


from utils import db


def domainofToken(token):
    ndid = utils.get_ndid(token)
    profile = db.Zucks_profile.find_one({"uId": ndid})
    return profile.get("domain")


# *==========================================================EDIT NAVBAR=========================================================
def EditNavbarQuery(edit_details):

    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        key = edit_details.get("key")
        value = edit_details.get("value") == "true"

        data = db.WebsiteData.find_one({"Domain": domain})

        toupdate = data["Details"].get("Navbar")
        toupdate[key] = value

        updateValues = {"$set": {"Details.Navbar": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True, "Navbar Updated"

    except:
        return False, "Error Occured during Edit Navbar"


# *==========================================================END EDIT NAVABAR=====================================================


# *==========================================================EDIT FACILITIES=================================================
def EditFacilitiesQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        key = edit_details.get("key")
        value = edit_details.get("value") == "true"

        data = db.WebsiteData.find_one({"Domain": domain})

        toupdate = data["Details"].get("Facilities")
        toupdate[key] = value

        updateValues = {"$set": {"Details.Facilities": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True, "Facilities Updated"

    except:
        return False, "Error Occured during Edit Facilities"


# *==========================================================END EDIT FACILITIES=========================================================


# *==========================================================ADD DELETE BANNER =========================================================
def AddDeleteBannerQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        operation = edit_details.get("operation")
        Heading = edit_details.get("Heading")
        subheading = edit_details.get("subheading")
        url = edit_details.get("url")
        video = edit_details.get("video")
        index = edit_details.get("index", "0")

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"].get("Banner")

        listToAdd = {
            "Heading": Heading,
            "Subhead": subheading,
            "url": url,
            "video": video,
        }
        if operation == "append":
            toupdate += [listToAdd]
            updateValues = {"$set": {"Details.Banner": toupdate}}
            updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
            return True, "Banner Added Successfully"

        else:
            toupdate.pop(int(index))
            updateValues = {"$set": {"Details.Banner": toupdate}}
            updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
            return True, "Banner Deleted Successfully"
    except:
        return False


# *==========================================================END ADD DELETE BANNER =========================================================
# *==========================================================EDIT BANNER =========================================================
def EditBannerQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        index = str(edit_details.get("removeindex"))
        image = edit_details.get("editImage")
        text = edit_details.get("edittext")
        subheading = edit_details.get("editsubhead")
        video = edit_details.get("editvideo")

        uploaddata = {
            "Heading": text,
            "Subhead": subheading,
            "url": image,
            "video": video,
        }
        updateValues = {"$set": {"Details.Banner." + index: uploaddata}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True, "Banner Edited Successfully"
    except:
        return False


# *==========================================================END EDIT BANNER =========================================================


# *==========================================================ADD DELETE IMAGES =========================================================
def AddDeleteImagesQuery(edit_details):  # append , delete
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        operation = edit_details.get("operation")
        imageurl = edit_details.get("imageurl")
        index = edit_details.get("index", "0")

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"]["Images"]
        listToAdd = {"Image": imageurl}
        if operation == "append":
            toupdate += [listToAdd]
            updateValues = {"$set": {"Details.Images": toupdate}}

        else:
            toupdate.pop(int(index))
            updateValues = {"$set": {"Details.Images": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True
    except:
        return False


# *==========================================================END ADD DELETE IMAGES================================================================
# *==========================================================EDIT IMAGES =================================================================
def EditImagesQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        index = str(edit_details.get("index"))
        image = edit_details.get("image")

        updateValues = {"$set": {"Details.Images." + index: {"Image": image}}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True
    except:
        return False


# *==========================================================END EDIT IMAGES================================================================


# *==========================================================EDIT HOTELAD================================================================
def EditHotelAd(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        heading = edit_details.get("heading")
        image = edit_details.get("image")
        video = edit_details.get("video")

        updateValues = {
            "$set": {
                "Details.HotelAdvr": {
                    "heading": heading,
                    "Image": image,
                    "video": video,
                }
            }
        }

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True
    except:
        return False


# *==========================================================END EDIT HOTELAD================================================================


# *==========================================================EDIT LINKS STATUS================================================================
def EditLinksStatusQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        key = edit_details.get("key")
        value = edit_details.get("value")
        ndid = utils.get_ndid(token)

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"]["Links"]
        toupdate[key] = value

        updateValues = {"$set": {"Details.Links": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        # updateDb1 = db.BookingEngineData.update_one({"ndid":ndid},updateValues)

        return True
    except:
        return False


# *==========================================================END LINK STATUS================================================================


# *==========================================================EDIT LINKS VALUES================================================================
def EditLinksValueQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Facebook = edit_details.get("Facebook")
        Instagram = edit_details.get("Instagram")
        Twitter = edit_details.get("Twitter")
        Youtube = edit_details.get("Youtube")
        Linkedin = edit_details.get("Linkedin")
        Tripadvisors = edit_details.get("Tripadvisors")

        ndid = utils.get_ndid(token)

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"]["Links"]
        toupdate["Facebook"] = Facebook
        toupdate["Instagram"] = Instagram
        toupdate["Twitter"] = Twitter
        toupdate["Youtube"] = Youtube
        toupdate["Linkedin"] = Linkedin
        toupdate["Tripadvisors"] = Tripadvisors

        updateValues = {"$set": {"Details.Links": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        updateDb1 = db.BookingEngineData.update_many({"ndid": ndid}, updateValues)

        return True
    except:
        return False


# *==========================================================END EDIT LINKS VALUES================================================================


# *==========================================================EDIT FOOTER =================================================================
def EditFooterQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Address = edit_details.get("Address")
        Phone = edit_details.get("Phone")
        city = edit_details.get("city")
        email = edit_details.get("email")
        Abouttext = edit_details.get("Abouttext")
        logo = edit_details.get("logo")
        WhatsApp = edit_details.get("WhatsApp")
        NewsLetterText = edit_details.get("NewsLetterText")
        ndid = utils.get_ndid(token)

        toupdate = {
            "Address": Address,
            "Phone": Phone,
            "WhatsApp": WhatsApp,
            "NewsLetterText": NewsLetterText,
            "City": city,
            "Email": email,
            "AboutText": Abouttext,
            "Logo": logo,
        }
        updateValues = {"$set": {"Details.Footer": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        updateDb1 = db.BookingEngineData.update_many({"ndid": ndid}, updateValues)
        return True

    except:
        return False


# *==========================================================END EDIT FOOTER =================================================================


# *==========================================================EDIT ABOUT================================================================
def EditAboutQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        heading = edit_details.get("heading")
        Text = edit_details.get("Text")
        url = edit_details.get("url")
        video_url = edit_details.get("video_url")

        update = {"Heading": heading, "Text": Text, "url": url, "video_url": video_url}
        updateValues = {"$set": {"Details.About": update}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True

    except:
        return False


# *==========================================================END EDIT ABOUT================================================================


# *==========================================================EDIT PAGES TITLES================================================================
def EditPagesTitlesQuery(edit_details):  # check pls
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        key = edit_details.get("key")
        Title = edit_details.get("Title")
        Description = edit_details.get("Description")
        Image = edit_details.get("Image")
        Video = edit_details.get("Video")
        try:
            updateValues = {
                "$set": {
                    "Details.PagesTitles."
                    + key: {
                        "Title": Title,
                        "Description": Description,
                        "Image": Image,
                        "Video": Video,
                    }
                }
            }

            updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
            return True

        except:
            return False
    except:
        return False


# *==========================================================END EDIT PAGES TITLES =================================================================


# *==========================================================EDIT ENGINE =================================================================
def EditEngineQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        newlink = edit_details.get("newLink")

        updateValues = {"$set": {"Details.Engine": newlink}}
        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True

    except:
        return False


# *==========================================================END EDIT ENGINE =================================================


# *==========================================================ADD DELETE FAQS =================================================
def AddDeleteFaqQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        operation = edit_details.get("operation")
        question = edit_details.get("question")
        answer = edit_details.get("answer")
        index = edit_details.get("index", "0")

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"]["Faq"]
        listToAdd = {"Question": question, "Answer": answer}
        if operation == "append":
            toupdate += [listToAdd]
            updateValues = {"$set": {"Details.Faq": toupdate}}
        else:
            toupdate.pop(int(index))
            updateValues = {"$set": {"Details.Faq": toupdate}}
        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END ADD DELETE FAQS================================================================


# *==========================================================EDIT FAQS================================================================
def EditFaqQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        question = edit_details.get("question")
        answer = edit_details.get("answer")
        index = edit_details.get("index")

        updateValues = {
            "$set": {"Details.Faq." + index: {"Question": question, "Answer": answer}}
        }

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True
    except:
        return False


# *==========================================================END EDIT FAQS================================================================


# *==========================================================ADD DELETE MENU================================================================
def AddDeleteMenuQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        operation = edit_details.get("operation")
        image = edit_details.get("image")
        name = edit_details.get("name")
        price = edit_details.get("price")
        Description = edit_details.get("Description")
        index = edit_details.get("index", "0")

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"]["Menu"]
        listToAdd = {
            "Image": image,
            "Name": name,
            "Price": price,
            "Description": Description,
        }
        if operation == "append":
            toupdate += [listToAdd]
            updateValues = {"$set": {"Details.Menu": toupdate}}
        else:
            toupdate.pop(int(index))
            updateValues = {"$set": {"Details.Menu": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END ADD DELETE MENU================================================================


# *==========================================================EDIT MENU================================================================
def EditMenuQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        image = edit_details.get("image")
        name = edit_details.get("name")
        price = edit_details.get("price")
        Description = edit_details.get("Description")
        index = edit_details.get("index")

        updateValues = {
            "$set": {
                "Details.Menu."
                + index: {
                    "Image": image,
                    "Name": name,
                    "Price": price,
                    "Description": Description,
                }
            }
        }

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END EDIT MENU================================================================


# *==========================================================EDIT GALLERY================================================================
def EditGalleryQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        operation = edit_details.get("operation")
        category = edit_details.get("category")
        imageurl = edit_details.get("imageurl")

        if operation == "append":

            updateDb = db.WebsiteData.update_one(
                {"Domain": domain, "Details.Gallery.Category": category},
                {"$push": {"Details.Gallery.$.Images": imageurl}},
            )

        else:
            updateDb = db.WebsiteData.update_one(
                {"Domain": domain, "Details.Gallery.Category": category},
                {"$pull": {"Details.Gallery.$.Images": imageurl}},
            )
        return True
    except:
        return False


# *==========================================================END EDIT GALLERY================================================================


# *==========================================================EDIT GALLERY STATUS =================================================================
def EditGalleryStatusQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        action = edit_details.get("action")
        category = edit_details.get("category")

        if action == "true":

            updateDb = db.WebsiteData.update_one(
                {"Domain": domain, "Details.Gallery.Category": category},
                {"$set": {"Details.Gallery.$.Required": True}},
            )

        else:
            updateDb = db.WebsiteData.update_one(
                {"Domain": domain, "Details.Gallery.Category": category},
                {"$set": {"Details.Gallery.$.Required": False}},
            )
        return True
    except:
        return False


# *==========================================================END EDIT GALLERY STATUS =================================================================


# *==========================================================ADD DELETE SERVICES================================================================
def AddDeleteServicesQuery(edit_details):
    # try:
    logging.info(f"{edit_details}")
    token = edit_details.get("token")
    domain = domainofToken(token)
    operation = edit_details.get("operation")
    Title = edit_details.get("Title")
    Text = edit_details.get("Text")
    Image = edit_details.get("Image")
    index = edit_details.get("index", "0")

    data = db.WebsiteData.find_one({"Domain": domain})
    toupdate = data["Details"]["Services"]
    listToAdd = {"Title": Title, "Text": Text, "Image": Image}

    if operation == "append":
        toupdate += [listToAdd]
        updateValues = {"$set": {"Details.Services": toupdate}}

    else:
        toupdate.pop(int(index))
        updateValues = {"$set": {"Details.Services": toupdate}}

    updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
    return True


# except:
#     return False
# *==========================================================END ADD DELETE SEVICES================================================================


# *==========================================================EDIT SERVICES================================================================
def EditServicesQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Title = edit_details.get("Title")
        Text = edit_details.get("Text")
        Image = edit_details.get("Image")
        index = str(edit_details.get("index"))

        updateValues = {
            "$set": {
                "Details.Services."
                + index: {"Title": Title, "Text": Text, "Image": Image}
            }
        }
        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END EDIT SERVICES================================================================


# *==========================================================ADD DELETE TEAMS================================================================
def AddDeleteTeamsQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        operation = edit_details.get("operation")
        Name = edit_details.get("Name")
        Designation = edit_details.get("Designation")
        Text = edit_details.get("Text")
        url = edit_details.get("url")
        index = edit_details.get("index", "0")

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"]["Team"]
        listToAdd = {"Name": Name, "Designation": Designation, "Text": Text, "url": url}
        if operation == "append":
            toupdate += [listToAdd]
            updateValues = {"$set": {"Details.Team": toupdate}}

        else:
            toupdate.pop(int(index))
            updateValues = {"$set": {"Details.Team": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END ADD DELETE TEAMS================================================================


# *==========================================================EDIT TEAMS================================================================
def EditTeamQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Name = edit_details.get("Name")
        Designation = edit_details.get("Designation")
        Text = edit_details.get("Text")
        url = edit_details.get("url")
        index = edit_details.get("index")

        updateValues = {
            "$set": {
                "Details.Team."
                + index: {
                    "Name": Name,
                    "Designation": Designation,
                    "Text": Text,
                    "url": url,
                }
            }
        }
        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END EDIT TEAMS================================================================


# *==========================================================ADD DELETE NEARBY================================================================
def AddDeleteNearbyQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        operation = edit_details.get("operation")
        Image = edit_details.get("Image")
        Place = edit_details.get("Place")
        Description = edit_details.get("Description")
        index = edit_details.get("index", "0")

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"]["Nearby"]
        listToAdd = {"Image": Image, "Place": Place, "Description": Description}
        if operation == "append":
            toupdate += [listToAdd]
            updateValues = {"$set": {"Details.Nearby": toupdate}}

        else:
            toupdate.pop(int(index))
            updateValues = {"$set": {"Details.Nearby": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END ADD DELETE NEARBY================================================================


# *==========================================================EDIT NEARBY================================================================
def EditNearbyQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Image = edit_details.get("Image")
        Place = edit_details.get("Place")
        Description = edit_details.get("Description")
        index = str(edit_details.get("index"))

        updateValues = {
            "$set": {
                "Details.Nearby."
                + index: {"Image": Image, "Place": Place, "Description": Description}
            }
        }
        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END EDIT NEARBY================================================================


# *==========================================================ADD DELETE BLOGS================================================================
def AddDeleteBlogsQuery(edit_details):

    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        operation = edit_details.get("operation")
        Heading = edit_details.get("Heading")
        Image = edit_details.get("Image")
        Text = edit_details.get("Text")
        Slug = edit_details.get("Slug")
        # date = edit_details.get("date")
        index = edit_details.get("index", "0")

        data = db.WebsiteData.find_one({"Domain": domain})
        toupdate = data["Details"]["Blogs"]

        listToAdd = {
            "Image": Image,
            "Text": Text,
            "Heading": Heading,
            "Slug": Slug,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        }

        if operation == "append":
            toupdate += [listToAdd]
            updateValues = {"$set": {"Details.Blogs": toupdate}}

        else:
            toupdate.pop(int(index))
            updateValues = {"$set": {"Details.Blogs": toupdate}}

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except Exception as ex:
        logging.error(f"Error in AddDeleteBlogsQuery: {ex}")
        return False


# *==========================================================END ADD DELETE BLOGS================================================================


# *==========================================================EDIT BLOGS================================================================
def EditBlogsQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Heading = edit_details.get("Heading")
        Image = edit_details.get("Image")
        Text = edit_details.get("Text")
        Slug = edit_details.get("Slug")
        date = edit_details.get("date")
        index = edit_details.get("index")

        updateValues = {
            "$set": {
                "Details.Blogs."
                + index: {
                    "Heading": Heading,
                    "Image": Image,
                    "Text": Text,
                    "Slug": Slug,
                }
            }
        }
        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END EDIT BLOGS================================================================


# *==========================================================EDIT SEODATA================================================================
def EditSeoData(edit_details):  # page,title,description
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Page = edit_details.get("Page")
        Title = edit_details.get("Title")
        description = edit_details.get("description")
        keyword = edit_details.get("keyword")

        data = {"Title": Title, "Description": description, "keyword": keyword}
        updateDb = db.WebsiteData.update_one(
            {"Domain": domain, "Details.SeoOptimisation.PageName": Page},
            {"$set": {"Details.SeoOptimisation.$.Data": data}},
        )

        return True

    except:
        return False


# *==========================================================END EDIT SEODATA================================================================


# *==========================================================EDIT SLUGS================================================================
def EditSlugsData(edit_details):  # page,title,description
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Page = edit_details.get("Page")
        slug = edit_details.get("slug")

        updateDb = db.WebsiteData.update_one(
            {"Domain": domain, f"Details.Slugs.{Page}": {"$exists": True}},
            {"$set": {f"Details.Slugs.{Page}.Slug": slug}},
        )

        return True

    except:
        return False


# *==========================================================END EDIT SLUGS================================================================


# *==========================================================EDIT LOCATION================================================================
def EditLocationData(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        location = edit_details.get("location")
        ndid = utils.get_ndid(token)

        updateValues = {"$set": {"Details.Location": location}}
        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        # updateDb1 = db.BookingEngineData.update_one({"ndid":ndid},updateValues)

        return True

    except:
        return False


# *==========================================================END EDIT LOCATION================================================================


# *==========================================================EDIT SECTION TITLES================================================================
def EditSectionTitlesQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        key = edit_details.get("key")
        Title = edit_details.get("Title")
        Description = edit_details.get("Description")
        updateValues = {
            "$set": {
                "Details.SectionTitles."
                + key: {
                    "Title": Title,
                    "Description": Description,
                }
            }
        }

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True
    except:
        return False


# *==========================================================END EDIT SECTION TITLES================================================================


# *==========================================================EDIT TERMS AND CONDITIONS================================================================
def EditTermsAndConditionsQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Privacy = edit_details.get("Privacy")
        Cancellation = edit_details.get("Cancellation")
        TermsServices = edit_details.get("TermsServices")

        updateValues = {
            "$set": {
                "Details.TermsConditions.0": {"Privacy": Privacy},
                "Details.TermsConditions.1": {"Cancellation": Cancellation},
                "Details.TermsConditions.2": {"TermsServices": TermsServices},
            }
        }

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True
    except:
        return False


# *==========================================================END EDIT TERMS AND CONDITIONS================================================================


# *==========================================================ADD DELETE EVENTS================================================================
def AddDeleteEventsQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(
            token
        )  # Assuming domainofToken is a function that extracts the domain.
        operation = edit_details.get("operation")
        Image = edit_details.get("Image")
        Text = edit_details.get("Text")
        Heading = edit_details.get("Heading")
        Time = edit_details.get("Time")
        Location = edit_details.get("Location")
        Date = edit_details.get("Date")
        BookingUrl = edit_details.get("BookingUrl")
        index = int(edit_details.get("index", 0))  # Ensure index is an integer

        listToAdd = {
            "Image": Image,
            "Text": Text,
            "Heading": Heading,
            "Date": Date,
            "Time": Time,
            "Location": Location,
            "BookingUrl": BookingUrl,
        }

        if operation == "append":
            db.WebsiteData.update_one(
                {"Domain": domain}, {"$push": {"Details.Events": listToAdd}}
            )
        elif operation == "pop":
            db.WebsiteData.update_one(
                {"Domain": domain}, {"$unset": {f"Details.Events.{index}": 1}}
            )
            db.WebsiteData.update_one(
                {"Domain": domain}, {"$pull": {"Details.Events": None}}
            )
        else:
            raise ValueError("Unsupported operation")

        return True
    except Exception as e:
        logging.error(f"Error in AddDeleteEventsQuery: {e}")
        return False


# *==========================================================END ADD DELETE EVENTS================================================================


# *==========================================================EDIT EVENTS================================================================
def EditEventsQuery(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        Image = edit_details.get("Image")
        Text = edit_details.get("Text")
        Heading = edit_details.get("Heading")
        index = str(edit_details.get("index"))

        updateValues = {
            "$set": {
                "Details.Events."
                + index: {"Image": Image, "Text": Text, "Heading": Heading}
            }
        }

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)
        return True
    except:
        return False


# *==========================================================END EDIT EVENTS================================================================


# *==========================================================EDIT DATA TO ATTANGE================================================================
def EditDatatoarrange(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        index = edit_details.get("index")
        heading = edit_details.get("heading")
        text = edit_details.get("text")
        images = edit_details.get("images", "None")

        if images == "None":
            updateValues = {
                "$set": {
                    "Details.DataToarrange."
                    + index: {
                        "Heading": heading,
                        "Text": text,
                    }
                }
            }
        else:
            updateValues = {
                "$set": {
                    "Details.DataToarrange."
                    + index: {"Heading": heading, "Text": text, "Images": images}
                }
            }

        db.WebsiteData.find_one_and_update({"Domain": domain}, updateValues)

        return True
    except:
        return False


# *==========================================================END EDIT DATA TO ARRANGE================================================


# *==========================================================EDIT CHECK IN CHECKOUT RULES================================================
def EditCheckinCheckoutRules(edit_details):
    try:
        logging.info(f"{edit_details}")
        token = edit_details.get("token")
        domain = domainofToken(token)
        checkin = edit_details.get("checkin")
        checkout = edit_details.get("checkout")
        rules = edit_details.get("rules")

        updateValues = {
            "$set": {
                "Details.SectionTitles.1": {
                    "Title": "Check-in",
                    "Description": checkin,
                },
                "Details.SectionTitles.2": {
                    "Title": "Check-out",
                    "Description": checkout,
                },
                "Details.SectionTitles.3": {
                    "Title": "rules",
                    "Description": rules,
                },
            }
        }

        updateDb = db.WebsiteData.update_one({"Domain": domain}, updateValues)

        return True
    except:
        return False


# *==========================================================END EDIT CHECK IN CHECKOUT RULES ================================================


# *==========================================================GET ALL ROOMS================================================
def get_all_rooms(ndid):
    try:
        logging.info(f"{ndid}")
        rooms = db.Rooms.find({"ndid": ndid})
        return json.loads(json_util.dumps(rooms))
    except Exception as ex:
        logging.error(ex)
        return None


# *==========================================================END GET ALL ROOMS================================================


# *==========================================================GET WEBSITE DATA =================================================
def getWebsiteData(domain):
    try:
        logging.info(f"{domain}")
        data = db.WebsiteData.find_one({"Domain": domain})
        profile_data = db.Zucks_profile.find_one({"domain": domain})
        hotels_data = profile_data.get('hotels')
        hid = list(hotels_data.keys())[0]
        return data.get("ndid"), data.get("Details"), hid
    except:
        return None


def getWebsiteDataonNdid(ndid):
    try:
        logging.info(f"{ndid}")
        data = db.WebsiteData.find_one({"ndid": ndid})
        return data.get("ndid"), data.get("Details")
    except:
        return None


# *==========================================================END GET WEBSITE DATA =================================================


# ?=================================================Booking engine======================================


def edit_colors_engine(data):
    try:
        Token = data.get("Token")

        ndid = utils.get_ndid(Token)
        hId = data.get("hId")
        BackgroundColor = data.get("BackgroundColor")
        BoardColor = data.get("BoardColor")
        ButtonColor = data.get("ButtonColor")

        db.BookingEngineData.find_one_and_update(
            {"ndid": ndid, "hId": hId},
            {
                "$set": {
                    "Details.Colors": {
                        "BackgroundColor": BackgroundColor,
                        "BoardColor": BoardColor,
                        "ButtonColor": ButtonColor,
                    }
                }
            },
        )

        return True
    except:
        return False


def edit_labels_engine(data):
    try:
        Token = data.get("Token")

        ndid = utils.get_ndid(Token)
        hId = data.get("hId")
        ReserveBoard = data.get("ReserveBoard")
        ReserveButton = data.get("ReserveButton")
        ConfirmButton = data.get("ConfirmButton")
        PayButton = data.get("PayButton")

        db.BookingEngineData.find_one_and_update(
            {"ndid": ndid, "hId": hId},
            {
                "$set": {
                    "Details.Labels": {
                        "ReserveBoard": ReserveBoard,
                        "ReserveButton": ReserveButton,
                        "ConfirmButton": ConfirmButton,
                        "PayButton": PayButton,
                    }
                }
            },
        )

        return True
    except:
        return False


def edit_content_engine(data):
    try:
        Token = data.get("Token")

        ndid = utils.get_ndid(Token)
        hId = data.get("hId")
        aboutus = data.get("aboutus")
        privacy = data.get("privacy")
        cancellation = data.get("cancellation")
        TermsConditions = data.get("TermsConditions")

        db.BookingEngineData.find_one_and_update(
            {"ndid": ndid, "hId": hId},
            {
                "$set": {
                    "Details.AboutUs": aboutus,
                    "Details.PrivacyPolicy": privacy,
                    "Details.CancellationPolicy": cancellation,
                    "Details.TermsConditions": TermsConditions,
                }
            },
        )

        return True
    except:
        return False


def getuserTemplateInfo(token):
    try:
        ndid = utils.get_ndid(token)
        template = db.Zucks_profile.find_one({"uId": ndid}).get("template")
        templateDetail = db.Zucks_templates.find_one({"templateName": template})
        obj = {
            "Status": True,
            "Template": template,
            "Pages": {
                "dnid": templateDetail.get("dnid"),
                "templateName": templateDetail.get("templateName"),
                "home": templateDetail.get("home"),
                "about": templateDetail.get("about"),
                "rooms": templateDetail.get("rooms"),
                "hotelAdvr": templateDetail.get("hotelAdvr"),
                "termsCondition": templateDetail.get("termsCondition"),
                "services": templateDetail.get("services"),
                "restaurants": templateDetail.get("restaurants"),
                "gallery": templateDetail.get("gallery"),
                "testimonials": templateDetail.get("testimonials"),
                "teams": templateDetail.get("teams"),
                "blogs": templateDetail.get("blogs"),
                "menu": templateDetail.get("menu"),
                "contact": templateDetail.get("contact"),
                "facilities": templateDetail.get("facilities"),
                "nearbyPlaces": templateDetail.get("nearbyPlaces"),
            },
        }
        return True, obj
    except Exception as ex:
        return False, ex


def postReviewData(data):
    try:
        ndid = utils.get_ndid(data.get("Token"))
        db.WebsiteData.find_one_and_update(
            {"ndid": ndid},
            {
                "$set": {
                    "Details.Reviews.Clarity": data.get("Clarity"),
                    "Details.Reviews.Analytics": data.get("Analytics"),
                    "Details.Reviews.TagManager": data.get("TagManager"),
                    "Details.Reviews.Console": data.get("Console"),
                    "Details.Reviews.Pixel": data.get("Pixel"),
                    "Details.Reviews.Pagespeed": data.get("Pagespeed"),
                }
            },
        )

        return True
    except Exception as ex:
        return False


def getNavbarDetails(token):
    try:
        ndid = utils.get_ndid(token)
        query = []
        contact = []
        Newsletter = []
        DigitalCheckin = []
        querydb = db.Query_Clients.find({"ndid": ndid})
        for data in querydb:
            query.append(data)

        contactdb = db.ContactUs.find({"ndid": ndid})
        for data in contactdb:
            contact.append(data)

        Newsletterdb = db.Newsletters.find({"ndid": ndid})
        for data in Newsletterdb:
            Newsletter.append(data)

        DigitalCheckindb = db.DigitalCheckin.find({"ndid": ndid})
        for data in DigitalCheckindb:
            DigitalCheckin.append(data)

        obj = {
            "Status": True,
            "Hotels": db.WebsiteData.find_one({"ndid": ndid}).get("hotels",[]),
            "Queries": json.loads(json_util.dumps(query)),
            "Contact": json.loads(json_util.dumps(contact)),
            "Newsletter": json.loads(json_util.dumps(Newsletter)),
            "DigitalCheckin": json.loads(json_util.dumps(DigitalCheckin)),
        }
        return True, obj
    except Exception as ex:
        return False, None


def getUserProfile(token):
    try:
        ndid = utils.get_ndid(token)
        obj = {"Status": True, "Details": db.Zucks_profile.find_one({"uId": ndid})}
        user = db.Zucks_users.find_one({"ndid": ndid})
        obj["Details"].pop("_id")
        obj["Details"].pop("ndid")
        obj["Details"].pop("uId")
        obj["Details"].pop("onBoardinDate")
        obj["Details"].pop("template")
        obj["Details"].pop("hotels")
        obj["Details"]["emailId"] = user.get("emailId")
        obj["Details"]["userName"] = user.get("userName")
        obj["Details"]["displayName"] = user.get("displayName")
        return True, obj
    except Exception as ex:
        return False, None


def getHotelLinks(token):
    try:
        ndid = utils.get_ndid(token)
        links = db.Zucks_hotellinks.find_one({"ndid": ndid})
        obj = {
            "Status": True,
            "Details": {
                "websiteLink": (
                    links.get("websiteLink")
                    if links.get("dashboardLink") == "None"
                    else links.get("dashboardLink")
                ),
                "engineLink": links.get("bookingEngineLink"),
            },
        }
        return True, obj
    except Exception as ex:
        return False, None


def updateOffers(data):
    ndid = utils.get_ndid(data.get("token"))
    offer_detail = data.get("offer")
    db.WebsiteData.find_one_and_update(
        {"ndid": ndid}, {"$set": {"Details.Offers": offer_detail}}
    )
    return True
