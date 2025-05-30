import utils
import hashlib
import pymongo
import settings
import logging
import json
import hashlib

from bson import json_util
from datetime import datetime
from model.user import User
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

from utils import db


def get_admin_profile(email):
    try:
        admin = db.Super_admins.find_one({"emailId":email})
        return admin
    except:
        return None
    
def get_admin_profile_from_token(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        admin = db.Super_admins.find_one({"emailId":email})
        return admin
    except:
        return None
    

def delete_admin_profile(email):
    try:
        admin = db.Super_admins.find_one_and_delete({"emailId":email})
        return True
    except:
        return False


def admin_is_owner(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile.get("owner")
    except:
        return False


def admin_have_client_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("clients")
    except:
        return False
    
def admin_have_templates_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("templates")
    except:
        return False

def admin_have_plans_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("plans")
    except:
        return False

def admin_have_seo_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("seo")
    except:
        return False

def admin_have_websites_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("websites")
    except:
        return False

def admin_have_data_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("data")
    except:
        return False
    
def admin_have_bookings_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("bookings")
    except:
        return False
    
def admin_have_domain_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("domain")
    except:
        return False
    
def admin_have_gateway_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("gateway")
    except:
        return False
    
def admin_have_profile_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("profile")
    except:
        return False
    
def admin_have_accessScope_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("accessScope")
    except:
        return False



def admin_have_seo_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("seo")
    except:
        return False

def admin_have_website_access(token):
    try:
        data = utils.getdata(token)
        email = data.get("emailId")
        adminProfile = get_admin_profile(email)
        return adminProfile["accessScope"].get("websites")
    except:
        return False


def login_super_admin(data):
    try:
        email = data.get("emailId")
        password = data.get("password")

        #hash password
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        try:
            status = True
            admin = db.Super_admins.find_one({"emailId":email,"password":password})

            token_payload = {
                "emailId":email
            }
            token = utils.create(token_payload)
        except:
            status = False
            admin = "-"
            token = "-"


        return status,token,admin
    except:
        return False,"-","-"


def add_super_admin(data):
    try:
        token = data.get("token")
        isOwner = admin_is_owner(token)

        if(isOwner==False):
            return False,"Admin Don't have permissions to add another admin"
        
        emailId = data.get("emailId")
        profile = get_admin_profile(emailId)
        if(profile!=None):
            return False,"Email Id already in use"


        username = data.get("username")
        password = data.get("password")
        phone = data.get("phone")
        team = data.get("team")
        owner = data.get("owner")
        accessScope = data.get("accessScope")

        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        

        db.Super_admins.insert_one({
            "username":username,
            "password":password,
            "emailId":emailId,
            "phone":phone,
            "team":team,
            "owner":owner=="true",
            "accessScope":{
                        "clients":accessScope.get("clients")=="true",
                        "templates":accessScope.get("templates")=="true",
                        "plans":accessScope.get("plans")=="true",
                        "seo":accessScope.get("seo")=="true",
                        "websites":accessScope.get("websites")=="true",
                        "data":accessScope.get("data")=="true",
                        "bookings":accessScope.get("bookings")=="true",
                        "accessScope": accessScope.get("accessScope")=="true",
                        "domain": accessScope.get("domain")=="true",
                        "gateway": accessScope.get("gateway")=="true",
                        "profile": accessScope.get("profile")=="true",
                        "templates": accessScope.get("templates")=="true"
            
            }
        })

        return True,"Admin Registered"
    except:
        return False,"Admin Not Registered"
    
def edit_super_admin(data):
    try:
        
        token = data.get("token")
        isOwner = admin_is_owner(token)


        if(isOwner==False):
            return False,"Admin Don't have permissions to edit another admin"
        
        emailId = data.get("emailId")
        profile = get_admin_profile(emailId)
        if(profile==None):
            return False,"Profile not found"
        


        username = data.get("username")
        password = data.get("password")
        phone = data.get("phone")
        team = data.get("team")
        owner = data.get("owner")
        accessScope = data.get("accessScope")

        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        db.Super_admins.find_one_and_update({"emailId":emailId},{"$set":{
            "username":username,
            "password":password,
            #"emailId":emailId,
            "phone":phone,
            "team":team,
            "owner":owner=="true",
            "accessScope":{
                        "clients":accessScope.get("clients")=="true",
                        "templates":accessScope.get("templates")=="true",
                        "plans":accessScope.get("plans")=="true",
                        "seo":accessScope.get("seo")=="true",
                        "websites":accessScope.get("websites")=="true",
                        "data":accessScope.get("data")=="true",
                        "bookings":accessScope.get("bookings")=="true",
                        "accessScope": accessScope.get("accessScope")=="true",
                        "domain": accessScope.get("domain")=="true",
                        "gateway": accessScope.get("gateway")=="true",
                        "profile": accessScope.get("profile")=="true",
                        "templates": accessScope.get("templates")=="true"
            
            }
        }})
        

        return True,"Admin data edited  successfully"
    except:
        return False,"Admin date Not edited"
    
    

def delete_super_admin(data):
    try:
        token = data.get("token")
        emailToDelete = data.get("emailId")
        isadmin = admin_is_owner(token)
        if(isadmin==False):
            return False,"Admin Don't have permissions to Delete another admin"

        profileOfEmail = get_admin_profile(emailToDelete)

        if(profileOfEmail.get("owner")):
            return False , "Owner can not be remove"
        
        else:
            delete_admin_profile(emailToDelete)
            return True , "Admin Deleted Successfully"
    except:
        return False , "Admin Not Deleted"
    

def getAllAdmins_super_admin(token):

    try:
        isadmin = admin_is_owner(token)
        
        if isadmin:
            admins = db.Super_admins.find()
            data = []
            for admin in admins:
                data.append(admin)
            return True,data
        
        else:
            return False,"No account exists"
    except:
        return False,[]


def getAllClients_super_admin(token):
    try:
        isadmin = admin_have_client_access(token)
        if isadmin:
            profiles = db.Zucks_profile.find()
            data = []
            for admin in profiles:
                links = db.Zucks_hotellinks.find_one({"ndid":admin.get("uId")})
                admin["websiteLink"] = links
                data.append(admin)
            return True,data
        
        else:
            return False,"Admin Don't Have access to see clients"
    except:
        return False,[]


def getAllClients_Seodata_super_admin(domain,token):
    try:
        isadmin = admin_have_seo_access(token)
        if isadmin:
            profiles = db.WebsiteData.find_one({"Domain":domain})
            seo_data = profiles["Details"].get("SeoOptimisation")
            slugs = profiles["Details"].get("Slugs")
            
            return True,"Data retrieved",seo_data,slugs
        
        else:
            return False,"Admin Don't Have access to see clients seo",[],[]
    except:
        return False,"Problem Occured",[],[]


def getAllClients_Websitedata_super_admin(token):
    try:
        isadmin = admin_have_website_access(token)
        if isadmin:
            websitedata = db.WebsiteData.find()

            websiteDatalist = []
            for data in websitedata:
                websiteDatalist.append(data)
            
            return True,"Data retrieved",websiteDatalist
        
        else:
            return False,"Admin Don't Have access to see clients website data",{}
    except:
        return False,"Some Problem Occured",{}
    

  

def getAllclient_OTADetails_super_admin(token):
    try:
        isadmin = admin_have_data_access(token)
        if isadmin:
            AllOTADetails = db.OTADetails.find()
            OTADetails = []
            for OTADetail in AllOTADetails:
                OTADetails.append(OTADetail)

            return True, "Data retrived",OTADetails
        else:
            return False,"Admin Don't Have access to see OTADetails ",[]
    except:
        return None,"message",[]


def getallUsers(token):
    try:
        isclients = admin_have_client_access(token)
        if isclients:
            allusers = db.Zucks_users.find()
            Users = []
            
            for user in allusers:
                Users.append(user)

            return True , "User fetched successfully",Users
        else:
            return False,"Admin have no permissions to fetch data",[]
    except:
        return False,"Users Not fetched",[]


def getDomainAnalysis(domain,token):
    try:
        access = admin_have_client_access(token)
        if access:
            profile = db.Zucks_profile.find_one({"domain":domain})
            usersCount = db.Zucks_users.count_documents({"ndid":profile.get("uId")})
            bookingCount = db.Bookings.count_documents({"ndid":profile.get("uId")})
            blogsCount = db.BlogsManagement.count_documents({"ndid":profile.get("uId")})
            contactCount = db.ContactUs.count_documents({"ndid":profile.get("uId")})
            roomsCount = db.Rooms.count_documents({"ndid":profile.get("uId")})
            bookingengine = db.BookingEngineData.find_one({"ndid":profile.get("uId")})
            hotellinks = db.Zucks_hotellinks.find_one({"ndid":profile.get("uId")})

            return True,"Success",{
                "location":len(profile.get("hotels")),
                "users":usersCount,
                "bookings":bookingCount,
                "blogs":blogsCount,
                "contactus":contactCount,
                "templateid":profile.get("template"),
                "plan":profile["plan"].get("name"),
                "rooms":roomsCount,
                "payment":bookingengine["Details"].get("Gateway"),
                "currency":profile.get("currency"),
                "domain":profile.get("domain"),
                "websitelink":hotellinks.get("websiteLink") if hotellinks.get("dashboardLink")=="None" else hotellinks.get("dashboardLink"),
                "bookinglink":hotellinks.get("bookingEngineLink")
                }
        else:
            return False,"Access Denied",{"location":0,"users":0,"bookings":0,"blogs":0,"contactus":0,"templateid":"-","plan":"-","rooms":"-","payment":{"Type":"-"},"currency":"-","domain":"-","websitelink":"-","bookinglink":"-"}
    except:
        return False,"Something went wrong",{"location":0,"users":0,"bookings":0,"blogs":0,"contactus":0,"templateid":"-","plan":"-","rooms":"-","payment":{"Type":"-"},"currency":"-","domain":"-","websitelink":"-","bookinglink":"-"}


def OtadetailofDomain(domain,token):
    try:
        access = admin_have_client_access(token)
        if access:
            profile = db.Zucks_profile.find_one({"domain":domain})
            otadetails = db.OTADetails.find_one({"ndid":profile.get("uId")})
            return True,otadetails,"Success"
        else:
            return False,{},"Access Denied"
    except:
        return False,{},"Something went wrong"
    

def getALlClientQuery(token):
    try:
        isclient = admin_have_client_access(token)
        if isclient:
            cursor = db.EazotelClientQuery.find({}, {'_id': False})  # Exclude _id field
            data = [document for document in cursor]  # Convert cursor to list of dictionaries
            return True, data
        else:
            return False, []
    except Exception as ex:
        return False,None
    

def editClientQuery(data,token):
    try:
        isclient = admin_have_client_access(token)
        if isclient:
            db.EazotelClientQuery.find_one_and_update({"clientQueryId":data.get("clientQueryId")},{"$set":{
                "flag":data.get("flag"),
                "remark":data.get("remark"),
                "followUp":data.get("followUp"),
                "nextFollowUp":data.get("nextFollowUp"),
                "Stage":{
                    "demoschedule":data.get("demoschedule"),
                    "messageSent":data.get("messageSent"),
                    "OTAListing":data.get("OTAListing"),
                    "sentProposal":data.get("sentProposal"),
                }
                }}
                
                )
        return True
    except Exception as ex:
        return False