#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-6-5 上午10:53
# @Author  : Lee
# @File    : zhihu_login_requests.py

import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re


session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')

try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookie cant load')

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent,
    "Cookie": '_zap=642b08d3-8a8e-4315-9106-4d50575a83f0; d_c0="ADCCQ9n8jguPTl8hT8C09d5jr0zYn01qIf4=|1491354302"; _xsrf=8f4b634af92924d53105835f6642d7ae; q_c1=c58346dd707c4204a550d5be3816a131|1496384287000|1490859537000; q_c1=c58346dd707c4204a550d5be3816a131|1496384287000|1490859537000; r_cap_id="YTRmZjc4YjVkNjg5NDJiZGI2YTI4MDgyZTU3NDhhMDQ=|1496751809|063ac05236a1140b31db22a91211e990f059ff2b"; cap_id="YjMxNGNmNjFiYTE5NGFhY2E1M2M5OGI3MTlmOWRmY2I=|1496751809|1722375a042de0d5d888b762424292f86e03729b"; __utma=51854390.315060952.1496629119.1496751864.1496800847.10; __utmb=51854390.0.10.1496800847; __utmc=51854390; __utmz=51854390.1496751864.9.6.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20140502=1^3=entry_date=20140502=1; z_c0=Mi4wQUFDQWFjQXRBQUFBTUlKRDJmeU9DeGNBQUFCaEFsVk45Q3RlV1FCcEI3eWl2ejRPZlV2c2o5M1M1TkFWbThRSzNn|1496800849|1b491da84674cdc53b42f94eaa34a430a2f2aacc'
}


def get_xsrf():
    # 获取xsrf
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", 'wb') as f:
        f.write(response.text.encode('utf8'))
    print('ok')


def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print("phone_num login")
        post_url = "https://www.zhihu.com/login/phone_num"

        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha()
        }
    else:
        if "@" in account:
            print('email login')
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
                "captcha": get_captcha()
            }
    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()


def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={}&type=login".format(t)
    # captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg", 'wb') as f:
        f.write(t.content)

    from PIL import Image
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n")
    return captcha


def is_login():
    # 通过个人中心页面返回状态码判断是否为登录状态
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def test_login():
    post_url = "https://www.zhihu.com"
    response = session.get(post_url, headers=header)
    pass


# zhihu_login("xxx", "xxx")
# get_index()
# is_login()
# get_captcha()
test_login()