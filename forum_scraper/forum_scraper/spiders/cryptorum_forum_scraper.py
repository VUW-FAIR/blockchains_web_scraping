import csv
import json
import os
import scrapy
import time
from bs4 import BeautifulSoup

class cyt_forum_scraper(scrapy.Spider):
    name = "cyt"
    forum_folder_name = "cryptorum"
    start_urls = ['https://cryptorum.com/forums/']


    def parse(self, response):
        print("in main parse")

        if not os.path.exists(self.forum_folder_name):
            os.makedirs(self.forum_folder_name)

        category_links =['https://cryptorum.com/forums/new-users.2/', 'https://cryptorum.com/forums/cryptocurrency.3/',
                         'https://cryptorum.com/forums/economic-speculation.14/', 'https://cryptorum.com/forums/initial-coin-offering-ico.17/',
                         'https://cryptorum.com/forums/mining.4/',
                         'https://cryptorum.com/forums/knowledgebase.13/']
        print(category_links)

        for link in category_links:
            url = response.urljoin(link)
            yield scrapy.Request(url=url, callback=self.parse_category)

    '''
    Parsing category which contains multiple pages of information
    '''

    def parse_category(self, response):
        print("IN cateogry page")
        forum_post_links = response.xpath('//a[@class="PreviewTooltip"]//@href').extract()

        for link in forum_post_links:
            print(link)
            url = response.urljoin(link)
            yield scrapy.Request(url=url, callback=self.parse_page)

        try:
            next_button = response.selector.xpath('//a[text()="Next >"]//@href').extract()
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

        title = response.selector.xpath('//*[@id="content"]/div/div/div[3]/h1').extract()[0].replace("<h1>", "").replace("</h1>", "")

        usernames = response.selector.xpath('//h3[@class="userText"]//a[@class="username"]//@href').extract()

        post_times = response.selector.xpath('//a[@class="datePermalink"]//text()').extract()


        post_text = []
        for i in range(0, len(usernames)):
            link_str = '(//blockquote[@class="messageText SelectQuoteContainer ugc baseHtml"])[' + str(i+1) + ']//text()'
            post_txt_list = response.xpath(link_str).extract()
            post_txt = ' '.join(post_txt_list)
            post_text.append(post_txt)


        print('usernames ' + str(len(usernames)))
        print('times ' + str(len(post_times)))
        print('messages ' + str(len(post_text)))

        # Opening CSV file and removing symbols that system may not like
        csv_file = open(".\\" + self.forum_folder_name + "\\" + title.replace("/", "").replace("\\", "").replace("|",
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
                writer.writerow([(title.strip()), (usernames[i].strip()), post_times[i],
                                 (post_text[i].strip())])
        else:
            print("number of usernames doesn't match up messages")

        csv_file.close()

        # try going to next page
        try:
            next_button = response.selector.xpath('//a[text()="Next >"]//@href').extract()
            if (len(next_button) >= 1):
                print("going to next page")
                url = response.urljoin(next_button[0])
                time.sleep(2)
                yield scrapy.Request(url=url, callback=self.parse_page)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")