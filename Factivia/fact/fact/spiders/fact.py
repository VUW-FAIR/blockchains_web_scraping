# -*- coding: utf-8 -*-
import csv

import os
import scrapy
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CommitsSpider(scrapy.Spider):

    name = "fact"
    start_urls = ['http://helicon.vuw.ac.nz/login?url=http://global.factiva.com/en/sess/login.asp?xsid=S003cb93WvtZWni5DEs5DEmMT2mM96rMp3yMHmnRsIuMcNG1pRRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQAA']


    def parse(self, response):
        #//*[@id="ftx"]

        #inputElement = response.selector.xpath('//*[@id="ftx"]').extract()[0]


        print(str(response))
        print("hi")

        # try:
        #     nextPage = response.selector.xpath('//*[contains(@class, "nextItem")]//@href').extract()
        #
        #     for page in nextPage:
        #         print(str(page))
        #         url = response.urljoin(page)
        #         yield scrapy.Request(url=page, callback=self.parse)
        # except:
        #     print("no nextpage button")

        try:
            links = response.selector.xpath('//*[contains(@class,"enHeadline")]//@href').extract()
            print(len(links))
            for url in links:
                print("hello" + str(url) + "end")
                url = response.urljoin(url)
                print(url)
                yield scrapy.Request(url=response, callback=self.parse)
        except:
            print("no links")


            # def parse_pages(self, response):
            #     self.driver.get(response.url)
            #     while True:
            #         time.sleep(1)
            #         try:
            #             links = self.driver.selector.xpath('//*[contains(@class,"enHeadline")]//@href').extract()
            #             print(len(links))
            #             for url in links:
            #                 url = response.urljoin(url)
            #                 print(url)
            #                 yield scrapy.Request(url=url, callback=self.parse_page)
            #         except:
            #             print("no links found")
            #
            #         time.sleep(1)
            #         try:
            #             self.driver.find_element_by_xpath('//*[@class="nextItem"]').click()
            #             print("next page")
            #         except Exception as exc:
            #             print("no next button")
            #             print(exc)
            #             print(type(exc))
            #
            #     self.driver.close()
