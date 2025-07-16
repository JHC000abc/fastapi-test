# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: service_sign.py
@time: 2025/6/20 21:17 
@desc: 

"""
import re
import requests
import json


class ServiceSign:
    """

    """

    def __init__(self):
        self.jd_url = "https://api.m.jd.com/client.action?functionId=signBeanAct&body=%7B%22fp%22%3A%22-1%22%2C%22shshshfp%22%3A%22-1%22%2C%22shshshfpa%22%3A%22-1%22%2C%22referUrl%22%3A%22-1%22%2C%22userAgent%22%3A%22-1%22%2C%22jda%22%3A%22-1%22%2C%22rnVersion%22%3A%223.9%22%7D&appid=ld&client=apple&clientVersion=10.0.4&networkType=wifi&osVersion=14.8.1&uuid=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6&openudid=3acd1f6361f86fc0a1bc23971b2e7bbe6197afb6&jsonp=jsonp_1645885800574_58482";
        self.jd_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "referer": "https://plogin.m.jd.com/",
            "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
        self.jd_cookies = {
            "wxa_level": "1",
            "retina": "0",
            "cid": "9",
            "jxsid": "17504804640237725513",
            "appCode": "ms0ca95114",
            "webp": "1",
            "__jda": "122270672.17504804640351386742392.1750480464.1750480464.1750480464.1",
            "__jdv": "122270672%7Cdirect%7C-%7Cnone%7C-%7C1750480464035",
            "__jdc": "122270672",
            "mba_muid": "17504804640351386742392",
            "visitkey": "5543035100892385302",
            "3AB9D23F7A4B3CSS": "jdd03QCVXCTC5KIPXEPJJTMHFKKLNE7V42O5YEEWHPBUAVQMXYFG3V6GZIHPEVLOSNEFK2O45S62BRCOA4IWQDFVBCALOJEAAAAMXSDCC4WQAAAAAD6G6BOQQDMFBIEX",
            "3AB9D23F7A4B3C9B": "QCVXCTC5KIPXEPJJTMHFKKLNE7V42O5YEEWHPBUAVQMXYFG3V6GZIHPEVLOSNEFK2O45S62BRCOA4IWQDFVBCALOJE",
            "_gia_d": "1",
            "cd_eid": "jdd03QCVXCTC5KIPXEPJJTMHFKKLNE7V42O5YEEWHPBUAVQMXYFG3V6GZIHPEVLOSNEFK2O45S62BRCOA4IWQDFVBCALOJEAAAAMXSDCC4WQAAAAAD6G6BOQQDMFBIEX",
            "shshshfpa": "b4a12cb4-77c1-a6ea-f8b9-3d315a797546-1750480476",
            "shshshfpx": "b4a12cb4-77c1-a6ea-f8b9-3d315a797546-1750480476",
            "shshshfpb": "BApXSTszMk_JAV4KkhYZIXkpwVEbhv8ScBhIJA1lo9xJ1MuANS462",
            "jcap_dvzw_fp": "pHscSLclTjd-b5aN_Za74qj-CsTddQFGHdFuHZh1_LbtmrcKQmFoJE-yYZ1cYhPffL8ltIOyk88sTliK-kt7yQ==",
            "TrackerID": "ZTar96a2AWiUV1tcrNf7OdKYYYzj-_YeER-f3O5fE0EzrcNLDNLFYIccgfN5V5TG2OfJlT7WoLpxS_FyhVolaJ6dWABoOFO21cXI4BEhCLs",
            "pt_key": "AAJoVjaPADAnAez5cWfPOkdEOqoXFStPzWvLAF1cm7InjYpgd2uRiCqr4L3gG4schRWEq_PR7WE",
            "pt_pin": "jd_4f775868cad90",
            "pt_st": "1_KS5omB7HONyL3mxbgwXifvUxfTeGpRKG96UqZgt-BiP2XLcLou9c6zT29XPVryEvP_5ccmKmWBoveBIa98rkcdgvFa_4SrmIgLJI2-v7kLXClr47AwtVdolt1X_ZX9YIP5aCn1cR1-3Hd-mx_pAqSobsqbkgy01Dpd2TldJtwYKt6Q8GO2tXXaS1jAmfc8uhrPI6_dLW3VaoyPIl6tKpsSxHL_uMkwMPutW2F_Cn",
            "pt_token": "2l0jjboc",
            "pwdt_id": "jd_4f775868cad90",
            "sfstoken": "tk01ma5f11bf9a8sMSszeDIrM2h1hk97hGuw5Me14dG15tIBvTZ0w5t+c+QRgLnubyYsNTxTaG7tnmv5JNG3MW3bWua0",
            "whwswswws": "",
            "wqmnx1": "MDEyNjM5OG0xMTNhMXhwdChpKTEgMzM0MktFRigl",
            "__jdb": "122270672.3.17504804640351386742392|1.1750480464",
            "mba_sid": "17504804640362034745934.3",
            "autoOpenApp_downCloseDate_jd_homePage": "1750480530842_1",
            "__jd_ref_cls": "MSearch_DarkLines",
            "sdtoken": "AAbEsBpEIOVjqTAKCQtvQu17UK5RTWttHCwoaXrjjocGgJgirQX9L-0JkL_Q4sM_8kbhhjuf-sfs7dlU52ZxfDvqmUzOtHfrHiTXWtpShtDWae0e5dYGPQ"
        }

    def sign_jd(self, token, ua=None):
        """
        京东签到
        :param token:
        :return:
        """
        self.jd_cookies["pt_key"] = token
        if ua:
            self.jd_headers["user-agent"] = ua
        response = requests.post(url=self.jd_url, headers=self.jd_headers, cookies=self.jd_cookies)
        response.encoding = "utf-8"
        return response.text

    def parse_jd(self, html):
        """

        :param html:
        :return:
        """
        res = re.findall("jsonp_1645885800574_58482\((.*?)\)", str(html), flags=re.DOTALL)
        res = res[0]
        print(res)
        if len(res) <= 0:
            return html
        json_res = json.loads(res)
        if json_res["code"] == "0":
            data = json_res["data"]
            continuityAward = data.get("continuityAward",data.get("dailyAward"))
            title = continuityAward["title"]
            return title
        elif json_res["code"] in ("3", "402"):
            return json_res.get("errorMessage", json_res.get("message"))
        else:
            return json.dumps(json_res, ensure_ascii=False, indent=4)

    def process(self,token=None):
        """

        :return:
        """
        if not token:
            token = "AAJoXVT8ADD3qhTpn-SB6quEIeyBlRT9MKPdlU9euD0qFdCCwuSGVJFeMxQm2RuD03wZ8paEAGM"
        html = self.sign_jd(token)
        res = self.parse_jd(html)
        print(res)
        return res


if __name__ == '__main__':
    service = ServiceSign()
    service.process()
