#!usr/bin/env python3
# -*- coding:utf-8 _*-

from flask import jsonify
from flask.blueprints import Blueprint

main_bp = Blueprint(name="main", import_name=__name__)


@main_bp.route('/', methods=['GET', 'POST'])
def test():
    return jsonify({"test": "Hello World"})
