#!usr/bin/env python3
# -*- coding:utf-8 _*-


class BaseError(Exception):
    code = 1001
    msg = "handle error"

    def __init__(self, msg=None, extra_msg=None):
        if msg:
            self.msg = msg
        if extra_msg:
            self.msg += ", {0}".format(extra_msg)

    def __str__(self):
        return "{0}, code:{1}, msg: {2}".format(self.__class__.__name__, self.code, self.msg)


class InvalidParamsError(BaseError):
    code = 2001
    msg = "Request params invalid"


class LackRequestParam(BaseError):
    code = 2002
    msg = "Lack request params"
