import utils
from flask import Blueprint , jsonify , request
from flask_cors import CORS,cross_origin

from usecases import dinabite_usecase
# cms_controller = Blueprint('cms', __name__)
dinabite_controller = Blueprint('dinabite', __name__)




@dinabite_controller.route("/hi")
def hello1():
    return {"Message":"Hi"}


#get user register with dinabite status using token
@dinabite_controller.route("/<token>",methods=["GET"])
def get_user_have_acess(token):
    try:
        ndid = utils.get_ndid(token)
        status,access_token = dinabite_usecase.verify_acess_token_db(ndid)
        return jsonify({"Status":status,"access_token":access_token})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500



#edit dinabite token to profile
@dinabite_controller.route("/update",methods=["POST"])
def update_user_acesstoken():
    try:
        data = request.get_json(force=True)
        status,message = dinabite_usecase.update_acess_token_db(data)
        return jsonify({"Status":status,"Message":message})
    except Exception as ex:
        return ({"Message": "{}".format(ex)}), 500