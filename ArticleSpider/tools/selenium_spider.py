#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-6-21 下午2:18
# @Author  : Lee
# @File    : selenium_spider.py

from selenium import webdriver
from scrapy.selector import Selector

# browser = webdriver.Chrome(executable_path="/home/lee/Downloads/chromedriver")
#
# browser.get("https://www.zhihu.com/#signin")
#
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys('13735846612')
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys('codewithpython666')
#
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()

# t_selector = Selector(text=browser.page_source)
# test = t_selector.css(".tm-promo-price .tm-price::text").extract()
# print(test)

# 微博模拟登录
# browser.get("https://www.weibo.com")
#
# import time
# time.sleep(10)
# browser.find_element_by_css_selector("#loginname").send_keys("")
# browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys("")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

# 设置chromedriver不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(executable_path="/home/lee/Downloads/chromedriver", chrome_options=chrome_opt)
browser.get("https://www.taobao.com")



# browser.quit()