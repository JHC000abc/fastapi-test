# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_device.py
@time: 2025/7/8 20:55 
@desc: 

"""
import os
import platform
import re
from utils.utils_cmd import CMDUtils


class DeviceUtils:
    """
    设备工具类
    """

    @staticmethod
    def get_wechat_wxid(folder=None):
        """
        获取设备上登陆的 微信 wxid
        :param folder:仅针对Windows平台自定义数据存储路径生效
        :return:
        """
        wxids = []
        system = DeviceUtils().get_system()
        if system == "Windows":
            if not folder:
                file = os.path.join(
                    os.environ['USERPROFILE'],
                    'Documents',
                    'WeChat Files',
                    'All Users',
                    'config',
                    'config.data'
                )
            else:
                file = os.path.join(
                    folder,
                    'All Users',
                    'config',
                    'config.data'
                )
            with open(file, "rb") as f:
                data = f.read()
            data_matches = re.findall(r'(wxid_.*?)\\\\config', str(data))
            if len(data_matches) > 0:
                wxids.extend(data_matches)
        elif system == "Linux":
            user = CMDUtils.run_await_results(cmd=['whoami'])
            for folder in ('文档', 'Documents'):
                file = f'/home/{user}/{folder}/xwechat_files/all_users/login'
                if os.path.exists(file):
                    file_list = os.listdir(file)
                    if len(file_list) > 0:
                        for filename in file_list:
                            if filename.startswith('wxid_'):
                                wxids.append(filename)
        elif system == "Darwin":
            user = CMDUtils.run_await_results(cmd=['whoami'])
            file = f"/Users/{user}//Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/all_users/login"
            if os.path.exists(file):
                file_list = os.listdir(file)
                if len(file_list) > 0:
                    for filename in file_list:
                        if filename.startswith('wxid_'):
                            wxids.append(filename)

        msg = f"{system} 识别到微信{len(wxids)}个" if len(wxids) > 0 else f"{system} 未识别到微信"
        print(msg)
        return wxids

    @staticmethod
    def get_system():
        system = platform.system()
        if system in ('Windows', 'Linux', 'Darwin'):
            return system
        return "Unsupported OS"


if __name__ == '__main__':
    folder = input("input folder:")
    print(DeviceUtils.get_wechat_wxid(folder))
