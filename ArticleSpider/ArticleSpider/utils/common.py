#!/usr/bin/env python
# encoding: utf-8

"""
@author: lee 
@file: common
@time: 2017/5/31 20:11
"""
import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
