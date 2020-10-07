import scrapy

import re 

from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

import time

import selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckinSpider(scrapy.Spider):
    name = "medpg"

    redirect_url = 'url'
    # handle_httpstatus_list = [301, 302]
    username = ''
    password = ''

    def __init__(self, checktype=None, username=None, password=None, *args, **kwargs):
        super(CheckinSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome('C:\selenium\selenium-java-3.141.59\chromedriver_win32\chromedriver')

        # if username is not None and password is not None:
        #     self.username = username
        #     self.password = password
        #     self.start_urls = [
        #         'https://edge.medpgbasics.com/login',
        #     ]
        # else:
        #     print('Please provide valid attributes like -a checktype=checkin -a username=harris -a password=harris')
        self.start_urls = [
            'https://url/login',
        ]


    def parse(self, response):
        # token = response.xpath('//*[@name="csrfmiddlewaretoken"]/@value').extract_first()
        # return scrapy.FormRequest.from_response(response, 
        #                             formdata={'csrfmiddlewaretoken': token,
        #                                         'password': self.password,
        #                                         'username': self.username}, 
        #                             callback=self.after_login)
        self.driver.get(response.url)  
        username = WebDriverWait(self.driver, 20).until(lambda driver: self.driver.find_element_by_xpath('//*[@id="id_username"]'))
        password = WebDriverWait(self.driver, 20).until(lambda driver: self.driver.find_element_by_xpath('//*[@id="id_password"]'))
        login_button = WebDriverWait(self.driver, 20).until(lambda driver: self.driver.find_element_by_xpath('//*[@class="tp-btn btn-block"]'))

        username.send_keys("youremail@gmail.com")
        password.send_keys("1234567")
        login_button.click()

        # print("*****")
        # print(self.driver.current_url)
        # print("*****")

        yield scrapy.Request (url = self.driver.current_url,
                       callback = self.after_login, #, dont_filter = True,
                    #    meta = {'dont_redirect' : True,
                    #            'handle_httpstatus_list': [302],
                    #            'cookiejar' : response.meta['cookiejar'] }
                       )                          

    def after_login(self, response):
        # print"***"
        # print(response.url)
        # print"***"
        self.driver.get(self.redirect_url)
        yield scrapy.Request (
                        url = self.driver.current_url,
                        callback = self.subjectLists,
                       )    
        # yield scrapy.Request(
        #     url="https://edge.medpgbasics.com//chapters/subject-tests",
        #     callback=self.subjectLists,
        # )
    
    def subjectLists(self, response):

        # Row fluid data

        try:
            articles = WebDriverWait(self.driver, 50).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='row-fluid clearfix']")))
            for result in articles:
                title = result.find_element_by_xpath('.//div[@class="item-title"]')
                print(title.text)



            # # WebDriverWait(self.driver,50).until(EC.visibility_of_all_elements_located(By.CLASS_NAME, "row-fluid clearfix"))

            # # Get the list of post
            # listpost = self.driver.find_elements_by_class_name("row-fluid clearfix")

            # for (WebElement element : elements) {
            #     System.out.println(element.getText());  
            # }

            # # articleData = response.xpath('//div[@class="row-fluid clearfix"]')
            # print(listpost)
            # # articles.get_attribute("value")
        finally:
            self.driver.quit()
        # time.sleep(50)
        # articles = response.xpath('//div[@class="row-fluid"]')
        # print(articles)
        # for article in articles:

        # self.driver.get(response.url)

        # print('If it is not redirected then check in successfull')
        # time.sleep(10)
        # open_in_browser(response)


        