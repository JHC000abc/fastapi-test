# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: service_slider.py
@time: 2025/6/25 17:24 
@desc: 

"""
import ddddocr


class ServiceSlider:
    """

    """

    def __init__(self, background_data, slider_data):
        self.background = background_data
        self.slider = slider_data
        self.ocr = None
        self.get_ocr()

    def get_ocr(self):
        """

        :return:
        """
        if not self.ocr:
            self.ocr = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)

    def get_options(self):
        """

        :return:
        """
        self.get_ocr()
        options = self.ocr.slide_match(self.slider, self.background, simple_target=True)
        print("options", options)
        return options

