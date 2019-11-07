#!usr/bin/env python3
# -*- coding:utf-8 _*-

import datetime
import re

from flask_validator_swagger.exceptions import InvalidParamsError, LackRequestParam

_a = float('-inf')
_b = float('inf')


class BaseFiled(object):
    """
    Base field type
    """

    def __init__(self, required=True, default=None, desc=None):
        self._required = required
        self._default = default
        self._desc = desc or ""

    def _get_value(self, name, params):
        if name not in params.keys():
            if self._required and self._default is None:
                raise LackRequestParam(extra_msg=name)
            value = self._default
        else:
            value = params[name]
        return value

    def validate(self, name, params):
        value = self._get_value(name=name, params=params)
        new_value = self._do_validate(name=name, value=value)
        return {name: new_value}

    def _do_validate(self, name, value):
        raise NotImplementedError

    def _get_extra_swagger_info(self, name):
        raise {}

    def swagger_info(self, name):
        extra_info = self._get_extra_swagger_info(name) or {}
        info = {"type": "string", "description": self._desc, "default": self._default}
        info.update(extra_info)
        return {name: info}

    def __str__(self):
        return "<{0}>".format(self.__class__.__name__)


class IntegerField(BaseFiled):
    """
    Integer field type
    """

    def __init__(self, required=False, default=None, desc=None, minimum=_a, maximum=_b):
        super(IntegerField, self).__init__(required=required, default=default, desc=desc)
        self.minimum = minimum
        self.maximum = maximum

    def _do_validate(self, name, value):
        if type(value) is not int:
            raise InvalidParamsError(extra_msg="Must be Integer:{0}".format(name))

        if not (self.minimum <= value <= self.maximum):
            raise InvalidParamsError(
                extra_msg="Must be in [{0}, {1}]:{2}".format(self.minimum, self.maximum, name))

        return value

    def _get_extra_swagger_info(self, name):
        tp = {'type': 'integer'}
        if self.minimum is not _a:
            tp['example'] = tp['minimum'] = self.minimum

        if self.maximum is not _b:
            tp['maximum'] = self.maximum
        return tp


class StringField(BaseFiled):

    def __init__(self, required=False, default=None, desc=None, min_length=0, max_length=_b):
        super(StringField, self).__init__(required=required, default=default, desc=desc)
        self.min_length = min_length
        self.max_length = max_length

    def _do_validate(self, name, value):
        if type(value) is not str:
            raise InvalidParamsError(extra_msg="Must be string:{0}".format(name))

        if not (self.min_length <= len(value) <= self.max_length):
            raise InvalidParamsError(
                extra_msg="Length must be in [{0}, {1}]:{2}".format(self.min_length, self.max_length, name))

        return value

    def _get_extra_swagger_info(self, name):
        tp = {'type': 'string', 'minLength': self.min_length}
        if self.max_length is not _b:
            tp['maxLength'] = self.max_length
        return tp


class IntegerStringMixField(BaseFiled):
    """
    Integer or string mix field type
    """

    def _do_validate(self, name, value):
        if not isinstance(value, (str, int)):
            raise InvalidParamsError(extra_msg="Must be integer or string:{0}".format(name))

        return value


class DateTimeField(BaseFiled):
    """
    DateTime field type
    """

    def __init__(self, required=False, default=None, desc=None, to_datetime=True):
        super(DateTimeField, self).__init__(required=required, default=default, desc=desc)
        self.to_datetime = to_datetime

    def _do_validate(self, name, value):
        try:
            value_dt = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            if self.to_datetime:
                return value_dt
            else:
                return value
        except ValueError:
            raise InvalidParamsError(extra_msg="Datetime format error:{0}".format(name))

    def _get_extra_swagger_info(self, name):
        return {'type': 'string', 'example': '2019-10-01 10:00:00'}


class UrlField(StringField):
    """
    Url field type
    """

    def _do_validate(self, name, value):
        if type(value) is not str:
            raise InvalidParamsError(extra_msg="Must be string:{0}".format(name))

        if not (self.min_length <= len(value) <= self.max_length):
            raise InvalidParamsError(
                extra_msg="Length must be in [{0}, {1}]:{2}".format(self.min_length, self.max_length, name))

        if not re.match(r'(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', value):
            raise InvalidParamsError(extra_msg="Not a url:{0}".format(name))

        return value

    def _get_extra_swagger_info(self, name):
        tp = {'type': 'string', 'minLength': self.min_length, 'example': 'https://www.google.com/'}
        if self.max_length is not _b:
            tp['maxLength'] = self.max_length
        return tp


class EnumField(BaseFiled):
    """
    Enum field type
    """

    def __init__(self, enums, required=False, default=None, desc=None):
        super(EnumField, self).__init__(required=required, default=default, desc=desc)
        self.enums = enums

    def _do_validate(self, name, value):
        if value not in self.enums:
            raise InvalidParamsError(
                extra_msg="value not in [{0}]:{1}".format(", ".join(list(map(lambda x: str(x), self.enums))), name))

        return value

    def _get_extra_swagger_info(self, name):
        tp = {'type': 'string', 'example': self.enums[0], 'enum': self.enums}
        return tp


class ListField(BaseFiled):
    """
    List field type
    """

    def __init__(self, list_definition, required=False, default=None, desc=None, min_length=0, max_length=_b):
        super(ListField, self).__init__(required=required, default=default, desc=desc)
        self.list_definition = list_definition
        self.min_length = min_length
        self.max_length = max_length

    def _do_validate(self, name, value):
        if type(value) is not list:
            raise InvalidParamsError(extra_msg="Must be list:{0}".format(name))

        if not (self.min_length <= len(value) <= self.max_length):
            raise InvalidParamsError(
                extra_msg="List length must be in [{0}, {1}]:{2}".format(self.min_length, self.max_length, name))

        result = []
        for i, v in enumerate(value):
            v = self.list_definition.validate(name="v", params={"v": v})["v"]
            result.append(v)

        return result

    def _get_extra_swagger_info(self, name):
        tp = {
            'type': 'array',
            'items': self.list_definition.swagger_info(name)[name]
        }
        return tp


class DictField(BaseFiled):
    """
    Dict field type
    """

    def __init__(self, dict_definition, required=False, default=None, desc=None):
        super(DictField, self).__init__(required=required, default=default, desc=desc)
        self.dict_definition = dict_definition

    def _do_validate(self, name, value):
        real_value = {}
        for k, field in self.dict_definition.items():
            nv = field.validate(name=k, params=value)[k]
            real_value[k] = nv
        return real_value

    def _get_extra_swagger_info(self, name):
        tp = {
            'type': 'object',
            'properties': {}
        }
        for k, v in self.dict_definition.items():
            tp['properties'].update(v.swagger_info(k))

        return tp


if __name__ == '__main__':
    import json

    _params = {
        "test_a": 12,
        "test_b": [1, 12],
        "test_c": {"c1": 7, "c2": [2, 1]}
    }
    a = IntegerField(maximum=10)
    b = ListField(list_definition=IntegerField(maximum=10))
    c = DictField(dict_definition={"c1": IntegerField(maximum=10), "c2": b})
    ret_b = b.validate(name="test_b", params=_params)
    ret_c = c.validate(name="test_c", params=_params)
    t = c.swagger_info(name="test_c")
    print(json.dumps(t, indent=4))
