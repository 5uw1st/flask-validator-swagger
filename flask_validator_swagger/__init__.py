#!usr/bin/env python3
# -*- coding:utf-8 _*-

import os

from flask import Flask


def create_app(config=None):
    _config = config or os.getenv('FLASK_CONFIG') or 'flask_validator_swagger.config.DevConfig'
    app = Flask(__name__)

    app.config.from_object(_config)

    # config swagger
    if app.config.get("SWAGGER_ENABLE", False):
        # reg swagger
        from flask_validator_swagger.libs.swagger import reg_swagger
        reg_swagger(app)

    return app
