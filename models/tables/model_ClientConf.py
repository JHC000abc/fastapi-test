# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model_ClientConf.py
@time: 2025/7/10 21:26 
@desc: 

"""
from datetime import datetime, timedelta, timezone
from models.tables.model_base import Base
from sqlalchemy import Column, Integer, DateTime, JSON

TABLE_NAME_ClientConf = "ClientConf"


class ClientConf(Base):
    """
    用户信息表
    """
    __tablename__ = TABLE_NAME_ClientConf
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    config = Column(JSON, nullable=False, comment='配置信息')
    create = Column(DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=8))), comment='创建时间')
    updated = Column(DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=8))),
                     onupdate=datetime.now(timezone(timedelta(hours=8))), comment='更新时间')

    __table_args__ = (
        {
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_unicode_ci",
        }
    )
