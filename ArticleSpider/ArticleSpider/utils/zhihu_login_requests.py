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
    "User-Agent": agent
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


# zhihu_login("xxx", "xxx")
# get_index()
# is_login()
get_captcha()
