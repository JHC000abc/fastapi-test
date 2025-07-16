# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model.py
@time: 2025/6/14 10:30 
@desc: 

"""
import re
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import date
from typing import Optional
from models.tables import ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP, STATUS_NORMAL, STATUS_DELETED, STATUS_FORBIDDEN


class UserInfo(BaseModel):
    id: int = None
    # username2: str = Field(regex="^/")
    name: str = None
    password: str = Field(default=None, max_length=255)
    status: str = Field(default=STATUS_NORMAL)
    role: str = Field(default=ROLE_USER)
    email: EmailStr = Field(default="2345678423@qq.com")
    phone: str = Field(default="18900000000", max_length=11)
    country: str = "China"
    address: str = Field(default="", max_length=255)
    birthday: Optional[date] = Field(default="1999-01-01")
    sex: bool = Field(default=True)
    age: int = Field(default=10, gt=1, lt=99)

    # @validator("name")
    # def name_must_alpha(cls, value):
    #     assert value.isalpha(), "name must be alph"
    #     return value

    @validator("role")
    def role_must_in_list(cls, value):
        role_list = [ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP]
        assert value in role_list, f"role must in {role_list}"
        return value

    @validator("status")
    def status_must_in_list(cls, value):
        status_list = [STATUS_NORMAL, STATUS_DELETED, STATUS_FORBIDDEN]
        assert value in status_list, f"status must in {status_list}"
        return value

    @validator('phone')
    def validate_phone(cls, value):
        # 中国手机号正则
        pattern = r'^1[3-9]\d{9}$'
        assert re.match(pattern, value), f'手机号格式不正确:{value}'
        return value
