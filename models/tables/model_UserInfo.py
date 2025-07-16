# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model_UserInfo.py
@time: 2025/6/14 21:26 
@desc: 

"""
from datetime import datetime, timedelta, timezone
from models.tables.model_base import Base
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, Enum, DateTime, Date

TABLE_NAME = "UserInfo"
STATUS_NORMAL = "normal"
STATUS_FORBIDDEN = "forbidden"
STATUS_DELETED = "deleted"

ROLE_USER = "user"
ROLE_ADMIN = "admin"
ROLE_DEVELOP = "develop"


class UserInfo(Base):
    """
    用户信息表
    """
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), unique=True, nullable=False, default='', comment='用户名')
    password = Column(String(255), nullable=False, default='', comment='密码')
    status = Column(Enum(STATUS_NORMAL, STATUS_FORBIDDEN, STATUS_DELETED), nullable=False, default=STATUS_NORMAL,
                    comment='账号状态')
    role = Column(Enum(ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP), nullable=False, default=ROLE_USER, comment='角色')
    email = Column(String(50), unique=True, nullable=False, default="", comment='邮箱')
    phone = Column(String(11), unique=True, nullable=False, default="", comment='手机号')
    country = Column(String(50), nullable=False, default="China", comment='国家')
    address = Column(String(255), nullable=False, default='', comment='地址')
    birthday = Column(Date, nullable=False, default='1900-01-01', comment='生日')
    sex = Column(Boolean, nullable=False, default=True, comment='性别')
    age = Column(Integer, nullable=False, default=99, comment='年龄')
    create = Column(DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=8))), comment='创建时间')
    updated = Column(DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=8))),
                     onupdate=datetime.now(timezone(timedelta(hours=8))), comment='更新时间')

    __table_args__ = (
        CheckConstraint("age > 0 AND age < 100", name='valid_age_range'),
        {
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_unicode_ci",
        }
    )
