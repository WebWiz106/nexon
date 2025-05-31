from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin

from usecases import cms, room_usecase

# cms_controller = Blueprint('cms', __name__)
cms_controller = Blueprint("cms", __name__)


@cms_controller.route("/hi")
def hello1():
    return {"Message": "Hi"}


# *================================================Navbar================================================
@cms_controller.route("/edit/Navbar", methods=["POST"])
def editNavbar():
    try:
        edit_details = request.get_json(force=True)
        status, message = cms.EditNavbarQuery(edit_details)
        return jsonify({"Status": status, "Message": message})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Facilities", methods=["POST"])
def editFacilities():
    try:
        edit_details = request.get_json(force=True)
        status, message = cms.EditFacilitiesQuery(edit_details)
        return jsonify({"Status": status, "Message": message})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================End Navbar================================================================

# *==================================================Banner for website=================================================


@cms_controller.route("/operation/Banner", methods=["POST"])
def addBanner():
    try:
        edit_details = request.get_json(force=True)
        status, message = cms.AddDeleteBannerQuery(edit_details)
        return jsonify({"Status": status, "Message": message})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Banner", methods=["POST"])
def editBanner():
    try:
        edit_details = request.get_json(force=True)
        status, message = cms.EditBannerQuery(edit_details)
        return jsonify({"Status": status, "Message": message})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *================================================End Banner for website===============================================


# *================================================Body Images for website===============================================
@cms_controller.route("/operation/Images", methods=["POST"])
def addImages():
    try:
        edit_details = request.get_json(force=True)  #
        status = cms.AddDeleteImagesQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Images", methods=["POST"])
def editImages():
    try:
        edit_details = request.get_json(force=True)  #
        status = cms.EditImagesQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *===============================================END Body Images for website===============================================


