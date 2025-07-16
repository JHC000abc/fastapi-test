# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: service_parse_json.py
@time: 2025/6/27 16:36 
@desc: 

"""
import copy
import json
import traceback
from typing import Any, Generator, List, Union, Optional, Dict


class ServiceParseJson:
    """

    """

    def __init__(self):
        pass

    @staticmethod
    def valid_rules(rules):
        """
        验证规则是否有效
        :param rules:
        :return:
        """
        try:
            if len(rules) != 0:
                rules = ",".join(rules.split(']['))
                rules = json.loads(rules)
            return True, rules
        except Exception as e:
            return False, rules

    def parse_json(self, json_data: Optional[Dict | List[Dict]], rules: List[Union[str, int]]) -> Generator[
        Any, None, None]:
        """
        解析JSON数据，返回符合规则的数据

        参数:
            json_data: 要解析的JSON数据
            rules: 解析规则列表，支持通配符"*"

        返回:
            生成器，生成匹配的数据或错误信息

        示例:
            rules = ["children", "*", "data", "value"]
            或
            rules = ["children", 0, "data"]
        """
        if not json_data or len(json_data) == 0:
            yield "Error: Input data is None"
            return

        if not rules:
            yield copy.deepcopy(json_data)
            return

        current_rule, *remaining_rules = rules

        # 处理通配符情况
        if current_rule == "*":
            if isinstance(json_data, list):
                for item in json_data:
                    yield from self.parse_json(item, remaining_rules)
            elif isinstance(json_data, dict):
                for value in json_data.values():
                    yield from self.parse_json(value, remaining_rules)
            return

        # 处理普通规则
        try:
            next_data = json_data[current_rule]
            yield from self.parse_json(next_data, remaining_rules)
        except (KeyError, TypeError, IndexError) as e:
            yield f"Error accessing path {current_rule}: {str(e)}"
        except Exception as e:
            yield traceback.format_exc()


if __name__ == '__main__':
    data = {
        "id": "root",
        "name": "Multi-Layer Example",
        "children": [
            {
                "id": "node_1",
                1: "Layer 1 - Node A",
                "type": "category",
                "data": {
                    "id": "internal_1",
                    "value": 100,
                    "rules": [
                        {
                            "id": "rule_1",
                            "condition": "if (x > 0)",
                            "actions": {
                                "id": "action_1",
                                "target": "output",
                                "params": {
                                    "id": "param_1",
                                    "type": "int",
                                    "constraints": {
                                        "id": "constraint_1",
                                        "min": 0,
                                        "max": 100
                                    }
                                }
                            }
                        }
                    ]
                },
                "children": [
                    {
                        "id": "node_1_1",
                        "name": "Layer 2 - Leaf A1",
                        "type": "item",
                        "metadata": {
                            "id": "meta_1",
                            "created": "2023-01-01",
                            "tags": [
                                "tag1",
                                "tag2"
                            ],
                            "nested": {
                                "id": "nested_1",
                                "priority": "high"
                            }
                        }
                    },
                    {
                        "id": "node_1_2",
                        "name": "Layer 2 - Leaf A2",
                        "type": "item",
                        "metadata": {
                            "id": "meta_2",
                            "created": "2023-01-02",
                            "tags": [
                                "tag3"
                            ],
                            "nested": {
                                "id": "nested_2",
                                "priority": "low"
                            }
                        }
                    }
                ]
            },
            {
                "id": "node_2",
                "name": "Layer 1 - Node B",
                "type": "category",
                "data": {
                    "id": "internal_2",
                    "value": 200,
                    "rules": [
                        {
                            "id": "rule_2",
                            "condition": "if (x < 0)",
                            "actions": {
                                "id": "action_2",
                                "target": "input",
                                "params": {
                                    "id": "param_2",
                                    "type": "float",
                                    "constraints": {
                                        "id": "constraint_2",
                                        "min": -1,
                                        "max": 1
                                    }
                                }
                            }
                        }
                    ]
                },
                "children": [
                    {
                        "id": "node_2_1",
                        "name": "Layer 2 - Leaf B1",
                        "type": "item",
                        "metadata": {
                            "id": "meta_3",
                            "created": "2023-01-03",
                            "tags": [
                                "tag2",
                                "tag4"
                            ],
                            "nested": {
                                "id": "nested_3",
                                "priority": "medium"
                            }
                        },
                        "children": [
                            {
                                "id": "node_2_1_1",
                                "name": "Layer 3 - Subleaf B1-1",
                                "type": "detail",
                                "metadata": {
                                    "id": "meta_4",
                                    "created": "2023-01-04",
                                    "nested": {
                                        "id": "nested_4",
                                        "priority": "critical"
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "metadata": {
            "id": "root_meta",
            "lang": {
                "id": "language",
            },
            "version": "1.0",
            "description": "This JSON intentionally contains duplicate keys at every level."
        }
    }
    rules = '["children"][0][1]'
    rules = '["children"]["*"]["data"]["rules"][0]["id"]'
    rules = ",".join(rules.split(']['))
    print(rules, type(rules))
    rules = json.loads(rules)

    for i in ServiceParseJson().parse_json(data, rules):
        print("result:", i)
