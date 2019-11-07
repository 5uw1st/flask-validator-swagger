#!usr/bin/env python3
# -*- coding:utf-8 _*-

from flask_validator_swagger.libs.fields import IntegerField, StringField, DictField, \
    ListField, DateTimeField, UrlField, EnumField, BaseFiled


class BaseValidator(object):

    @classmethod
    def keys(cls):
        _keys = []
        for key, value in cls.__dict__.items():
            if isinstance(value, BaseFiled):
                _keys.append(key)
        return _keys


class AddUserValidator(BaseValidator):
    name = StringField(max_length=20, min_length=1, desc="user name", required=True)
    age = IntegerField(minimum=1, maximum=100, desc="user age")
    sex = EnumField(enums=["man", "woman"], default="man", desc="user sex")
    url = UrlField(max_length=256, desc="user blog url", default="https://www.json.cn/")
    publish_date = DateTimeField(desc="user publish blog time", required=False, default="2019-10-02 11:22:11")
    values = ListField(IntegerField(maximum=100), desc="user values")
    data = DictField({
        "host": StringField(desc="host address"),
        "port": IntegerField(maximum=65535, desc="port")
    }, desc="user data")


class GetUserInfoValidator(BaseValidator):
    name = StringField(max_length=20, min_length=1, desc="user name", required=True)

