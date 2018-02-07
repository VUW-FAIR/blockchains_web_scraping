import csv
import json
import os
import scrapy
import time
from bs4 import BeautifulSoup

'''
NOTE: 
Seems to work only for a little bit then stops, most likely because they block the ip.
'''

class cryptoinfo_forum_scraper(scrapy.Spider):
    name = "bitco"
    forum_folder_name = "bitco"
    start_urls = ['https://bitco.in/forum/']

    def parse(self, response):
        print("in main parse")

        if not os.path.exists(self.forum_folder_name):
            os.makedirs(self.forum_folder_name)

        category_links = response.selector.xpath('(//h3[contains(@class, "nodeTitle")])//@href').extract()
        print(category_links)

        for link in category_links:
            url = response.urljoin(link)
            yield scrapy.Request(url=url, callback=self.parse_category)


    '''
    Parsing category which contains multiple pages of information
    '''

    def parse_category(self, response):

        links = response.xpath('(//h3[contains(@class, "title")])//@href').extract()

        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url=url, callback=self.parse_page)

        try:
            next_button = response.selector.xpath('//a[text()="Next >"]//@href').extract()
            if (len(next_button) >= 1):
                print("going to next category page!")
                url = response.urljoin(next_button[0])
                time.sleep(60)
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

        title = response.selector.xpath('//div[@class="titleBar"]//h1//text()').extract()
        usernames = response.selector.xpath('//div[@class="uix_usernameWrapper"]//a[@class="username"]//text()').extract()
            #soup.find_all('div', attrs={'class': 'extraUserInfo'})

        post_text = soup.find_all('blockquote', attrs={'class': 'messageText SelectQuoteContainer ugc baseHtml'})
        #'(//blockquote[@class="messageText SelectQuoteContainer ugc baseHtml"])[1]//text()'
        post_times = response.selector.xpath('//span[@class="item muted"]//abbr[@class="DateTime"]//@title|//span[@class="item muted"]//span[@class="DateTime"]//@title').extract()

        print(post_times)

        print('usernames ' + str(len(usernames)))
        print('times ' + str(len(post_times)))
        print('messages ' + str(len(post_times)))

        # Opening CSV file and removing symbols that system may not like
        csv_file = open(".\\" + self.forum_folder_name + "\\" + title[0].replace("/", "").replace("\\", "").replace("|",
                                                                                                                    "").replace(
            "*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace(":", "").replace("-",
                                                                                                                  "_").replace(
            ".", "") + ".csv", "a", encoding="utf-8")

        writer = csv.writer(csv_file, delimiter=",")

        if (len(usernames) == len(post_times) == len(post_text)):
            # Writing to the csv file
            for i in range(0, len(usernames)):
                print(usernames[i].strip())
                print(post_times[i].strip())
                print(post_text[i].text.strip())
                writer.writerow([(title[0].strip()), (usernames[i].strip()), str(post_times[i].strip()),
                                 (post_text[i].text.strip())])
        else:
            print("number of usernames doesn't match up messages")

        csv_file.close()

        # try going to next page
        try:
            next_button = response.selector.xpath('//a[text()="Next >"]//@href').extract()
            if (len(next_button) >= 1):
                print("going to next page")
                url = response.urljoin(next_button[0])
                time.sleep(5)
                yield scrapy.Request(url=url, callback=self.parse_page)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")