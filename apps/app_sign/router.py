# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: router.py
@time: 2025/6/20 19:12 
@desc: 

"""
from fastapi import APIRouter, Request, Depends, Body
from models.model_response import ResponseModel
from utils.utils_sqlalchemy import get_async_db, AsyncSqlAlchemyUtils
from utils.utils_decorate import regular_sample, verify_cookies
from models.tables import ROLE_DEVELOP, ROLE_USER, ROLE_ADMIN
from apps.app_sign.model import Sign
from service.service_sign import ServiceSign
from utils.utils_email import EmailSend

router_sign = APIRouter(prefix="/sign", tags=["签到服务"])


@router_sign.post("/jd", summary="京东签到", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_DEVELOP, ROLE_USER, ROLE_ADMIN])
async def jd_sign(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                  data: Sign = Body(...)):
    if data.server_name != "jd":
        raise ValueError("请传入正确的服务名")
    # 调用签到接口
    server_sign = ServiceSign()
    ua = request.headers.get("user-agent", None)
    html = server_sign.sign_jd(data.token, ua)
    response = server_sign.parse_jd(html)
    # 发送邮件提醒
    if len(data.send_list) > 0:
        es = EmailSend()
        es.load_send_info(data.send_list, ["京东签到" for _ in data.send_list],
                          [response for _ in data.send_list])
    return response
