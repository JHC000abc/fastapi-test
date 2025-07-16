# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: register.py
@time: 2025/6/14 00:03 
@desc: 

"""
import traceback
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from apps import router_user, base_router, router_files, router_sign, router_datas, router_card
from conf.conf_base import STATIC_FOLDER, MIDDLEWARE_PREFIX_ALLOW_LIST
from fastapi.middleware.cors import CORSMiddleware
from conf.conf_base import server
from models.tables import UserInfo, CardSecret, ClientConf, LEVEL_DEVELOP, LEVEL_USER, STATUS_NORMAL
from utils.utils_auth import JwtHandler
from utils.utils_times import DataTimeUtils

app = FastAPI()


async def startup():
    """

    :return:
    """
    from utils.utils_sqlalchemy import get_async_db, get_db_config
    db = await get_async_db(get_db_config())
    await db._create_tables()
    jwt = JwtHandler()

    obj = UserInfo(name="root", password=jwt.get_hash_code('root'),
                   email="jhc000abc@gmail.com", phone="17600000000", address="北京市海淀区", role="develop",
                   status="normal")

    obj2 = UserInfo(name="zhangsan", password=jwt.get_hash_code('zhangsan'),
                    email="jhc000abc2@gmail.com", phone="17600000001", address="山东省烟台市", role="admin",
                    status="normal")

    obj3 = UserInfo(name="lisi", password=jwt.get_hash_code('lisi'),
                    email="jhc000ab3c@gmail.com", phone="17600000002", address="北京市海淀区", role="user",
                    status="normal")

    obj4 = UserInfo(name="wangwu", password=jwt.get_hash_code('wangwu'),
                    email="jhc000ab4c@gmail.com", phone="17600000003", address="黑龙江省大庆市", role="user",
                    status="forbidden")

    obj5 = UserInfo(name="zhaoliu", password=jwt.get_hash_code('zhaoliu'),
                    email="jhc000ab5c@gmail.com", phone="17600000004", address="河南省开封市", role="user",
                    status="deleted")
    if not await db.query_by_conditions(UserInfo, {'id': 1}):
        res = await db.insert_objects([obj, obj2, obj3, obj4, obj5])
        print(res)

    config = {"server": "http://172.17.0.1", "port": 8000, "debug": True}
    config2 = {"server": "http://127.0.0.1", "port": 8000, "debug": False}
    obj_client_conf = ClientConf(config=config)
    obj_client_conf2 = ClientConf(config=config2)
    if not await db.query_by_conditions(ClientConf, {'id': 1}):
        res = await db.insert_objects([obj_client_conf, obj_client_conf2])
        print(res)

    card_secret_obj = CardSecret(nickname="root", secret="root", role=LEVEL_DEVELOP)
    card_secret_obj2 =CardSecret(secret="user",parent_id=1)
    if not await db.query_by_conditions(CardSecret, {'id': 1}):
        res= await db.insert_objects([card_secret_obj, card_secret_obj2])
        print(res)


# 初始化 建表 注册事件
app.add_event_handler("startup", startup)

app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="静态资源")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{server['host']}:{server['port']}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 注册路由
app.include_router(base_router)
app.include_router(router_user)
app.include_router(router_files)

app.include_router(router_sign)
app.include_router(router_datas)

app.include_router(router_card)


# 添加中间件
@app.middleware("http")
async def middleware(request: Request, call_next):
    """

    :param request:
    :param call_next:
    :return:
    """
    if not any(request.url.path.startswith(prefix) for prefix in MIDDLEWARE_PREFIX_ALLOW_LIST):
        return await call_next(request)
    response = None
    print(datetime.now(), ' 请求地址：', request.url)
    start = datetime.now()
    try:
        response = await call_next(request)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        end = datetime.now()
        time_diff = end - start
        print("执行时间:", time_diff)
        return response
