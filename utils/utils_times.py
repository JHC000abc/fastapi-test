# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_times.py
@time: 2025/7/8 20:25 
@desc: 

"""
from datetime import datetime, timedelta, timezone
from conf.conf_secret import SECRET_EXPIRED


class DataTimeUtils:

    @staticmethod
    def now():
        return datetime.now(timezone(timedelta(hours=8)))

    @staticmethod
    def next_interval_days(seconds: int = None):
        return DataTimeUtils.now() + timedelta(seconds=SECRET_EXPIRED if not seconds else int(seconds))
