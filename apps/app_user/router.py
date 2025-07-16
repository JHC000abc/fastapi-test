# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: router.py
@time: 2025/6/14 10:30 
@desc: 

"""
import traceback
from utils.utils_decorate import regular_sample, verify_cookies
from fastapi import APIRouter, Body, Depends, Request, Form, Response
from models.model_response import ResponseModel
from models.tables import UserInfo, TABLE_NAME, STATUS_NORMAL, ROLE_DEVELOP, ROLE_USER, ROLE_ADMIN, STATUS_DELETED, \
    STATUS_FORBIDDEN
from apps.app_user.model import UserInfo as app_UserInfo
from utils.utils_sqlalchemy import get_async_db, AsyncSqlAlchemyUtils
from utils.utils_auth import JwtHandler
from datetime import datetime
from utils.utils_set_cookise import set_cookies
from conf.conf_base import LONG_TOKEN_EXPIRE

router_user = APIRouter(prefix="/user", tags=["用户操作"])


@router_user.get("/{id}", summary="获取用户信息", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_DEVELOP, ROLE_USER, ROLE_ADMIN])
async def get_user(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db), id: int = None):
    """

    :param id:
    :param db:
    :return:
    """
    return await db.query_by_conditions(UserInfo, {"id": id})


@router_user.post("/add", summary="添加用户", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_DEVELOP, ROLE_ADMIN])
async def add_user(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                   user: app_UserInfo = Body(...)):
    """

    :param user:
    :param db:
    :return:
    """
    obj = user.dict()
    if obj.get("id"):
        del obj["id"]
    if obj.get("password"):
        obj["password"] = JwtHandler().get_hash_code(obj["password"])
    return await db.insert_object(UserInfo(**obj))


@router_user.post("/update", summary="更新用户", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_DEVELOP, ROLE_USER, ROLE_ADMIN])
async def update_status(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                        user: app_UserInfo = Body(...)):
    """
    id 必传
    :param request:
    :param db:
    :param user:
    :return:
    """
    obj_json = user.dict()
    if obj_json.get("password"):
        obj_json["password"] = JwtHandler().get_hash_code(obj_json["password"])
    return await db.update_objects([UserInfo(**obj_json)])


@router_user.post("/delete", summary="删除用户", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_DEVELOP, ROLE_ADMIN])
async def delete(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                 id: int = Form(...), mode: bool = Form(False)):
    """

    :param request:
    :param db:
    :param id:
    :param mode: True:删除，False：禁用
    :return:
    """
    obj_json = {
        "id": id,
        "status": STATUS_DELETED if mode else STATUS_FORBIDDEN
    }
    return await db.update_objects([UserInfo(**obj_json)])


@router_user.post("/login", summary="登陆", response_model=ResponseModel)
@regular_sample
async def login(username: str = Form(...), password: str = Form(...),
                db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                response: Response = None
                ):
    """

    :param username:
    :param password:
    :param db:
    :return:
    """
    # 查询数据库 用户名是否存在
    query_data = await db.query_by_conditions(UserInfo, {
        "name": username
    }, False)
    if not query_data:
        raise RuntimeError(f"user:{username} not exists")
    query_data = query_data[0]
    # 校验账号状态
    if query_data.status != STATUS_NORMAL:
        raise RuntimeError(f"status is {query_data.status}")
    # 对比密码
    db_pwd = query_data.password
    jwt = JwtHandler()
    verify = jwt.verify_hash_code(password, db_pwd)
    if verify:
        token = jwt.create_token(username, {"login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        long_token = JwtHandler(interval=LONG_TOKEN_EXPIRE).create_token(username, {
            "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        cookies_map = {
            "token": token,
            "long_token": long_token,
        }
        await set_cookies(response, cookies_map)

    return "login success" if verify else "login failed"


@router_user.post("/register", summary="注册", response_model=ResponseModel)
@regular_sample
async def register(user: app_UserInfo=Body(...), db: AsyncSqlAlchemyUtils = Depends(get_async_db)):
    """

    :param user:
    :param db:
    :return:
    """
    obj = user.dict()
    obj.update({"password": JwtHandler().get_hash_code(obj["password"])})
    if obj.get("id") is not None:
        del obj["id"]
    return await db.insert_object(UserInfo(**obj))


@router_user.post("/refresh/cookies", summary="刷新cookies", response_model=ResponseModel)
@regular_sample
async def refresh_cookies(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                          response: Response = None):
    """
    仅刷新短期cookies 长期cookies 过期 重新登陆
    :param request:
    :param db:
    :param response:
    :return:
    """
    # 检查cookies 有效性
    jwt = JwtHandler()
    token = request.cookies.get("token")
    long_token = request.cookies.get("long_token")
    token_status, token_data = jwt.decrypt_token(token)
    long_token_status, long_token_data = jwt.decrypt_token(long_token)
    if token_status or not long_token_status:
        raise RuntimeError(f"token is enable or long_token is expired")
    username = long_token_data.get("key")

    query_data = await db.query_by_conditions(UserInfo, {
        "name": username
    }, False)
    if not query_data:
        raise RuntimeError(f"user:{username} not exists")
    query_data = query_data[0]
    # 校验账号状态
    if query_data.status != STATUS_NORMAL:
        raise RuntimeError(f"status is {query_data.status}")

    token = jwt.create_token(username, {"login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    cookies_map = {
        "token": token
    }
    await set_cookies(response, cookies_map)
