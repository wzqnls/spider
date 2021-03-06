#!/usr/bin/env python
# encoding: utf-8

"""
@author: lee 
@file: common
@time: 2017/5/31 20:11
"""
import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(text):
    # 从字符串中提取数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums