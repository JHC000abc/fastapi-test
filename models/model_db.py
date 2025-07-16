# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model_db.py
@time: 2025/6/14 09:55 
@desc: 

"""
from pydantic import BaseModel
from conf.conf_db import db_config


class DatabaseConfig(BaseModel):
    host = "172.17.0.1"
    user = "root"
    port = 3306
    password = "123456"
    database = "test"
    pool_size = 5


def get_db_config() -> DatabaseConfig:
    """返回数据库配置的可调用函数"""
    return DatabaseConfig(**db_config)
