# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model_CradSecret.py
@time: 2025/7/8 20:10 
@desc: 

"""
from datetime import datetime, timedelta, timezone
from models.tables.model_base import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from utils.utils_secret import SecretUtil

TABLE_NAME_CardSecret = "CardSecret"

STATUS_UNREVIEWED = "unreviewed"
STATUS_NORMAL = "normal"
STATUS_FORBIDDEN = "forbidden"
STATUS_DELETED = "deleted"

LEVEL_USER = "user"
LEVEL_ADMIN = "admin"
LEVEL_DEVELOP = "develop"

VERSION1 = "v1"  # 普通时间校验
VERSION2 = "v2"  # 使用次数校验
VERSION3 = "v3"  # 使用时长检验
VERSION4 = "v4"  # 使用频率校验


class CardSecret(Base):
    """
    用户信息表
    """
    __tablename__ = TABLE_NAME_CardSecret
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # 父级ID（外键关联到自身的id）
    parent_id = Column(Integer, ForeignKey(f'{TABLE_NAME_CardSecret}.id'), nullable=True, comment='上级卡密ID')
    # 建立自引用关系
    parent = relationship('CardSecret', remote_side=[id], backref='children')
    nickname = Column(String(50), nullable=True, default='momo', comment='用户昵称')
    secret = Column(String(255), nullable=False, unique=True, default='', comment='卡密')
    uid = Column(String(32), nullable=False, unique=True, default=lambda :SecretUtil.get_uuid(), comment='唯一识别码')
    status = Column(Enum(STATUS_UNREVIEWED, STATUS_NORMAL, STATUS_FORBIDDEN, STATUS_DELETED), nullable=False,
                    default=STATUS_NORMAL,
                    comment='卡密状态')

    role = Column(Enum(LEVEL_USER, LEVEL_ADMIN, LEVEL_DEVELOP), nullable=False, default=LEVEL_USER, comment='卡密等级')
    version = Column(Enum(VERSION1, VERSION2, VERSION3, VERSION4), nullable=False, default=VERSION1, comment='卡密版本')
    used = Column(Integer, nullable=False, default=0, comment='卡密验证次数')
    expired = Column(DateTime, nullable=True, default='2099-01-01 00:00:00', comment='卡密过期时间')
    create = Column(DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=8))), comment='创建时间')
    updated = Column(DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=8))),
                     onupdate=datetime.now(timezone(timedelta(hours=8))), comment='更新时间')

    __table_args__ = (
        {
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_unicode_ci",
        }
    )
