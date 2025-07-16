# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_folder.py
@time: 2025/6/17 20:39 
@desc: 

"""
import os


class FolderUtils:
    """

    """

    def get_all_files(self, path, ext=None):
        """

        :param path:
        :param ext:
        :return:
        """
        if os.path.exists(path) and os.path.isabs(path):
            for path, dir_lis, file_lis in os.walk(path):
                if len(file_lis) > 0:
                    for name in file_lis:
                        if ext:
                            if os.path.splitext(name)[-1] in ext:
                                yield os.path.join(path, name), name
                        else:
                            yield os.path.join(path, name), name
