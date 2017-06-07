# -*- coding: utf-8 -*-
import scrapy
import re
import json
import requests
from urllib import parse


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": agent
    }

    # 使用登录cookie信息
    session = requests.session()

    def parse(self, response):
        """
        提取出html所有url并跟踪这些url进一步爬去
        如果提取的url格式为/question/xxxx 下载后直接解析
        """

        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        for url in all_urls:
            pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com', headers=self.headers, callback=self.login)]

    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        xsrf = ""
        if match_obj:
            xsrf = match_obj.group(1)

        if xsrf:
            post_data = {
                "_xsrf": xsrf,
                "phone_num": '13735846612',
                "password": 'codewithpython666',
                "captcha": ""
            }

            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={}&type=login".format(t)
            # captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
            yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data}, callback=self.login_after_captcha)

    def login_after_captcha(self, response):
        with open("captcha.jpg", 'wb') as f:
            f.write(response.body)

        from PIL import Image

        im = Image.open('captcha.jpg')
        im.show()
        im.close()

        captcha = input("输入验证码:\n")

        post_data = response.meta.get("post_data")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        # 验证服务器返回数据是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)
        pass