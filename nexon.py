import logging
import settings

from flask import Flask
from flask_cors import CORS, cross_origin
from controller.booking_engine import booking_controller
from controller.users import user_controller
from controller.rooms import room_controller
from controller.payment import payment_controller
from controller.google import google_controller
from controller.meal_package import meal_package_controller
from controller.promos import promos_controller
from controller.ad_packages import ad_package_controller
from controller.price import price_controller
from controller.multilocation import multilocation_controller
from controller.cms import cms_controller
from controller.roominventory import roominventory
from controller.upload_files import upload_files_controller
from controller.admin import admin_controller
from controller.dinabite import dinabite_controller
from controller.frontdesk import frontdesk_controller
from controller.razorpay import razorpay_controller
from controller.eazotel import eazotel_controller
from controller.plans import plan_controller
from controller.analytics import analytics_controller
from controller.leadsmanagement import leadmanagement_controller
from controller.blogsMgmt import blogs_controller
from controller.phonepay import phonepe_controller
from controller.wati import wati_controller
from controller.channelDist import channel_distribution
from controller.sports import sports
from controller.bookingEngineLogin import bookingEngineLogin_controller
from controller.lead_gen_form import leadgenform_controller


# career controller
from controller.career import career_controller


logging.basicConfig(format=settings.LOG_FORMATTER)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(settings.LOG_LEVEL)

app = Flask(__name__)
CORS(app)
app.register_blueprint(user_controller, url_prefix="/user")
app.register_blueprint(meal_package_controller, url_prefix="/mpackage")
app.register_blueprint(room_controller, url_prefix="/room")
app.register_blueprint(promos_controller, url_prefix="/promos")
app.register_blueprint(ad_package_controller, url_prefix="/rpackage")
app.register_blueprint(price_controller, url_prefix="/price")
app.register_blueprint(booking_controller, url_prefix="/booking")
app.register_blueprint(payment_controller, url_prefix="/payment")
app.register_blueprint(google_controller, url_prefix="/google")
app.register_blueprint(multilocation_controller, url_prefix="/multilocation")
app.register_blueprint(cms_controller, url_prefix="/cms")
app.register_blueprint(roominventory, url_prefix="/inventory")
app.register_blueprint(upload_files_controller, url_prefix="/upload")
app.register_blueprint(admin_controller, url_prefix="/admin")
app.register_blueprint(dinabite_controller, url_prefix="/dinabite")
app.register_blueprint(frontdesk_controller, url_prefix="/frontdesk")
app.register_blueprint(razorpay_controller, url_prefix="/razorpay")
app.register_blueprint(eazotel_controller, url_prefix="/eazotel")
app.register_blueprint(plan_controller, url_prefix="/plans")
app.register_blueprint(analytics_controller, url_prefix="/analytics")
app.register_blueprint(leadmanagement_controller, url_prefix="/leadmanagement")
app.register_blueprint(blogs_controller, url_prefix="/blogs")
app.register_blueprint(phonepe_controller, url_prefix="/phonepe")
app.register_blueprint(wati_controller, url_prefix="/wati")
app.register_blueprint(channel_distribution, url_prefix="/distribution")
app.register_blueprint(sports, url_prefix="/sports")
app.register_blueprint(bookingEngineLogin_controller, url_prefix="/feature1")
app.register_blueprint(career_controller, url_prefix="/career")
app.register_blueprint(leadgenform_controller, url_prefix="/leadgen")


if __name__ == "__main__":
    app.config["DEBUG"] = settings.DEBUG
    app.run()
