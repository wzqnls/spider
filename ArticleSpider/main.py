#!/usr/bin/env python
# encoding: utf-8

"""
@author: lee 
@file: main.py
@time: 2017/5/24 23:49
"""


import sys
import os

from scrapy.cmdline import execute


# print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])