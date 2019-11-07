#!usr/bin/env python3
# -*- coding:utf-8 _*-


import logging
import os

BASE_PATH = os.path.dirname(__file__)


def get_env(key, default):
    return os.environ.get(key, default)


current_env = get_env("ENV_MODE", "DEV").upper()


class BaseConfig(object):
    API_VERSION = "v1"
    URL_PREFIX = "/api/{version}/{api_type}"
    DEBUG = False
    LOG_PATH = get_env("LOG_PATH", os.path.join(BASE_PATH, "logs"))
    LOG_FORMAT = "%(asctime)s [%(process)d] - %(levelname)s - %(name)s[%(lineno)s]: %(message)s"
    LOG_LEVEL = logging.DEBUG

    SECRET_KEY = b'\xa28\xb4rN\x90[\r\x8f\xb8J\x15\xa3e\x02z\xc5\xe8dzNv+\x1b'

    SWAGGER_ENABLE = False
    SWAGGER_TITLE = "Restful Api"
    SWAGGER_JSON_PATH = "/spec/swagger.json"
    SWAGGER_DOC_PATH = "/api/doc"


class DevConfig(BaseConfig):
    DEBUG = True
    SWAGGER_ENABLE = True


class TestConfig(BaseConfig):
    SECRET_KEY = b'D\xd9\xc3ZPI\xd57b7\xbb\xf3\xb8.\x06vA\x16\x96*\xbd\xa5\xc8H'


class ProdConfig(BaseConfig):
    LOG_LEVEL = logging.INFO
    SECRET_KEY = b'\xdd$X\x826\xeb\xf4Sj"\x08\x7f=:\xe9\x89\xfb\xaa\x83T\xea\xe0\xc7\x81'


__env_config = {
    "DEV": DevConfig,
    "TEST": TestConfig,
    "PROD": ProdConfig
}

current_config = __env_config.get(current_env)
if current_config is None or not issubclass(current_config, BaseConfig):
    raise KeyError
