# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_decorate.py
@time: 2025/6/14 22:19 
@desc: 

"""
import traceback
from functools import wraps
from models.model_response import ResponseModel
from fastapi import Request, Depends
from utils.utils_auth import JwtHandler
from utils.utils_sqlalchemy import get_async_db, AsyncSqlAlchemyUtils
from models.tables import UserInfo, STATUS_NORMAL


def regular_sample(func):
    """
    装饰器，用于包装处理所有函数异常
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        resp = ResponseModel()
        try:
            result = await func(*args, **kwargs)
            if isinstance(result, dict):
                resp.data = {
                    "response": result
                }
            resp.code = 0
            resp.msg = "success"
            resp.data = {"response": result}
        except Exception as e:
            resp.msg = f"{traceback.format_exc()}"
        finally:
            return resp

    return wrapper


def verify_cookies(**kw):
    """
    验证cookies对应的用户的权限 状态
    :param func:
    :return:
    """

    def decorate(func):
        @wraps(func)
        async def wrapper(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db), *args, **kwargs):
            # 从cookies中获取token
            cookies = request.cookies
            token = cookies.get('token')
            # 解析并验证token
            jwt = JwtHandler()
            token_status, token_dict = jwt.decrypt_token(token)
            if not token_status:
                raise RuntimeError("token is invalid")

            # 根据解析token中的用户名查询用户信息
            select_res = await db.query_by_conditions(UserInfo, {"name": token_dict.get("key")}, False)
            if len(select_res) != 1:
                raise RuntimeError("user info is not exist")

            select_res = select_res[0]

            # 验证状态
            if select_res.status != STATUS_NORMAL:
                raise RuntimeError("user status is not normal")

            # 验证角色
            if kw.get("roles"):
                verify_role = kw.get("roles")
                if select_res.role not in verify_role:
                    raise RuntimeError("role verify failed")

            return await func(request, db, *args, **kwargs)

        return wrapper

    return decorate
