import utils
import constants
import pymongo
import json
import settings
import logging

from bson import json_util
from usecases import mail_usecase,booking_usecase
import random
from model.bookings import Bookings
from model.booking_item import BookingItem
from datetime import datetime, date, timedelta
logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

from utils import db


def test():
    return "Hello Blogs"


def generate_random_code(ndid):
    # Generate a random 10-digit code
    random_code = ''.join(str(random.randint(0, 9)) for _ in range(10))

    # Concatenate the random code and the date
    code_with_date = random_code + ndid
    
    return code_with_date

def generate_random_commentid(blogid):
    # Generate a random 10-digit code
    random_code = ''.join(str(random.randint(0, 9)) for _ in range(8))

    # Concatenate the random code and the date
    code_with_date = random_code + blogid
    
    return code_with_date

def generate_random_replyid(commentid):
    # Generate a random 10-digit code
    random_code = ''.join(str(random.randint(0, 9)) for _ in range(6))

    # Concatenate the random code and the date
    code_with_date = random_code + commentid
    
    return code_with_date


def getBlogs(domain):
    try:
        dbprofile = db.Zucks_profile.find_one({"domain":domain})
        ndid = dbprofile.get("uId")

        blogs = db.BlogsManagement.find({"ndid":ndid})
        return True,blogs
    except:
        return False,[]
    

def getBlogsDashboardtoken(token):
    try:
        ndid = utils.get_ndid(token)
        blogs = db.BlogsManagement.find({"ndid":ndid})
        return True,blogs
    except:
        return False,[]

def remove_whitespace_with_hyphen(input_string):
    return '-'.join(input_string.split())


def createBlogs(blogdetails):
    try:
        token = blogdetails.get("token")
        ndid = utils.get_ndid(token)    
        blogid = generate_random_code(ndid)
        blogdetails["blogId"]=blogid
        blogdetails["blogLink"]=remove_whitespace_with_hyphen(blogdetails.get("blogTitle"))
        current_datetime = datetime.now()
        blogdetails["blogIssueDate"]=current_datetime.strftime('%Y-%m-%d')
        blogdetails["ndid"]=ndid
        blogdetails.pop("token")
        blogdetails["blogShares"]=int(blogdetails["blogShares"])
        blogdetails["blogLikes"]=int(blogdetails["blogLikes"])
        blogdetails["blogViews"]=int(blogdetails["blogViews"])
        blogdetails["ishide"]=blogdetails["ishide"]=="true"
        blogdetails["isPin"]=blogdetails["isPin"]=="true"
        db.BlogsManagement.insert_one(blogdetails)
        return True,"Blog Created successfully"
    except:
        return False,"Blog Creation failed"
    

def deleteBlogsFuntion(blogdetails):
    try:
        token = blogdetails.get("token")
        ndid = utils.get_ndid(token)

        blogid = blogdetails.get("blogid")

        db.BlogsManagement.find_one_and_delete({"ndid":ndid,"blogId":blogid})
        
        return True
    except:
        return False
    

def addViewsLikesShares(blogdetails):
    try:
        token = blogdetails.get("token")
        ndid = utils.get_ndid(token)
        blogid = blogdetails.get("blogid")
        bloglikes = blogdetails.get("likes")
        blogshare = blogdetails.get("shares")
        blogviews = blogdetails.get("views")

        blog = db.BlogsManagement.find_one_and_update({"ndid":ndid,"blogId":blogid},{"$set":{
            "blogLikes":int(bloglikes),
            "blogViews":int(blogviews),
            "blogShares":int(blogshare)
        }})
        return True
    except:
        return False
    
def addViewsLikesSharesdomain(blogdetails):
    try:
        domain = blogdetails.get("domain")
        profile = db.Zucks_profile.find_one({"domain":domain})
        ndid = profile.get("uId")
        blogid = blogdetails.get("blogid")
        bloglikes = blogdetails.get("likes")
        blogshare = blogdetails.get("shares")
        blogviews = blogdetails.get("views")

        blog = db.BlogsManagement.find_one_and_update({"ndid":ndid,"blogId":blogid},{"$set":{
            "blogLikes":int(bloglikes),
            "blogViews":int(blogviews),
            "blogShares":int(blogshare)
        }})
        return True
    except:
        return False
    

def addComment(blogdetails):
    try:
        token = blogdetails.get("token")
        ndid = utils.get_ndid(token)
        blogid = blogdetails.get("blogid")  

        commentid = generate_random_commentid(blogid)
        author = blogdetails.get("author")
        comment = blogdetails.get('comment')

        blog = db.BlogsManagement.find_one({"ndid":ndid,"blogId":blogid})
        
        newcomment = {
            "commentId":commentid,
            "author":author,
            "message":comment,
            "reply":[]
        }
        comments = blog.get("blogsComments")
        comments.append(newcomment)

        blog = db.BlogsManagement.find_one_and_update({"ndid":ndid,"blogId":blogid},{"$set":{
            "blogsComments":comments
        }})


        return True
    except:
        return False
    

def addReply(blogdetails):
    try:
        token = blogdetails.get("token")
        ndid = utils.get_ndid(token)
        blogid = blogdetails.get("blogid")  
        commentid = blogdetails.get("commentid")

        replyid = generate_random_replyid(commentid)
        author = blogdetails.get("author")
        comment = blogdetails.get('comment')

        data = {
            "replyId":replyid,
            "author":author,
            "comment":comment
        }

        blogscomment = db.BlogsManagement.find_one({"ndid":ndid,"blogId":blogid}).get("blogsComments")
        for i in blogscomment:
            if(i.get("commentId")==commentid):
                comment = i.get("reply")
                comment.append(data)



        db.BlogsManagement.find_one_and_update({"ndid":ndid,"blogId":blogid},{"$set":{
            "blogsComments":blogscomment
        }})
        return True
    except:
        return False
        
    
def updateBlogs(blogdetails):
    try:
        ndid=utils.get_ndid(blogdetails.get("token"))
        blogId=blogdetails.get("blogId")
        blogdetails["ndid"]=ndid
        blogdetails["blogShares"]=int(blogdetails["blogShares"])
        blogdetails["blogLikes"]=int(blogdetails["blogLikes"])
        blogdetails["blogLink"]=remove_whitespace_with_hyphen(blogdetails.get("blogTitle"))
        blogdetails["blogViews"]=int(blogdetails["blogViews"])
        blogdetails["ishide"]=blogdetails["ishide"]=="true"
        blogdetails["isPin"]=blogdetails["isPin"]=="true"
        blogdetails.pop("token")
        db.BlogsManagement.find_one_and_replace({"ndid":ndid,"blogId":blogId},blogdetails)
        return True,"Blogs Updated Successfully"
    except Exception as ex:
        return False,"Blogs Updation failed"

def getIndividualDomain(domain,name):
    try:
        profile = db.Zucks_profile.find_one({"domain":domain})
        blog = db.BlogsManagement.find_one({"ndid":profile.get("uId"),"blogLink":name})
        if blog==None:
            return {}
        else:
            return blog

    except:
        return "False"