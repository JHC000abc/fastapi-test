# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: conf_secret.py
@time: 2025/7/8 20:42 
@desc: 

"""
from conf.conf_base import DEBUG

if DEBUG:
    SECRET_EXPIRED = 30 * 12 * 60 * 60
    SECRET_VERIFY_SERVER = "http://127.0.0.1:8000/card/verify"
    SECRET_REGISTER_SERVER = "http://127.0.0.1:8000/card/add"
else:
    SECRET_EXPIRED = 30 * 12 * 60 * 60
    SECRET_VERIFY_SERVER = "http://127.0.0.1:8000/card/verify"
    SECRET_REGISTER_SERVER = "http://127.0.0.1:8000/card/add"
