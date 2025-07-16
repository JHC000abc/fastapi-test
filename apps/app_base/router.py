# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: router.py
@time: 2025/6/14 10:29 
@desc: 

"""
import traceback
from fastapi import APIRouter, Request
from models.model_response import ResponseModel

base_router = APIRouter(prefix="", tags=["主路由"])


@base_router.get("/", summary="首页", response_model=ResponseModel)
async def index(request: Request):
    resp = ResponseModel()
    try:
        print(request.url)
        print(request.headers)
        print(request.cookies)
        print(request.client.host)
        print(request.client.port)
        resp.code = 0
        resp.msg = "success"
        resp.data = {
            "url": request.url,
            "headers": request.headers,
            "cookies": request.cookies,
            "client": {
                "host": request.client.host,
                "port": request.client.port
            },
        }
    except Exception as e:
        resp.msg = traceback.print_exc()
    finally:
        return resp
