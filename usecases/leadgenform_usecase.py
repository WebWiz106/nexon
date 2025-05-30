from datetime import datetime
import logging
import settings
import utils
from utils import db
import json
import uuid
import re
from model.user import User
from form_field_array import form_fields, default_form_fields

logging.basicConfig(format=settings.LOG_FORMATTER)
Logger = logging.getLogger(__name__)
Logger.setLevel(settings.LOG_LEVEL)


def create_lead_gen_form(token, data):
    try:

        ndid = utils.get_ndid(token)
        hId = data.get("hId")
        name = utils.get_name(token).lower()
        title = data.get("title").lower()
        domain = utils.getdata(token)

        # print("name", form_slug)
        if not ndid or not hId:
            return False, "Token is missing ndid or hId"

        # lead_form = db.LeadGenForm.find_one({"ndid": ndid, "hId": hId})

        # if lead_form != None:
        #     return False, "Lead form already exists for this location"

        tenant_data = db.Zucks_profile.find_one({"uId": ndid})

        form_slug = re.sub(r"[^a-z0-9]+", "-", title).strip("-")

        form_unique_id = str(uuid.uuid4())

        form_live_url = f"https://forms.eazotel.com/{tenant_data["domain"]}/{hId}/{form_slug}/{form_unique_id}"
        new_form = {
            "ndid": ndid,
            "hId": hId,
            "form_id": form_unique_id,
            "title": title,
            "description": "Lead Gen Form",
            "status": "active",
            "emailId": "lead@eazotel.com",
            "contact": "1234567890",
            "form_url": form_live_url,
            "form_cms": {
                "bg_color": "#ffffff",
                "text_color": "#000000",
                "button_color": "#007bff",
                "button_text_color": "#ffffff",
                "button_text": "Submit",
                "border_color": "#000000",
                "border_radius": "5px",
                "bg_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxCAOltKzWe9ICbwuCKzpWS-B0nsvHVgB89w&s",
                "logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcST8qp3Nq1klrG-ADP9gZmRQZvog7WJZ-Qlkg&s",
                "banner_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTh-_ilTx-cg8DUxNkZ8J_nw_Qlv_ANNQjb-g&s",
                "banner_text": "Welcome to our service!",
                "banner_link": "https://example.com",
            },
            "form_fields": default_form_fields,
            "updated_at": datetime.utcnow(),
            "created_at": datetime.utcnow(),
        }

        db.LeadGenForm.insert_one(new_form)
        return True, "Lead form created successfully"

    except Exception as ex:
        logging.error(f"{ex}")
        return False, "{}".format(ex)


def get_lead_gen_form(token, hId):
    try:
        ndid = utils.get_ndid(token)
        # email = utils.get_email(token)
        if not ndid:
            return False, "Token is missing ndid", {}

        lead_forms = db.LeadGenForm.find({"ndid": ndid, "hId": hId})
        if lead_forms == None:
            return True, "Lead form not found", {}

        lead_forms_data = []
        for lead_form in lead_forms:
            del lead_form["_id"]
            lead_forms_data.append(lead_form)

        return False, "Form data fetched successfully", lead_forms_data
    except Exception as ex:
        logging.error(ex)
        return False, "{}".format(ex), {}


def get_lead_gen_form_by_id(form_id, title, hId, name):
    try:

        user = db.Zucks_profile.find_one({"domain": name})

        lead_form = db.LeadGenForm.find_one(
            {"ndid": user.get("uId"), "hId": hId, "title": title, "form_id": form_id}
        )

        if lead_form == None:
            return False, "Lead form not found", {}

        del lead_form["_id"]
        return True, "Lead form data fetched successfully", lead_form
    except Exception as ex:
        logging.error(ex)
        return False, "{}".format(ex), {}


