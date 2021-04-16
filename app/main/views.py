# -*- coding: utf-8 -*-
import base64
import json
from datetime import datetime

from flask import request, jsonify

from . import main
from .model import User
from .utils import curl_server, base64_to_ssrs
from .. import db


@main.route('/')
def index():
    return 'hello world'


@main.route('/ssr/<key>')
def get_ssrs(key):
    # todo 添加数据库判定
    print(key)
    result = curl_server('https://speedwlkj.top/s/akYKst')
    res = base64_to_ssrs(result)
    return res


@main.route('/create', methods=['POST'])
def create():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    wx_name = data.get('wx_name')
    key = base64.b64encode(wx_name.encode()).decode()
    user = User()
    user.key = key
    user.wx_name = wx_name
    user.user_name = wx_name
    user.create_at = datetime.now()
    user.update_at = datetime.now()
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'code': 1,
        'message': 'success',
        'url': 'http://big.forcebing.top:8084/{}'.format(key)
    })
