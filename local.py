import logging
import os
LOG_LEVEL = logging.DEBUG
LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(message)s'
DEBUG=os.environ.get("DEBUG", True)
DBURL=os.environ.get("DBURL","mongodb+srv://eazotel:admin@cluster0.p0kewzl.mongodb.net/")
DBNAME=os.environ.get("DBNAME","Courage")
RAZORPAY_API_KEY=os.environ.get("RAZORPAY_API_KEY","rzp_test_UZ0V9jh3jMC0C9")
RAZORPAY_SECRET_KEY=os.environ.get("RAZORPAY_SECRET_KEY","XHctZxmnMhzkkwcAlDtF0Xuc")
#XHctZxmnMhzkkwcAlDtF0Xuc , rzp_test_UZ0V9jh3jMC0C9
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyB7275VpUoxX56JWDwoISq00bXcq2LSHtI")