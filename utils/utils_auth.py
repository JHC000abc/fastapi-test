# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_auth.py
@time: 2025/6/16 20:53 
@desc: 

"""
from jose import jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from conf.conf_base import TOKEN_EXPIRE


class JwtHandler(object):
    """
    JWT 验证
    """

    def __init__(self, interval=TOKEN_EXPIRE, secret=None):
        """

        """
        # 密钥
        self.secret = "fb565ca799a431a5a4102d10ff84cb3661bb0cf0f415e7" \
                      "8cc389ad42ced61fa4dcb3c635a4f5568697526549ed5dee3" \
                      "a5e791d100ce4f9a95c0728e3b617dc07f575edea41ee6152f08" \
                      "6651719606abba2806ea8845ea4d53a2a91e14c31f1ae825a8c00" \
                      "47b05bf580108cb9af7db40a6ed9f0fb2a1802b6eb1823528b68706b"
        # 加密算法
        self.algorithm = "HS256"
        # 默认30秒过期
        self.interval = interval
        # 密钥对象
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hash_code(self, pwd):
        """
        获取密码对应的 hash 值
        :param pwd:
        :return:
        """
        return self.pwd_context.hash(pwd)

    def verify_hash_code(self, pwd, hash_code):
        """
        验证密码和hash是否匹配
        :param pwd:
        :param hash_code:
        :return:
        """
        return self.pwd_context.verify(pwd, hash_code)

    def create_token(self, key: str = None, data: dict = None):
        """
        创建带exp字段的JWT字符串
        :param key:
        :param data:
        :return:
        """
        if not (key or data):
            raise ValueError("key or data must be provided")

        # 创建一个包含key（如果提供）和用户数据的字典
        payload = {}
        if key:
            payload['key'] = key
        if data:
            payload.update(data)

        # 设置过期时间
        expires_delta = timedelta(seconds=self.interval)
        expire = datetime.now(timezone.utc) + expires_delta

        # 将过期时间添加到payload中
        payload['exp'] = int(expire.timestamp())

        # 使用SECRET_KEY对声明集进行签名并编码为JWT字符串
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)

        return token

    def decrypt_token(self, token):
        """
        解析 token
        :param token:
        :return:
        """
        try:
            res = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return True, res
        except ExpiredSignatureError:
            return False, ""


if __name__ == '__main__':
    jwt_handler = JwtHandler()
    passowrd = '123456'
    pwd_hash = jwt_handler.get_hash_code(passowrd)
    print(pwd_hash, len(pwd_hash))
    token = jwt_handler.create_token(passowrd)
    print(token)
    jwt_data = jwt_handler.decrypt_token(token)
    print("jwt_data", jwt_data)
    passowrd = "34325234525"
    verify = jwt_handler.verify_hash_code(passowrd, pwd_hash)
    print(verify)
