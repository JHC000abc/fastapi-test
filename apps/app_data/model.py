# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: model.py
@time: 2025/6/27 17:29 
@desc: 

"""
from pydantic import BaseModel, validator
from typing import Dict, List, Optional, Any
from service.service_parse_json import ServiceParseJson


class DATAModel(BaseModel):
    """

    """
    data: Optional[Dict[str, Any] | List[Any]] = None
    rules: Optional[List[str]] = []

    @validator("rules")
    def rules_must_in_list(cls, value):
        status = True
        _value = []
        for i in value:
            status, value = ServiceParseJson.valid_rules(i)
            if not status:
                break
            _value.append(value)
        value = _value

        assert status is True, f"Rules Failed to pass verification"
        return value
