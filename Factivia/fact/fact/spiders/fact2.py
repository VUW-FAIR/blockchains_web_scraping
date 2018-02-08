import time
from urllib.parse import urljoin

import requests
import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import os


class ProductSpider(scrapy.Spider):
    os.environ["LANG"] = "en_US.UTF-8"
    name = "fact2"
    start_urls = ['http://helicon.vuw.ac.nz/login?url=http://global.factiva.com/en/sess/login.asp?xsid=S003cb93WvtZWni5DEs5DEmMT2mM96rMp3yMHmnRsIuMcNG1pRRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQAA']

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='../chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        print(self.driver.page_source)

        # Navigate to page and
        try:
            inputElement = self.driver.find_element_by_id("ftx")
            if (inputElement != None):
                inputElement.send_keys('bitcoin')
                self.driver.find_element_by_xpath("//select[@name='dr']/option[text()='All Dates']").click()

                print("yeet")
                inputElement.send_keys(Keys.ENTER)
                time.sleep(1)
                # yield scrapy.Request(url=self.driver.current_url, callback=self.parse_pages)
        except:
            print("no searchbox found")

        try:
            self.driver.find_element_by_xpath('//*[@id="headlineTabs"]/table[1]/tbody/tr/td/span[2]/a').click()
            print("clicked on all")
            time.sleep(1)
        except:
            print("Can't find all button")


        with open("fact_page.txt", "w", encoding="utf-8") as text_file:
            text_file.write(self.driver.page_source)




        while True:
            self.wait_random_amount(min = 1, max = 3)
            try:
                print("getting links")

                soup = BeautifulSoup(self.driver.page_source)
                links = soup.findAll("a", { "class" : "enHeadline" }, href=True)

                # links = self.driver.find_elements_by_xpath('//*[contains(@class,"enHeadline")]//@href').extract()
                print(len(links))
                for url in links:
                    url = response.urljoin(url['href'])
                    url = url.replace("en/", "")

                    # # open new tab
                    # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') #test

                    yield scrapy.Request(url=url, callback=self.parse_page, meta={'the_url': url})
            except Exception as exc:
                print("no links found")
                print(exc)
                print(type(exc))

            self.wait_random_amount(min = 1, max = 2)
            try:
                self.driver.find_element_by_xpath('//*[@class="nextItem"]').click()
                print("next page")
            except Exception as exc:
                print("no next button")
                print(exc)
                print(type(exc))

        self.driver.close()


    def parse_page(self, response):
        print("here")

        #open new tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

        # Load a page
        self.driver.get(response.meta['the_url'])

        try:
            self.driver.find_element_by_xpath('//*[@title="Download Articles in RTF Format"]').click()
            self.wait_random_amount(min = 2, max = 5)
            # self.driver.find_element_by_link_text('Download Articles in RTF Format')
            self.driver.find_element_by_xpath('//*[@id="listMenu-id-3"]/li[3]/a').click()
            self.wait_random_amount(min = 1, max = 4)
            print("downloaded")
        except Exception as inst:
            print("no download buttons found")
            print(inst)
            print(type(inst))

        #close tab
        print("close")
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    def wait_random_amount(self, min, max):
        time.sleep(random.randint(min, max))