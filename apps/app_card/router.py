# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: router.py
@time: 2025/7/8 23:32 
@desc: 

"""
from apps.app_card.model import CardVerifyModel, CardRegisterModel, CardAuditModel
from models.model_response import ResponseModel, FunctionResponseModel
from utils.utils_decorate import regular_sample, verify_cookies
from models.tables import ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP, STATUS_NORMAL, LEVEL_USER, VERSION1
from fastapi import APIRouter, Request, Body
from utils.utils_sqlalchemy import get_async_db, AsyncSqlAlchemyUtils, Depends
from typing import List
from models.tables import STATUS_UNREVIEWED, CardSecret, TABLE_NAME_CardSecret
from utils.utils_times import DataTimeUtils
from service.service_card import ServiceCard

router_card = APIRouter(prefix="/card", tags=["卡密"])


@router_card.post("/verify", summary="校验卡密", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP])
async def parse_json_datas(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                           data: CardVerifyModel = Body(...)
                           ):
    """

    :param request:
    :param db:
    :param data:
    :return:
    """
    results = FunctionResponseModel()
    query_res = await db.query_by_conditions(CardSecret, {"secret": data.secret})
    if not query_res:
        results.msg = "卡密不存在"
        return results
    query_res = query_res[0]
    nickname = query_res.nickname
    if nickname != data.nickname:
        results.msg = "昵称不匹配"
        results.data = query_res.uid
        return results
    if query_res.status != STATUS_NORMAL:
        results.msg = "卡密状态异常"
        results.data = query_res.uid
        return results
    expire_status = ServiceCard(query_res.version).verify({"expired": query_res.expired})
    if not expire_status:
        results.msg = "卡密过期"
        results.data = query_res.uid
        return results
    sql = f"update {TABLE_NAME_CardSecret} set used = used + 1 ,updated='{DataTimeUtils.now()}' where id= {query_res.id}; "
    await db.run_raw_sql(sql)
    results.msg = "卡密校验成功"
    results.data = query_res.uid
    results.status = True
    return results


@router_card.post("/add", summary="添加卡密", response_model=ResponseModel)
@regular_sample
# @verify_cookies(roles=[ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP])
async def add_secret(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                     data: CardRegisterModel = Body(...)
                     ):
    """
    支持上传多组解析处理
    :param request:
    :param db:
    :param data:
    :return:
    """
    results = FunctionResponseModel()
    # 检查卡密是否存在
    query_res = await db.query_by_conditions(CardSecret, {"secret": data.secret})
    if query_res:
        results.msg = "卡密已存在，请更换微信注册"
        return results
    # 上级不存在 直接插入
    if data.parent_id == 0:
        insert_res = await db.insert_object(
            CardSecret(secret=data.secret, nickname=data.nickname, status=STATUS_UNREVIEWED))
        if insert_res[0] != 1:
            results.msg = "卡密添加失败"
            return results
        insert_id = insert_res[-1]
        query_data = await db.query_by_conditions(CardSecret, {"id": insert_id})
        query_data = query_data[0]
        results.status = True
        results.msg = "卡密添加成功,等待管理员审核"
        results.data = query_data.uid
        return results
    # 上级存在 检查上级状态 插入
    query_res_parent = await db.query_by_conditions(CardSecret, {"id": data.parent_id})
    if not query_res_parent:
        results.msg = "上级不存在"
        return results
    query_res_parent = query_res_parent[0]
    if query_res_parent.status != STATUS_NORMAL:
        results.msg = "上级卡密异常"
        return results
    insert_res = await db.insert_object(
        CardSecret(secret=data.secret, nickname=data.nickname, status=STATUS_UNREVIEWED, parent_id=data.parent_id))
    if insert_res[0] != 1:
        results.msg = "卡密添加失败"
        return results
    results.status = True
    results.msg = "卡密添加成功,等待管理员审核"
    results.data = query_res_parent.uid
    return results


# 上级存在 检查上级状态 插入


@router_card.post("/audit", summary="审核卡密", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_ADMIN, ROLE_DEVELOP])
async def audit_secret(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                       data: List[CardAuditModel] = Body(...),
                       ):
    """

    :param request:
    :param db:
    :param data:
    :return:
    """
    results = []
    for item in data:
        sql = f"""
        UPDATE {TABLE_NAME_CardSecret}
        SET status = '{item.status}',
            role = '{item.role}',
            expired = '{item.expired}',
            parent_id = {item.parent_id if item.parent_id != 0 else 'NULL'},
            updated='{DataTimeUtils.now()}',
            version = '{item.version}'
        WHERE uid = '{item.uid}' and status = '{STATUS_UNREVIEWED}';
        """
        res = await db.run_raw_sql(sql)
        results.append([item.id, res])
    return results


@router_card.post("/change", summary="修改卡密状态", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_ADMIN, ROLE_DEVELOP])
async def audit_secret(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                       data: List[CardAuditModel] = Body(...),
                       ):
    """

    :param request:
    :param db:
    :param data:
    :return:
    """
    results = []
    for item in data:
        sql = f"""
        UPDATE {TABLE_NAME_CardSecret}
        SET status = '{item.status}',
            role = '{item.role}',
            expired = '{item.expired if item.expired else '2099-01-01 00:00:00'}',
            parent_id = {item.parent_id if item.parent_id != 0 else 'NULL'},
            updated='{DataTimeUtils.now()}',
            version = '{item.version}'
        WHERE id = {item.id};
        """
        res = await db.run_raw_sql(sql)
        results.append([item.id, res])
    return results
