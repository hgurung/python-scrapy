import scrapy

import re 

from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class CheckinSpider(scrapy.Spider):
    name = "checkin"

    checkin_url = 'https://oa.ekbana.info/checkIncheck'
    checkout_url = 'https://oa.ekbana.info/checkOutcheck'
    redirect_url = 'https://oa.ekbana.info/dashboard'
    checkin_checkout_type = ''
    handle_httpstatus_list = [301, 302]
    username = ''
    password = ''

    def __init__(self, checktype=None, username=None, password=None, *args, **kwargs):
        super(CheckinSpider, self).__init__(*args, **kwargs)
        if checktype is not None and username is not None and password is not None:
            self.checkin_checkout_type = checktype
            self.username = username
            self.password = password
            print(checktype)
            self.start_urls = [
                'https://oa.ekbana.info/login',
            ]
        else:
            print('Please provide valid attributes like -a checktype=checkin -a username=harris -a password=harris')

    def parse(self, response):
        token = response.xpath('//*[@name="_token"]/@value').extract_first()
        return scrapy.FormRequest.from_response(response, 
                                     formdata={'csrf_token': token,
                                                'password': self.password,
                                                'username': self.username}, 
                                     callback=self.after_login)
                                

    def after_login(self, response):
        open_in_browser(response)

        # token = response.xpath("//meta[@name='csrf-token']/@content").extract_first()
        # cookie = response.headers.getlist('Set-Cookie')[0].split(';')[0].split("=")[1]
        # # open_in_browser(response)
        # return scrapy.Request(
        #     url="https://qa-oa.ekbana.info/profile",
        #     callback=self.checkin,
        #     meta={"csrf-token": token, 'X-CSRF-TOKEN': token},
        #     cookies={'XSRF-TOKEN': cookie},
        # )
        # print response.url

        if response.url != self.redirect_url:
            print('Invalid username password')
            return

        if self.checkin_checkout_type == 'checkin':
            return scrapy.Request(
                url=self.checkin_url,
                dont_filter=True,
                callback=self.checkin,
            )
        if self.checkin_checkout_type == 'checkout':
            return scrapy.Request(
                url=self.checkout_url,
                dont_filter=True,
                callback=self.checkout,
            )
    
    def checkin(self, response):
        print('If it is not redirected then check in successfull')
        open_in_browser(response)

    def checkout(self, response):
        print('If it is not redirected then check out successfull')
        open_in_browser(response)


        