# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model.py
@time: 2025/6/20 19:12 
@desc: 

"""
from pydantic import BaseModel
from typing import List


class Sign(BaseModel):
    """
    Sign
    """
    server_name: str = "jd"
    token: str = None
    send_list: List[str] = []

