#!usr/bin/env python3
# -*- coding:utf-8 _*-

from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from flask_validator_swagger.libs.decorators import apis


def reg_swagger(app):
    swagger_json = {}
    paths = {}
    doc_base = app.config["SWAGGER_DOC_PATH"]
    swagger_bp = get_swaggerui_blueprint(doc_base, app.config["SWAGGER_JSON_PATH"])
    swagger_bp.name = "swagger-api"
    config = app.config
    for api_name, api in apis.items():
        url_prefix = config["URL_PREFIX"].format(version=config["API_VERSION"], api_type=api["api_type"])
        uri = "{0}/{1}".format(url_prefix, api_name)
        # param schema
        schema = {
            'properties': {
            },
            'type': 'object'
        }
        validator = api["validator"]
        for name in validator.keys():
            validate_class = getattr(validator, name)
            schema['properties'].update(validate_class.swagger_info(name))

        path_spec = {
            'post': {
                'tags': [
                    api_name,
                ],
                'description': api['target'].__doc__.split("\n")[1].strip(),
                'responses': {
                    '200': {
                        'description': 'Success'
                    },
                    '201': {
                        'description': 'Created / Updated'
                    },
                    '401': {
                        'description': 'No Authorization'
                    }
                },
                'parameters': [
                    {
                        'name': 'payload',
                        'required': True,
                        'in': 'body',
                        'schema': schema
                    }
                ]
            }
        }
        paths[uri] = path_spec

    swagger_json = {
        'swagger': '2.0',
        'basePath': '/',
        'paths': paths,
        'produces': [
            'application/json'
        ],
        'consumes': [
            'application/json'
        ],
        'definitions': {},
        'info': {
            'title': app.config["SWAGGER_TITLE"],
            'version': app.config["API_VERSION"]
        },
    }
    app.register_blueprint(swagger_bp, url_prefix=doc_base)

    @app.route(app.config["SWAGGER_JSON_PATH"])
    def spec():
        return jsonify(swagger_json)