# *================================================Hotel-Ads for website====================================================
@cms_controller.route("/edit/hotelads", methods=["POST"])
def editHotelAds():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditHotelAd(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *================================================END Hotel-ads for website================================================
# *================================================Social-Links for website=================================================
@cms_controller.route("/edit/sociallinks/status", methods=["POST"])
def editSocialLinksStatus():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditLinksStatusQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/sociallinks", methods=["POST"])
def editSocialLinks():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditLinksValueQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *================================================END Social-Links for website==============================================


# *=======================================================Footer for website================================================
@cms_controller.route("/edit/footer", methods=["POST"])
def editFooter():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditFooterQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *======================================================END Footer for website==============================================


# *========================================================About for website==================================================
@cms_controller.route("/edit/aboutus", methods=["POST"])
def editAboutUs():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditAboutQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *=====================================================END About for website===============================================


# *===================================================Page Titles for website================================================
@cms_controller.route("/edit/pagetitles", methods=["POST"])
def editPagetitles():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditPagesTitlesQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Page Titles for website=============================================


# *==================================================Engine-Links for website================================================
@cms_controller.route("/edit/enginelink", methods=["POST"])
def editEngineLink():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditEngineQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==============================================End Engine-Links for website================================================


# *==================================================FAQ for website============================================
@cms_controller.route("/operation/Faq", methods=["POST"])
def addFaq():
    try:
        edit_details = request.get_json(force=True)  #
        status = cms.AddDeleteFaqQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Faq", methods=["POST"])
def editFaq():
    try:
        edit_details = request.get_json(force=True)  #
        status = cms.EditFaqQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END FAQ for website============================================


# *==================================================Menu for website============================================
@cms_controller.route("/operation/Menu", methods=["POST"])
def addMenu():
    try:
        edit_details = request.get_json(force=True)
        status = cms.AddDeleteMenuQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Menu", methods=["POST"])
def editMenu():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditMenuQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Menu for website============================================


# *==================================================Gallery for website============================================
@cms_controller.route("/edit/Gallery/Status", methods=["POST"])
def editGalleryStatus():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditGalleryStatusQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Gallery/Images", methods=["POST"])
def editGalleryImages():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditGalleryQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Gallery for website============================================


# *==================================================Services for website============================================
@cms_controller.route("/operation/Services", methods=["POST"])
def addServies():
    # try:
    edit_details = request.get_json(force=True)
    status = cms.AddDeleteServicesQuery(edit_details)
    return jsonify({"Status": status})


# except Exception as ex:
#     return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Services", methods=["POST"])
def editServices():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditServicesQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Services for website============================================


# *==================================================Teams for website============================================
@cms_controller.route("/operation/Teams", methods=["POST"])
def addTeams():
    try:
        edit_details = request.get_json(force=True)
        status = cms.AddDeleteTeamsQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Teams", methods=["POST"])
def editTeams():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditTeamQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Teams for website============================================


# *==================================================Nearby for website============================================
@cms_controller.route("/operation/Nearby", methods=["POST"])
def addNearby():
    try:
        edit_details = request.get_json(force=True)
        status = cms.AddDeleteNearbyQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Nearby", methods=["POST"])
def editNearby():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditNearbyQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Nearby for website============================================


# *==================================================Blogs for website============================================
@cms_controller.route("/operation/Blogs", methods=["POST"])
def addBlogs():
    try:
        edit_details = request.get_json(force=True)
        status = cms.AddDeleteBlogsQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Blogs", methods=["POST"])
def editBlogs():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditBlogsQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Blogs for website============================================


# *==================================================SEO-DATA for website============================================
@cms_controller.route("/edit/seo/seodata", methods=["POST"])
def editSeoData():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditSeoData(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/seo/slugs", methods=["POST"])
def editSlugs():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditSlugsData(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END SLUGS for website============================================


# *==================================================Locations for website============================================
@cms_controller.route("/edit/locationlink", methods=["POST"])
def editLocations():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditLocationData(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Locations for website============================================


# *==================================================Terms&Conditions for website============================================
@cms_controller.route("/edit/termsandconditions", methods=["POST"])
def editTermsAndConditions():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditTermsAndConditionsQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Terms&Conditions for website============================================


# *==================================================Data-to-arrange for website============================================
@cms_controller.route("/edit/dataarrange", methods=["POST"])
def editDatatoArrange():
    try:
        details = request.get_json(force=True)
        status = cms.EditDatatoarrange(details)
        return jsonify({"Status": status})
    except:
        return jsonify({"Status": False})


# *==================================================END Data-to-arrange for website============================================


# *==================================================Events for website============================================
@cms_controller.route("/operation/Events", methods=["POST"])
def addEvents():
    try:
        edit_details = request.get_json(force=True)
        status = cms.AddDeleteEventsQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


@cms_controller.route("/edit/Events", methods=["POST"])
def editEvents():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditEventsQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Events for website============================================


# *==================================================Section-Titles for website============================================
@cms_controller.route("/edit/sectiontitles", methods=["POST"])
def editSectionTitles():
    try:
        edit_details = request.get_json(force=True)
        status = cms.EditSectionTitlesQuery(edit_details)
        return jsonify({"Status": status})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500


# *==================================================END Section-Titles for website============================================


# *==================================================House Rules for website============================================
@cms_controller.route("/edit/houserules", methods=["POST"])
def editHouseRules():
    try:
        details = request.get_json(force=True)
        status = cms.EditCheckinCheckoutRules(details)
        return jsonify({"Status": status})
    except:
        return jsonify({"Status": False})


# *==================================================End House Rules for website============================================


# *==================================================Website for website============================================
@cms_controller.route("/get/website/<domain>", methods=["GET"])
def getWebsiteData(domain):
    try:
        ndid, websitedata, hid = cms.getWebsiteData(domain)
        return jsonify({"Status": True, "WebsiteData": websitedata, "ndid": ndid, "hid":hid})
    except:
        return jsonify({"Status": False})


@cms_controller.route("/get/website/ndid/<ndid>", methods=["GET"])
def getWebsiteDataNdid(ndid):
    try:
        did, websitedata = cms.getWebsiteDataonNdid(ndid)
        return jsonify({"Status": True, "WebsiteData": websitedata, "ndid": did})
    except:
        return jsonify({"Status": False})


# *==================================================END Website for website============================================


# ?==================================================Booking engine edit==================================================
@cms_controller.route("/edit/engine/labels", methods=["POST"])
def editEngineLabels():
    try:
        data = request.get_json(force=True)
        status = cms.edit_labels_engine(data)
        return jsonify({"Status": status})
    except:
        return jsonify({"Status": False})


@cms_controller.route("/edit/engine/content", methods=["POST"])
def editEngineContent():
    try:
        data = request.get_json(force=True)
        status = cms.edit_content_engine(data)
        return jsonify({"Status": status})
    except:
        return jsonify({"Status": False})


@cms_controller.route("/edit/engine/colors", methods=["POST"])
def editEngineColors():
    try:
        data = request.get_json(force=True)
        status = cms.edit_colors_engine(data)
        return jsonify({"Status": status})
    except:
        return jsonify({"Status": False})


@cms_controller.route("/get/UsertemplateDetail/<token>", methods=["GET"])
def getTemplateDetail(token):
    try:
        status, message = cms.getuserTemplateInfo(token)
        if status:
            return jsonify(message)
        return jsonify({"Status": False})
    except:
        return jsonify({"Status": False})


@cms_controller.route("/post/reviewsection", methods=["POST"])
def postreviewsection():
    try:
        data = request.get_json(force=True)
        status = cms.postReviewData(data)
        return jsonify({"Status": status})
    except:
        return jsonify({"Status": False})


@cms_controller.route("/get/navbar", methods=["GET"])
def getNavBarData():
    try:
        token = request.args.get("id") 
        print("token",token)
        status, obj = cms.getNavbarDetails(token)
        # print(obj)
        return jsonify(obj)
    except Exception as ex:
        return jsonify({"Status": False, "Message": "Some problem"})


@cms_controller.route("/get/userdetails", methods=["GET"])
def getUserDetails():
    try:
        token = request.args.get("id")
        status, obj = cms.getUserProfile(token)
        # print(status)
        if status:
            return jsonify(obj)
        return jsonify({"Status": False, "Message": "Error Occured"})
    except Exception as ex:
        return jsonify({"Status": False, "Message": "Some problem"})


@cms_controller.route("/get/links", methods=["GET"])
def getHotelLinks():
    try:
        token = request.args.get("id")
        status, obj = cms.getHotelLinks(token)
        # print(status)
        if status:
            return jsonify(obj)
        return jsonify({"Status": False, "Message": "Error Occured"})
    except Exception as ex:
        return jsonify({"Status": False, "Message": "Some problem"})


# =================Offers================
@cms_controller.route("/edit/offers", methods=["POST"])
def editOffers():
    try:
        details = request.get_json(force=True)
        status = cms.updateOffers(details)
        return jsonify({"Status": status})
    except:
        return jsonify({"Status": False})
