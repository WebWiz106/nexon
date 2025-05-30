import json
import settings
import razorpay
import utils
from bson import json_util

from usecases import blogsMgmt_usecase
from flask import Blueprint, jsonify, request
from datetime import datetime, date, timedelta
import logging
blogs_controller = Blueprint('blogsMgmt', __name__)


@blogs_controller.route("/hi")
def hi():
    hello = blogsMgmt_usecase.test()
    return json.dumps({"mesage":hello})

@blogs_controller.route("/getblog/blogs/<domain>",methods=["GET"])
def getBlogs(domain):
    try:
        status ,response= blogsMgmt_usecase.getBlogs(domain)
        return jsonify({"Status":status,"Blogs":json.loads(json_util.dumps(response))})
    except:
        return jsonify({"Status":True,"mesage":"Some Problem"})
    

@blogs_controller.route("/getblog/blogs/dashboard/<token>",methods=["GET"])
def getBlogsDashboard(token):
    try:
        status ,response= blogsMgmt_usecase.getBlogsDashboardtoken(token)
        return jsonify({"Status":status,"Blogs":json.loads(json_util.dumps(response))})
    except:
        return jsonify({"Status":True,"mesage":"Some Problem"})
    

@blogs_controller.route("/createblog",methods=["POST"])
def createBlogs():
    try:
        data = request.get_json(force=True)
        status,message = blogsMgmt_usecase.createBlogs(data)
        return jsonify({"Status":status,"Message":message})
    except:
        return jsonify({"Status":True,"mesage":"Some Problem"})

@blogs_controller.route("/updateblog",methods=["POST"])
def updateBlogs():
    try:
        data=request.get_json(force=True)
        status,message=blogsMgmt_usecase.updateBlogs(data)
        return jsonify({"Status":status,"Message":message})
    except:
        return json.dumps({"Status":True,"Message":"Some Problem"})


@blogs_controller.route("/deletedblog",methods=["POST"])
def deleteBlogs():
    try:
        data = request.get_json(force=True)
        status = blogsMgmt_usecase.deleteBlogsFuntion(data)
        return jsonify({"Status":True,"Message":"Blog Deleted Successfully"})
    except:
        return jsonify({"Status":False})
    

@blogs_controller.route("/addstats",methods=["POST"])
def editBlogsStats():
    try:
        data = request.get_json(force=True)
        status = blogsMgmt_usecase.addViewsLikesShares(data)
        return jsonify({"Status":True,"Message":"Done"})
    except:
        return jsonify({"Status":False})
    
@blogs_controller.route("/addstatsDomain",methods=["POST"])
def editBlogsStatsdomain():
    try:
        data = request.get_json(force=True)
        status = blogsMgmt_usecase.addViewsLikesSharesdomain(data)
        return jsonify({"Status":True,"Message":"Done"})
    except:
        return jsonify({"Status":False})


@blogs_controller.route("/addcomment",methods=["POST"])
def addBlogsComments():
    try:
        data = request.get_json(force=True)
        status = blogsMgmt_usecase.addComment(data)
        return jsonify({"Status":True,"Message":"Done"})
    except:
        return jsonify({"Status":False})
    

@blogs_controller.route("/addreplytocomment",methods=["POST"])
def addBlogsReplytoComment():
    try:
        data = request.get_json(force=True)
        status = blogsMgmt_usecase.addReply(data)
        return jsonify({"Status":True,"Message":"Done"})
    except:
        return jsonify({"Status":False})
    

@blogs_controller.route("/get/blog/<domain>/<name>",methods=["GET"])
def getIndividualBlogonDomain(domain,name):
    try:
        blog = blogsMgmt_usecase.getIndividualDomain(domain,name)
        return jsonify({"Status":True,"Message":json.loads(json_util.dumps(blog))})
    except:
        return jsonify({"Status":False})
        