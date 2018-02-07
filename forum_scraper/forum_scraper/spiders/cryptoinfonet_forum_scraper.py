import csv
import json
import os
import scrapy
import time
from bs4 import BeautifulSoup

class cryptoinfo_forum_scraper(scrapy.Spider):
    name = "cryptoinfo"
    forum_folder_name = "cryptoinfo"
    start_urls = ['http://www.forum.cryptoinfo.net/']

    def parse(self, response):
        print("in main parse")

        if not os.path.exists(self.forum_folder_name):
            os.makedirs(self.forum_folder_name)

        category_links = response.selector.xpath('//a[@class="forumtitle"]//@href').extract()
        print(category_links)

        for link in category_links:
            url = response.urljoin(link)
            yield scrapy.Request(url=url, callback=self.parse_category)

        try:
            for link in category_links:
                url = response.urljoin(link)
                yield scrapy.Request(url=url, callback=self.parse)
        except:
            print("no other category pages on this page")

    '''
    Parsing category which contains multiple pages of information
    '''

    def parse_category(self, response):

        links = response.xpath('//a[@class="topictitle"]//@href').extract()

        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url=url, callback=self.parse_page)

        try:
            next_button = response.selector.xpath('//a[@rel="next"]//@href').extract()
            if (len(next_button) >= 1):
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
        print("HELLO THERE")
        soup = BeautifulSoup(response.body, 'html.parser')

        title = response.selector.xpath('//h2[@class="topic-title"]//text()').extract()
        usernames = response.selector.xpath('//a[contains(@class, "username")]//text()').extract()

        post_text = []
        for i in range(0, len(usernames)):
            post_str = '(//div[@class="content"])[' + str(i + 1) + ']//text()'
            post = response.selector.xpath(post_str).extract()
            post_text.append(' '.join(post))

        post_times = []
        for i in range(0, len(usernames)):
            time_str = '(//p[@class="author"])[' + str(i + 1) + ']//text()'
            post_time = response.selector.xpath(time_str).extract()
            post_times.append(' '.join(post_time))

        print('usernames ' + str(len(usernames)))
        print('times ' + str(len(post_times)))
        print('messages ' + str(len(post_times)))

        # Opening CSV file and removing symbols that system may not like
        csv_file = open(".\\" + self.forum_folder_name + "\\" + title[0].replace("/", "").replace("\\", "").replace("|",
                                                                                                                    "").replace(
            "*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace(":", "").replace("-",
                                                                                                                  "_").replace(
            ".", "") + ".csv", "a", encoding="utf-8")  # or append?

        writer = csv.writer(csv_file, delimiter=",")

        if (len(usernames) == len(post_times) == len(post_text)):
            # Writing to the csv file
            for i in range(0, len(usernames)):
                print(usernames[i].strip())
                print(post_times[i])
                print(post_text[i].strip())
                writer.writerow([(title[0].strip()), (usernames[i].strip()), post_times[i].strip(),
                                 (post_text[i].strip())])
        else:
            print("number of usernames doesn't match up messages")

        csv_file.close()

        # try going to next page
        try:
            next_button = response.selector.xpath('//a[@rel="next"]//@href').extract()
            if (len(next_button) >= 1):
                print("going to next page")
                url = response.urljoin(next_button[0])
                time.sleep(2)
                yield scrapy.Request(url=url, callback=self.parse_page)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")