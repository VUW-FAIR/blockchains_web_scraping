import csv
import json
import os
import scrapy
import time
from bs4 import BeautifulSoup

class acc_forum_scraper(scrapy.Spider):
    name = "acc"
    forum_folder_name = "altcoincommunity"
    start_urls = ['http://altcoincommunity.net/']
    #TODOOOO

    def parse(self, response):
        print("in main parse")

        if not os.path.exists(self.forum_folder_name):
            os.makedirs(self.forum_folder_name)

        category_links = ['http://altcoincommunity.net/forum-4.html', 'http://altcoincommunity.net/forum-7.html', 'http://altcoincommunity.net/forum-11.html', 'http://altcoincommunity.net/forum-15.html', 'http://altcoincommunity.net/forum-16.html',
                          'http://altcoincommunity.net/forum-17.html', 'http://altcoincommunity.net/forum-20.html', 'http://altcoincommunity.net/forum-21.html', 'http://altcoincommunity.net/forum-23.html',
                          'http://altcoincommunity.net/forum-24.html', 'http://altcoincommunity.net/forum-26.html', 'http://altcoincommunity.net/forum-27.html', 'http://altcoincommunity.net/forum-28.html', 'http://altcoincommunity.net/forum-30.html',
                          'http://altcoincommunity.net/forum-32.html', 'http://altcoincommunity.net/forum-33.html', 'http://altcoincommunity.net/forum-38.html', 'http://altcoincommunity.net/forum-39.html', 'http://altcoincommunity.net/forum-40.html',
                          'http://altcoincommunity.net/forum-41.html', 'http://altcoincommunity.net/forum-5.html', 'http://altcoincommunity.net/forum-6.html', 'http://altcoincommunity.net/forum-8.html', 'http://altcoincommunity.net/forum-9.html',
                          'http://altcoincommunity.net/forum-12.html', 'http://altcoincommunity.net/forum-13.html', 'http://altcoincommunity.net/forum-18.html', 'http://altcoincommunity.net/forum-22.html', 'http://altcoincommunity.net/forum-29.html',
                          'http://altcoincommunity.net/forum-31.html', 'http://altcoincommunity.net/forum-34.html']
        print(category_links)

        for link in category_links:
            url = response.urljoin(link)
            yield scrapy.Request(url=url, callback=self.parse_category)


    '''
    Parsing category which contains multiple pages of information
    '''

    def parse_category(self, response):

        links = response.xpath('//span[@class=" subject_old"]//@href').extract()

        for link in links:
            yield  scrapy.Request(url= link, callback=self.parse_page)

        try:
            next_button = response.selector.xpath('//a[@title="Next page"]//@href').extract()
            if (len(next_button) >= 1):
                print("going to next category page!")
                url = response.urljoin(next_button[0])
                time.sleep(1)
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

        title = response.selector.xpath('//div[@class="thead"]//strong//text()').extract()

        #TODO usernames downwards
        usernames = []
        number_of_usernames = len(response.selector.xpath('//h3[contains(@class, "ipsType_sectionHead cAuthorPane_author ipsType_blendLinks ipsType_break")]').extract())
        print(str(number_of_usernames))

        for i in range(0, number_of_usernames):
            link_str = '(//h3[contains(@class, "ipsType_sectionHead cAuthorPane_author ipsType_blendLinks ipsType_break")])[' + str(i+1) + ']//text()'
            forum_post_links = response.xpath(link_str).extract()
            print(forum_post_links[2])
            usernames.append(forum_post_links[2])

        post_times = response.selector.xpath('//div[contains(@class, "ipsComment_meta ipsType_light")]//@datetime').extract()

        post_text = soup.find_all('div', attrs={'class': 'cPost_contentWrap ipsPad'})

        for i in range(0, number_of_usernames):
            link_str = '(//div[contains(@class, "cPost_contentWrap ipsPad")])[' + str(i + 1) + ']//text()'
            forum_post_text = response.xpath(link_str).extract()
            for t in forum_post_text:
                print(t)

        print('usernames ' + str(len(usernames)))
        print('times ' + str(len(post_times)))
        print('messages ' + str(len(post_text)))


        print("TITLELLLLLLLLLLLLLLLLLLLLLLLLL")
        for t in title:
            print(t)

        # Opening CSV file and removing symbols that system may not like
        csv_file = open(".\\" + self.forum_folder_name + "\\" + title[1].replace("/", "").replace("\\", "").replace("|", "").replace(
"*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace(":", "").replace("-", "_").replace(".", "") + ".csv", "a", encoding="utf-8")  # or append?

        writer = csv.writer(csv_file, delimiter=",")

        if (len(usernames) == len(post_times) == len(post_text)):
            # Writing to the csv file
            for i in range(0, len(usernames)):
                print(usernames[i].strip())
                print(post_times[i])
                print(post_text[i].text.strip())
                writer.writerow([(title[1].strip()), (usernames[i].strip()), post_times[i],
                                 (post_text[i].text.strip())])
        else:
            print("number of usernames doesn't match up messages")

        csv_file.close()

        # try going to next page
        try:
            next_button = response.selector.xpath('//a[@title="Next page"]//@href').extract()
            if (len(next_button) >= 1):
                print("going to next page")
                url = response.urljoin(next_button[0])
                time.sleep(2)
                yield scrapy.Request(url=url, callback=self.parse_page)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")