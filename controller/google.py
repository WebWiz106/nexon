from flask import Blueprint,request,jsonify
from usecases import google_usecase
google_controller = Blueprint('google', __name__)


@google_controller.route("/hi")
def hello():
    return "Hello Goolge !!"


@google_controller.route("/reviews/<ndid>")
def get_reviews(ndid):
    try:
        print("*****", ndid)
        reviews = google_usecase.get_reviews(ndid)
        print(reviews)
        return {"Reviews": reviews}
    except Exception as ex:
        return None
    
@google_controller.route("/reviews/website/<domain>")
def get_reviews_domain_data(domain):
    try:
        print("*****", domain)
        reviews = google_usecase.get_reviews_domain(domain)
        print(reviews)
        return {"Reviews": reviews}
    except Exception as ex:
        return None



@google_controller.route("/getlighthousedata")
def get_lighthousedata():
    data = request.get_json(force=True)
    value=google_usecase.getlighthousedata(data)
    return jsonify({"Data":value})



