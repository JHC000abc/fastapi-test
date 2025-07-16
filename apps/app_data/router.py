# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: router.py
@time: 2025/6/27 17:29 
@desc: 

"""
from apps.app_data.model import DATAModel
from models.model_response import ResponseModel
from service.service_parse_json import ServiceParseJson
from utils.utils_decorate import regular_sample, verify_cookies
from models.tables import ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP
from fastapi import APIRouter, Request, Body
from utils.utils_sqlalchemy import get_async_db, AsyncSqlAlchemyUtils, Depends
from typing import List

router_datas = APIRouter(prefix="/datas", tags=["数据处理"])


@router_datas.post("/parse/json", summary="解析JSONs数据", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP])
async def parse_json_datas(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                           data: List[DATAModel] = Body(...)
                           ):
    """
    支持上传多组解析处理
    :param request:
    :param db:
    :param data:
    :return:
    """
    service_parse_json = ServiceParseJson()
    result = {}
    for ind, req in enumerate(data):
        res = {}
        for r_ind, rule in enumerate(req.rules):
            rul = []
            for i in service_parse_json.parse_json(req.data, rule):
                rul.append(i)
            res[r_ind] = rul

        result[ind] = res

    return result
