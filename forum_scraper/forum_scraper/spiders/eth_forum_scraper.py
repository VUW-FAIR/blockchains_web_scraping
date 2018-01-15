import csv
import json
import os
import scrapy
import time
from bs4 import BeautifulSoup

class eth_forum_scraper(scrapy.Spider):
    name = "eth"
    forum_folder_name = "ethereum_community_forum"
    start_urls = ['https://forum.ethereum.org/']

    ''''
    This web scraper can be used to web scrape all posts from the ethereum community forum at https://forum.ethereum.org/. 
    '''
    def parse(self, response):
        print("in main parse")

        if not os.path.exists(self.forum_folder_name):
            os.makedirs(self.forum_folder_name)

        category_links = response.selector.xpath('//tr[contains(@class, "Item Category")]//div[contains(@class, "Wrap")]/a[@class ="Item-Icon PhotoWrap PhotoWrap-Category Hidden NoPhoto"]/@href').extract()
        print(category_links)
        for link in category_links:
            url = response.urljoin(link)
            yield scrapy.Request(url=url, callback=self.parse_category)


    '''
    Parsing category which contains multiple pages of information
    '''
    def parse_category(self, response):
        forum_post_links = response.xpath('//a[@class = "Title"]/@href').extract()

        for link in forum_post_links:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_page)

        try:
            next_button = response.selector.xpath('//a[@class = "Next"]/@href').extract()
            if(len(next_button) >= 1):
                print("going to next category page!")
                url = response.urljoin(next_button[0])
                time.sleep(10)
                yield scrapy.Request(url=url, callback=self.parse_category)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")


    '''
    Parsing the individual pages including all posts and relevant information on the page
    '''
    def parse_page(self, response):

        soup = BeautifulSoup(response.body, 'html.parser')
        title = response.selector.xpath('//h1/text()').extract()
        # usernames = response.selector.xpath('//a[@class = "Username"]/@href').extract()
        usernames = soup.find_all('a', attrs={'class': 'Username'})
        # item_headers = response.selector.xpath('//div[contains(@class, "Item-Header")]/text()').extract()

        item_headers = soup.find_all('div', attrs={'class': 'Item-Header'})

        messages = soup.find_all('div', attrs={'class': 'Message'})


        print('usernames' + str(len(usernames)))
        print('item headers' +  str(len(item_headers)))
        print('messages' +  str(len(messages)))

        # Opening CSV file and removing symbols that system may not like
        csv_file = open(".\\" + self.forum_folder_name + "\\" + title[0].replace("/", "").replace("\\", "").replace("|", "").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace(":", "").replace("-", "_").replace(".", "") + ".csv", "a", encoding="utf-8") #or append?

        writer = csv.writer(csv_file, delimiter=",")

        if(len(usernames) == len(item_headers) == len(messages)):
            # Writing to the csv file
            for i in range(0, len(usernames)):
                print(usernames[i].text.strip())
                print(item_headers[i].text.strip())
                print(messages[i].text.strip())
                writer.writerow([(title[0].strip()), (item_headers[i].text.strip()), usernames[i].text.strip(), (messages[i].text.strip())])
        else:
            print("number of usernames doesn't match up messages")

        csv_file.close()

        #try going to next page
        try:
            next_button = response.selector.xpath('//a[@class = "Next"]/@href').extract()
            if(len(next_button) >= 1):
                print("going to next page")
                url = response.urljoin(next_button[0])
                time.sleep(2)
                yield scrapy.Request(url=url, callback=self.parse_page)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")