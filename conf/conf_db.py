# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: conf_db.py
@time: 2025/6/14 10:03 
@desc: 

"""
from conf.conf_base import DEBUG

if DEBUG:
    db_config = {
        "host": "172.17.0.1",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "database": "test",
    }
else:
    db_config = {
        "host": "172.93.106.85",
        "port": 3307,
        "user": "root",
        "password": "123456",
        "database": "test",
    }
