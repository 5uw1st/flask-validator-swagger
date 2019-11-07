#!usr/bin/env python3
# -*- coding:utf-8 _*-

from flask.blueprints import Blueprint

from flask_validator_swagger.libs.decorators import validate_params
from flask_validator_swagger.validator import AddUserValidator, GetUserInfoValidator

user_bp = Blueprint(name="user", import_name=__name__)


@user_bp.route('/get_user_info', methods=['GET', 'POST'])
@validate_params(validator=GetUserInfoValidator)
def get_user_info(**request_params):
    """
    Get user info by name
    :param request_params:
    :return:
    """
    return {
        "name": request_params["name"],
        "age": 20
    }


@user_bp.route('/add_user', methods=['GET', 'POST'])
@validate_params(validator=AddUserValidator)
def add_user(**request_params):
    """
    Add a new user
    :param request_params:
    :return:
    """
    return {
        "name": request_params["name"]
    }
