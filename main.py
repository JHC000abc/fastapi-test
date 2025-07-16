# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: main.py
@time: 2025/6/13 22:22 
@desc: 

"""
import uvicorn
from conf.conf_base import DEBUG


def run_online(app):
    """

    :return:
    """
    print("start online mode")
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)


def run_debug(app):
    """

    :param app:
    :return:
    """
    print("start debug mode")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


if __name__ == '__main__':
    app = "apps.register:app"
    if DEBUG:
        run_debug(app)
    else:
        run_online(app)

# git push https://$GITUSERNAME:$GITPWD@github.com/JHC000abc/fastapi-test.git main