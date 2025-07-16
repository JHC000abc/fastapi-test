# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: service_card.py
@time: 2025/7/10 13:46 
@desc: 

"""
from models.tables import VERSION1, VERSION4, VERSION2, VERSION3
from utils.utils_times import DataTimeUtils


class ServiceCard:
    """
    卡密服务类
    """

    def __init__(self, version):
        self.version = version
        self.version_func_map = {
            VERSION1: self.verify_version1,
            VERSION2: self.verify_version2,
            VERSION3: self.verify_version3,
            VERSION4: self.verify_version4,
        }

    def verify(self, data):
        """
        验证卡密
        :param data:
        :return:
        """

        return self.version_func_map.get(self.version)(data)

    def verify_version1(self, data):
        """
        验证版本1卡密
        :param data:
        :return:
        """
        if data["expired"].replace(tzinfo=None) <= DataTimeUtils.now().replace(tzinfo=None):
            return False
        return True

    def verify_version2(self, data):
        pass

    def verify_version3(self, data):
        pass

    def verify_version4(self, data):
        pass