def edit_lead_gen_form(token, data, form_id):
    try:

        print("data", data)
        ndid = utils.get_ndid(token)
        hId = data.get("hId")
        if not ndid:
            return False, "Token is missing ndid"

        lead_form = db.LeadGenForm.find_one(
            {"ndid": ndid, "hId": hId, "form_id": form_id}
        )

        if lead_form == None:
            return True, "Lead form not found"

        form_url = lead_form.get("form_url")
        title = data.get("title")

        # break url into parts
        name = form_url.split("/")[-4]
        hId = form_url.split("/")[-3]
        form_slug = form_url.split("/")[-2]
        form_unique_id = form_url.split("/")[-1]
        # print(
        #     "name",
        #     name,
        #     "hId",
        #     hId,
        #     "form_slug",
        #     form_slug,
        #     "form_unique_id",
        #     form_unique_id,
        # )
        # form_url = lead_form.get("form_url")

        # lead_form["_id"] = str(lead_form["_id"])

        # print("lead_form", form_url)

        new_form_slug = re.sub(r"[^a-z0-9]+", "-", data.get("title")).strip("-")

        # form_unique_id = form_url.split("/")[-2]

        # print("form_unique_id", form_unique_id)
        form_live_url = (
            f"https://forms.eazotel.com/{name}/{hId}/{new_form_slug}/{form_unique_id}"
        )

        # print("form_live_url", form_url, title, form_slug, form_unique_id)
        db.LeadGenForm.update_one(
            {"ndid": ndid, "hId": hId, "form_id": form_id},
            {
                "$set": {
                    "title": data.get("title"),
                    "description": data.get("description"),
                    "status": data.get("status"),
                    "emailId": data.get("emailId"),
                    "contact": data.get("contact"),
                    "form_url": form_live_url,
                    "form_cms": {
                        "bg_color": data["form_cms"].get("bg_color"),
                        "text_color": data["form_cms"].get("text_color"),
                        "button_color": data["form_cms"].get("button_color"),
                        "button_text_color": data["form_cms"].get("button_text_color"),
                        "button_text": data["form_cms"].get("button_text"),
                        "border_color": data["form_cms"].get("border_color"),
                        "border_radius": data["form_cms"].get("border_radius"),
                        "bg_image_url": data["form_cms"].get("bg_image_url"),
                        "logo_url": data["form_cms"].get("logo_url"),
                        "banner_image_url": data["form_cms"].get("banner_image_url"),
                        "banner_text": data["form_cms"].get("banner_text"),
                        "banner_link": data["form_cms"].get("banner_link"),
                    },
                    "form_id": form_id,
                    "form_fields": data.get("form_fields"),
                    "updated_at": datetime.utcnow(),
                }
            },
        )
        return True, "Form updated successfully"

    except Exception as ex:
        logging.error(ex)
        return False, "{}".format(ex)


def delete_lead_gen_form(token, form_id):
    try:
        ndid = utils.get_ndid(token)

        if not ndid or not form_id:
            return False, "Token is missing ndid or form_id"

        lead_form = db.LeadGenForm.find_one({"ndid": ndid, "form_id": form_id})
        if lead_form == None:
            return True, "Lead form not found"

        db.LeadGenForm.delete_one({"ndid": ndid, "form_id": form_id})
        return True, "Lead form deleted successfully"

    except Exception as ex:
        logging.error(ex)
        return False, "{}".format(ex)


def get_form_fields(token):
    try:
        ndid = utils.get_ndid(token)
        if not ndid:
            return False, "Token is missing ndid", {}

        form_fields = list(db.GlobalFormFields.find({}))

        if form_fields == None:
            return False, "Form not found", {}

        print("form_fields", form_fields)

        fields = form_fields[0].get("form_fields")

        return True, "Form fetch successfully", fields

    except Exception as ex:
        logging.error(ex)
        return False, "{}".format(ex), {}


def add_form_fields():
    try:
        print("form_fields", form_fields)

        db.GlobalFormFields.insert_one({"form_fields": form_fields})

        return True, "Form fields added successfully", form_fields

    except Exception as ex:
        logging.error(ex)
        return False, "{}".format(ex)
