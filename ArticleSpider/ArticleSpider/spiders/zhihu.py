# -*- coding: utf-8 -*-
import scrapy
import re
import json
import requests


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
    # headers = {
    #     "HOST": "www.zhihu.com",
    #     "Referer": "https://www.zhihu.com",
    #     "User-Agent": agent
    # }
    agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        'User-Agent': agent
    }

    # 使用登录cookie信息
    session = requests.session()

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.login)]

    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        xsrf = ""
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": 'xxx',
                "password": 'xxx',
                "captcha": self.get_captcha()
            }

            return [scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.headers,
                callback=self.check_login
            )]

    def get_captcha(self):
        # 获取验证码
        import time
        t = str(int(time.time() * 1000))
        captcha_url = "https://www.zhihu.com/captcha.gif?r={}&type=login".format(t)
        # captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        t = self.session.get(captcha_url, headers=self.headers)
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

    def check_login(self, response):
        # 验证服务器返回数据是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)
        pass
