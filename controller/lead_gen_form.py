from flask import Blueprint, request, jsonify
import json
from usecases import leadgenform_usecase
import logging

leadgenform_controller = Blueprint("leadgen", __name__)


@leadgenform_controller.route("/hi", methods=["GET"])
def hello():
    return json.dumps({"Message": "Hello lead gen form "})


@leadgenform_controller.route("/create-lead-gen-form", methods=["POST"])
def create_lead_gen_form():
    try:
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return (
                jsonify({"Message": "Missing Authorization header", "Status": False}),
                401,
            )
        token = bearer_token.split(" ")[1]
        data = request.get_json(force=True)

        status, msg = leadgenform_usecase.create_lead_gen_form(token, data)

        return (
            jsonify({"Message": msg, "Status": status}),
            201,
        )

    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "Internal server error", "Status": False}), 500


@leadgenform_controller.route("/get-lead-gen-form", methods=["GET"])
def get_lead_gen_form():
    try:
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return (
                jsonify({"Message": "Missing Authorization header", "Status": False}),
                401,
            )
        token = bearer_token.split(" ")[1]
        hId = request.args.get("hId")
        if not hId:
            return (
                jsonify(
                    {"Message": "Missing hId in query parameters", "Status": False}
                ),
                400,
            )

        status, msg, response = leadgenform_usecase.get_lead_gen_form(token, hId)
        return (
            jsonify({"Message": msg, "Status": status, "Data": response}),
            200,
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "Internal server error", "Status": False}), 500


@leadgenform_controller.route("/get-lead-gen-form-by-id", methods=["GET"])
def get_lead_gen_form_by_id():
    try:
        form_id = request.args.get("form_id")
        title = request.args.get("title")
        hId = request.args.get("hId")
        name = request.args.get("name")
        if not hId:
            return (
                jsonify(
                    {"Message": "Missing hId in query parameters", "Status": False}
                ),
                400,
            )
        if not title:
            return (
                jsonify(
                    {"Message": "Missing title in query parameters", "Status": False}
                ),
                400,
            )
        if not name:
            return (
                jsonify(
                    {"Message": "Missing name in query parameters", "Status": False}
                ),
                400,
            )
        if not form_id:
            return (
                jsonify(
                    {"Message": "Missing form_id in query parameters", "Status": False}
                ),
                400,
            )

        status, msg, response = leadgenform_usecase.get_lead_gen_form_by_id(
            form_id, title, hId, name
        )
        return (
            jsonify({"Message": msg, "Status": status, "Data": response}),
            200,
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "Internal server error", "Status": False}), 500


@leadgenform_controller.route("/edit-lead-gen-form", methods=["POST"])
def edit_lead_gen_form():
    try:
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return (
                jsonify({"Message": "Missing Authorization header", "Status": False}),
                401,
            )
        token = bearer_token.split(" ")[1]
        form_id = request.args.get("form_id")

        if not form_id:
            return (
                jsonify(
                    {"Message": "Missing form_id in query parameters", "Status": False}
                ),
                400,
            )

        data = request.get_json(force=True)
        print("data", data)
        print("form_id", form_id)
        status, msg = leadgenform_usecase.edit_lead_gen_form(token, data, form_id)
        print("hgjkljhghjkhgjkhg")
        return (
            jsonify({"Message": msg, "Status": status}),
            200,
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "Internal server error", "Status": False}), 500


@leadgenform_controller.route("/delete-lead-gen-form", methods=["POST"])
def delete_lead_gen_form():
    try:
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return (
                jsonify({"Message": "Missing Authorization header", "Status": False}),
                401,
            )
        token = bearer_token.split(" ")[1]
        form_id = request.args.get("form_id")
        status, msg = leadgenform_usecase.delete_lead_gen_form(token, form_id)
        return (
            jsonify({"Message": msg, "Status": status}),
            200,
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "Internal server error", "Status": False}), 500


# just to create more fileds and get fields on the frontend
@leadgenform_controller.route("/get-global-form-fields", methods=["GET"])
def get_form_fields():
    try:
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return (
                jsonify({"Message": "Missing Authorization header", "Status": False}),
                401,
            )
        token = bearer_token.split(" ")[1]
        status, msg, response = leadgenform_usecase.get_form_fields(token)
        return (
            jsonify({"Message": msg, "Status": status, "Data": response}),
            200,
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "Internal server error", "Status": False}), 500


@leadgenform_controller.route("/add-global-form-fields", methods=["POST"])
def add_form_fields():
    try:
        status, msg, data = leadgenform_usecase.add_form_fields()

        return (
            jsonify({"Message": msg, "Status": status, "Data": data}),
            200,
        )
    except Exception as ex:
        logging.error(f"{ex}")
        return ({"Message": "Internal server error", "Status": False}), 500
