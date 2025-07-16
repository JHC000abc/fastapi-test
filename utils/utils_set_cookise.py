# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_set_cookise.py
@time: 2025/6/16 21:40 
@desc: 

"""
from fastapi import Response


async def set_cookies(response: Response, cookies_map:dict):
    """

    :param response:
    :param cookies_map:
    :return:
    """
    for key,value in cookies_map.items():
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=True,
            samesite="lax",
        )
