from http import HTTPStatus
from flask import render_template, request
from db_utils import *
from app import create_app
from app.responses import (
    register_package_created_response,
    submit_package_to_office_created_response,
    register_package_error_response,
    submit_package_error_response,
    package_not_found_error_response,
    post_office_not_found_error_response,
    missing_params_error_response,
    post_office_created_response,
    create_post_office_error_response
)

app = create_app()


@app.route('/')
def index():
    """
    Renders the main template.
    """
    return render_template('index.html')


@app.route('/package/register', methods=['POST'])
def register_package():
    """
    Register a package and get tracking number in return.
    """
    recipient_name = request.form.get("recipient_name")
    destination_address = request.form.get("destination_address")
    destination_zip_code = request.form.get("destination_zip_code")
    package_type = request.form.get("package_type")

    if not all([recipient_name, destination_address, destination_zip_code, package_type]):
        # Basic validator
        return missing_params_error_response(["recipient_name", "destination_address", "destination_zip_code", "package_type"])

    package, error = persist_package(recipient_name, destination_address, destination_zip_code, package_type)
    if package is None:
        return register_package_error_response(error)

    return register_package_created_response(package.tracking_number)


@app.route('/package/submit', methods=['POST'])
def submit_package_to_office():
    """
    Submit a package at a post office.
    """
    tracking_number = request.form.get("tracking_number")
    post_office_name = request.form.get("post_office_name")

    if not all([tracking_number, post_office_name]):
        return missing_params_error_response(["tracking_number", "post_office_name"])

    package = get_package(tracking_number)
    if package is None:
        return package_not_found_error_response(tracking_number)

    if package.delivered:
        return {"message": f"Package {package.tracking_number} was already delivered"}, HTTPStatus.BAD_REQUEST

    post_office = get_post_office(post_office_name)
    if post_office is None:
        return post_office_not_found_error_response(post_office_name)

    error_message = record_package_in_post_office(package, post_office)
    if error_message:
        return submit_package_error_response(error_message)

    return submit_package_to_office_created_response(package.tracking_number, post_office.name)


@app.route('/package/tracking', methods=['GET'])
def retrieve_package_tracking():
    """
    Return package tracking history by its tracking number.
    """
    tracking_number = request.args.get("tracking_number")
    if not tracking_number:
        return missing_params_error_response(["tracking_number"])

    package = get_package(tracking_number)
    if package is None:
        return package_not_found_error_response(tracking_number)

    package_tracking = get_package_tracking(package)
    return package_tracking.to_dict(), HTTPStatus.OK


@app.route('/package', methods=['GET'])
def package_info():
    """
    Return all packages.
    """
    packages = get_packages()

    return [package.to_dict() for package in packages], HTTPStatus.OK


@app.route('/office', methods=['POST'])
def create_post_office():
    """
    Create a post office.
    """
    name = request.form.get("name")
    address = request.form.get("address")
    zip_code = request.form.get("zip_code")

    if not all([name, address, zip_code]):
        # Basic validator
        return missing_params_error_response(["name", "address", "zip_code"])

    office, error = persist_post_office(name, address, zip_code)
    if office is None:
        return create_post_office_error_response(error)

    return post_office_created_response


@app.route('/office', methods=['GET'])
def post_offices():
    """
    Return all post offices.
    """
    all_post_offices = get_post_offices()

    return [office.to_dict() for office in all_post_offices], HTTPStatus.OK
