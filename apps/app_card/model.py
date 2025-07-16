# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model.py
@time: 2025/7/8 23:31 
@desc: 

"""
from pydantic import BaseModel
from datetime import datetime
from models.tables import STATUS_NORMAL, ROLE_USER, VERSION1


class CardVerifyModel(BaseModel):
    """

    """
    nickname: str
    secret: str


class CardRegisterModel(BaseModel):
    """

    """
    nickname: str = "momo"
    secret: str
    parent_id: int


class CardAuditModel(BaseModel):
    """

    """
    id: int
    status: str = STATUS_NORMAL
    parent_id: int
    role: str = ROLE_USER
    expired: datetime = '2099-01-01 00:00:00'
    version: str = VERSION1
    uid :str = ""
