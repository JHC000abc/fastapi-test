# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_cmd.py
@time: 2025/7/8 21:53 
@desc: 

"""
import subprocess
from typing import Union, List, Callable, Optional
import threading


class CMDUtils:
    """

    """

    @staticmethod
    def run_await_results(cmd: Union[str, List[str]],
                          timeout: Optional[int] = None) -> str:
        """
        阻塞执行命令并返回结果（自动剥离首尾空格）

        :param cmd: 命令（字符串或列表形式）
        :param timeout: 超时时间（秒）
        :return: 命令输出（stdout 或 stderr）
        :raises: subprocess.CalledProcessError 当命令返回非零状态码时
        """
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=isinstance(cmd, str),
            timeout=timeout
        )
        return result.stdout.strip()

    @staticmethod
    def run_background(cmd: Union[str, List[str]],
                       **kwargs) -> subprocess.Popen:
        """
        后台非阻塞执行命令

        :param cmd: 命令（字符串或列表形式）
        :param kwargs: 传递给 subprocess.Popen 的额外参数
        :return: Popen 对象（可通过 returncode 属性检查状态）
        """
        return subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=isinstance(cmd, str),
            **kwargs
        )

    @staticmethod
    def run_realtime_output(cmd: Union[str, List[str]],
                            output_handler: Callable[[str], None] = print,
                            **kwargs) -> subprocess.Popen:
        """
        实时输出命令执行结果（非阻塞）

        :param cmd: 命令（字符串或列表形式）
        :param output_handler: 自定义输出处理函数（默认打印到控制台）
        :param kwargs: 传递给 subprocess.Popen 的额外参数
        :return: Popen 对象
        """

        def _enqueue_output(pipe, handler):
            for line in iter(pipe.readline, ''):
                handler(line.strip())
            pipe.close()

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=isinstance(cmd, str),
            **kwargs
        )

        # 启动独立线程处理输出
        threading.Thread(
            target=_enqueue_output,
            args=(proc.stdout, output_handler),
            daemon=True
        ).start()

        return proc
