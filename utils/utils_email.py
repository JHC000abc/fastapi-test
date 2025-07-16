# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_email.py
@time: 2025/6/20 21:30 
@desc: 

"""
import smtplib
from email.mime.text import MIMEText
from conf.conf_email import conf_email


class EmailSend(object):
    """

    """

    def __init__(self):
        self.mail_host = conf_email.get("mail_host")
        self.password = conf_email.get("password")
        self.sender = conf_email.get("sender")
        self.title_list = None
        self.content_list = None
        self.recv_list = None

    def load_send_info(self, recv_list, title_list, content_list):
        """

        :param recv_list:
        :param title_list:
        :param content_list:
        :return:
        """
        self.recv_list = recv_list
        self.title_list = title_list
        self.content_list = content_list
        if recv_list:
            self.recv_list = recv_list
            self.send()

    def init_message(self, receiver, title, content):
        """

        :return:
        """
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = title
        message['From'] = self.sender
        message['To'] = receiver
        return message

    def send_email(self, receiver, message):
        """

        :param receiver:
        :param message:
        :return:
        """
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(self.mail_host, 25)
            # 登录到服务器
            smtpObj.login(self.sender, self.password)
            # 发送
            smtpObj.sendmail(
                self.sender, receiver, message.as_string())
            # 退出
            smtpObj.quit()
            print(f'{receiver} send success')
        except smtplib.SMTPException as e:
            print(f'{receiver} send failed')
            print('error', e)  # 打印错误

    def send(self):
        """

        :return:
        """
        for recv, title, content in zip(self.recv_list, self.title_list, self.content_list):
            message = self.init_message(recv, title, content)
            self.send_email(recv, message)


if __name__ == '__main__':
    es = EmailSend()
    es.load_send_info(["JHC000abc@gmail.com", "3237558741@qq.com"], ["测试邮件", "测试邮件"],
                      ["测试邮件1", "测试邮件1"])
