#!usr/bin/env python3
# -*- coding:utf-8 _*-

import inspect
import os
from functools import wraps

from flask import request, current_app, jsonify

from flask_validator_swagger.validator import BaseValidator

apis = {}


def validate_params(validator=BaseValidator):
    """
    validate request params
    :param validator:
    :return:
    """

    def _handle(func):
        @wraps(func)
        def __handler():
            code, msg, data = 0, "ok", {}
            try:
                new_params = {}
                params = request.get_json(force=True, silent=True) or {}
                for key in validator.keys():
                    validate_class = getattr(validator, key)
                    _pm = validate_class.validate(name=key, params=params)
                    new_params.update(_pm)
                data = func(**new_params or params)
            except Exception as e:
                current_app.logger.exception("--->api_name:{0}, error:{1}".format(func.__name__, str(e)))
                msg = getattr(e, "msg", "unknown error")
                code = getattr(e, "code", -1)
            finally:
                result = {
                    "code": code,
                    "msg": msg,
                    "data": data
                }

            return jsonify(**result)

        api_type = os.path.basename(inspect.stack()[1].filename)[:-3]
        apis[func.__name__] = {
            'target': __handler,
            'validator': validator,
            'api_type': api_type
        }

        return __handler

    return _handle
