from http import HTTPStatus
from typing import Tuple, Dict


# 200's responses
def register_package_created_response(package_id) -> Tuple[Dict, int]:
    return {'message': f'Package {package_id} was registered'}, HTTPStatus.CREATED


def submit_package_to_office_created_response(package_id, office_name) -> Tuple[Dict, int]:
    return {'message': f'Package {package_id} was submitted in post office {office_name}'}, HTTPStatus.CREATED


post_office_created_response = {'message': f'Post office created successfully'}, HTTPStatus.CREATED


# 400's responses
def register_package_error_response(error) -> Tuple[Dict, int]:
    return {'message': f'Could not register new package: {error}'}, HTTPStatus.BAD_REQUEST


def submit_package_error_response(error) -> Tuple[Dict, int]:
    return {'message': f'Could not submit package: {error}'}, HTTPStatus.BAD_REQUEST


def package_not_found_error_response(package_id) -> Tuple[Dict, int]:
    return {'message': f'Package with id {package_id} was not found'}, HTTPStatus.NOT_FOUND


def post_office_not_found_error_response(office_name) -> Tuple[Dict, int]:
    return {'message': f'Post office with name {office_name} was not found'}, HTTPStatus.NOT_FOUND


def missing_params_error_response(params) -> Tuple[Dict, int]:
    return {'message': f'Required parameters {params} are missing'}, HTTPStatus.BAD_REQUEST


def create_post_office_error_response(error) -> Tuple[Dict, int]:
    return {'message': f'Could not create post office: {error}'}, HTTPStatus.BAD_REQUEST
