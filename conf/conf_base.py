# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: conf_base.py
@time: 2025/6/13 23:58 
@desc: 

"""
DEBUG = True

server = {
    "host": "127.0.0.1",
    "port": 8000,
}

STATIC_FOLDER = "statics"

MIDDLEWARE_PREFIX_ALLOW_LIST = ["/user", "/files", "/card", "/sign", "/datas"]

# long_token 过期时间 单位：秒
LONG_TOKEN_EXPIRE = 60 * 60 * 12 * 15
# token 过期时间 单位：秒
TOKEN_EXPIRE = 60 * 15


