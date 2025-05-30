import logging
import os

LOG_LEVEL = logging.DEBUG
LOG_FORMATTER = "%(asctime)s - %(levelname)s - %(message)s"

DEBUG = os.environ.get("DEBUG", True)

DBURL = os.environ.get("DBURL")
DBNAME = os.environ.get("DBNAME")


JWT_SECRETS = ".L+aZVH?%z^sLCSMB^67_A=Q7cs;@^L5]97x>yY]wd`67t"
JWT_ALGORITHM = "HS256"

RAZORPAY_API_KEY = os.environ.get("RAZORPAY_API_KEY")
RAZORPAY_SECRET_KEY = os.environ.get("RAZORPAY_SECRET_KEY")

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

try:
    from local import *
except:
    pass
