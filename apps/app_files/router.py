# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: router.py
@time: 2025/6/14 20:44 
@desc: 

"""
import os
import traceback
from fastapi import APIRouter, File, UploadFile, Request, Depends
from typing import List
from models.model_response import ResponseModel
from utils.utils_decorate import regular_sample, verify_cookies
from models.tables import ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP
from utils.utils_sqlalchemy import get_async_db, AsyncSqlAlchemyUtils
from conf.conf_base import STATIC_FOLDER
from utils.utils_folder import FolderUtils
from service.service_slider import ServiceSlider
from conf.conf_medias import IMG_ALLOWS

router_files = APIRouter(prefix="/files", tags=["文件操作"])


@router_files.post("/upload", summary="上传多文件", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP])
async def upload_file(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                      files: List[UploadFile] = File(...)):
    """

    :param files:
    :return:
    """
    recode = {}
    save_file = os.path.abspath("uploads")
    os.makedirs(save_file, exist_ok=True)
    for file in files:
        with open(os.path.join(save_file, file.filename), "wb") as f:
            f.write(await file.read())

        recode.update({file.filename: file.size})
    return recode


@router_files.get("/lists", summary="获取静态资源路径下文件列表", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_USER, ROLE_ADMIN, ROLE_DEVELOP])
async def static_lists(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db), limit: int = 10,
                       offset: int = 0):
    static_folder = os.path.abspath(STATIC_FOLDER)
    recode = []
    nums = 0
    return_num = 0
    for file, filename in FolderUtils().get_all_files(static_folder):
        nums += 1
        if nums <= offset:
            continue
        return_num += 1
        recode.append({
            "index": return_num,
            "file": file.replace(static_folder, ""),
            "filename": filename,
            "size": f"{round(os.path.getsize(file) / (1024 * 1024), 2)} M" if round(
                os.path.getsize(file) / (1024 * 1024), 2) > 0 else f"{os.path.getsize(file)} KB"
        })
        if nums > limit:
            break
    return recode


@router_files.post("/slider/options", summary="滑块位置识别", response_model=ResponseModel)
@regular_sample
@verify_cookies(roles=[ROLE_DEVELOP, ROLE_USER, ROLE_ADMIN])
async def check_slider_options(request: Request, db: AsyncSqlAlchemyUtils = Depends(get_async_db),
                               img_background: UploadFile = File(...),
                               img_slider: UploadFile = File(...)):
    if img_background.size <= img_slider.size:
        raise ValueError("背景图不能小于滑块图")
    content_bg = await img_background.read()
    content_slider = await img_slider.read()
    if img_slider.content_type not in IMG_ALLOWS or img_background.content_type not in IMG_ALLOWS:
        raise ValueError(f"upload file is not in allow types ,support {IMG_ALLOWS}")
    options = ServiceSlider(content_bg, content_slider).get_options()
    await img_background.close()
    await img_slider.close()
    return options
