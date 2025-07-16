# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_secret.py
@time: 2025/7/10 11:46 
@desc: 

"""
import uuid
import hashlib


class SecretUtil:
    """

    """

    @staticmethod
    def get_md5(data, salt=b''):
        md5 = hashlib.md5(salt)
        md5.update(data.encode("utf-8"))
        return md5.hexdigest()

    @staticmethod
    def get_uuid():
        uid = str(uuid.uuid4()).replace('-', '')
        return uid
