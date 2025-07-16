# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: test.py
@time: 2025/6/13 22:40 
@desc: 

"""
from datetime import datetime
from service.service_sign import ServiceSign
from utils.utils_email import EmailSend


def get_cookies(file="cookies.list"):
    """

    :param file:
    :return:
    """
    with open(file, "r", encoding="utf-8") as f:
        for i in f:
            line = i.strip()
            yield line


if __name__ == '__main__':
    ss = ServiceSign()
    for cookie in get_cookies():
        msg = f"{datetime.now()}--{cookie}--{ss.process(cookie)}"
        EmailSend().load_send_info(["JHC000abc@163.com"], ["京东签到"],
                                   [msg])
