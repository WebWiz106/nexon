import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from bson import json_util
from pathlib import Path
from bson.binary import Binary
from datetime import datetime, date, timedelta
from usecases import room_usecase, mail_usecase
import logging
import settings
import utils
from utils import db
from model.career import Careers
from bson import ObjectId

logging.basicConfig(format=settings.LOG_FORMATTER)
Logger = logging.getLogger(__name__)
Logger.setLevel(settings.LOG_LEVEL)


def create_career(career_data):

    try:
        domain = career_data.get("domain")
        profile = db.Zucks_profile.find_one({"domain": domain})

        if not profile:
            raise ValueError("Profile not found for the given domain")

        is_exist = db.Careers.find_one(
            {
                "email": career_data.get("email"),
                "contact": career_data.get("contact"),
                "jobtitle": career_data.get("jobtitle"),
            }
        )

        if is_exist:
            return False, "Already applied for this job title"

        db.Careers.insert_one(
            {
                "ndid": profile.get("uId"),
                "name": career_data.get("name"),
                "email": career_data.get("email"),
                "contact": career_data.get("contact"),
                "jobtitle": career_data.get("jobtitle"),
                "linkedin": career_data.get("linkedin"),
                "resume_url": career_data.get("resume_url"),
                "experience": career_data.get("experience"),
                "skills": career_data.get("skills"),
                "portfolio": career_data.get("portfolio"),
                "cover_letter": career_data.get("cover_letter"),
                "address": career_data.get("address"),
                "status": "pending",
                "education": career_data.get(
                    "education", []
                ),  # List of education details
                "certifications": career_data.get(
                    "certifications", []
                ),  # List of certifications
                "work_experience": career_data.get(
                    "work_experience", []
                ),  # List of work experiences
                "languages": career_data.get(
                    "languages", []
                ),  # List of spoken languages
                "expected_salary": career_data.get("expected_salary"),
                "availability": career_data.get("availability"),
                "github": career_data.get("github"),
                "references": career_data.get("references", []),  # List of references
                "created_at": datetime.utcnow(),
            }
        )

        mail_usecase.send_job_application_mail(
            profile.get("hotelName"),
            profile.get("hotelEmail"),
            domain,
            career_data.get("contact"),
            career_data.get("name"),
            career_data.get("email"),
            career_data.get("jobtitle"),
            career_data.get("cover_letter"),
            career_data.get("resume_url"),
        )
        return True, "Career created successfully"
    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)


def get_career(token):

    try:
        ndid = utils.get_ndid(token)
        careers = db.Careers.find({"ndid": ndid})
        careers_list = []

        for career in careers:
            career["_id"] = str(career["_id"])  # Convert ObjectId to string
            careers_list.append(career)
        return True, careers_list

    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)
