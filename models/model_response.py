# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model_response.py
@time: 2025/6/14 00:06 
@desc: 

"""
from pydantic import BaseModel
from typing import Dict, Any, Optional, List, Union


class ResponseModel(BaseModel):
    """
    ResponseModel
    """
    code: int = -1
    msg: str = ""
    data: Optional[Dict[str, Any]] = None


class FunctionResponseModel(BaseModel):
    status: bool = False
    msg: str = ""
    data: Any = None