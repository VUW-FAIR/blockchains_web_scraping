import csv
import json
import os
import scrapy
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class bitcoin_garden_scraper(scrapy.Spider):
    name = "btcgarden"
    forum_folder_name = "btcgarden"
    start_urls = ['http://bitcoingarden.org/forum/']


    def parse(self, response):
        print("in main parse")

        if not os.path.exists(self.forum_folder_name):
            os.makedirs(self.forum_folder_name)

        category_links = response.selector.xpath('//a[@class="subject"]//@href').extract()
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
        forum_post_links = []
        print("c")
        print(response.url)
        links1 = response.xpath('//td[@class="subject windowbg2"]//span//@href').extract()
        links2 = response.xpath('//td[@class="subject global2"]//span//@href').extract()
        for link in links1:
            forum_post_links.append(link)
        for link in links2:
            forum_post_links.append(link)
        print(len(forum_post_links))
        for link in forum_post_links:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_page)

        try:
            current_page = int(response.selector.xpath('//div[@class="pagelinks floatleft"]//strong//text()').extract()[0].replace("[", "").replace("]", ""))
            print("current page!!!!")
            print(current_page)
            next_button = response.selector.xpath('//a[text()="' + str(current_page + 1) + '"]//@href').extract()
            print(next_button)
            if(len(next_button) >= 1):
                print("going to next category page!")
                # url = response.urljoin(next_button[1])
                time.sleep(1)
                yield scrapy.Request(url=next_button[0], callback=self.parse_category)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")


    '''
    Parsing the individual pages including all posts and relevant information on the page
    '''
    def parse_page(self, response):
        print("in parse page")
        soup = BeautifulSoup(response.body, 'html.parser')

        title = response.selector.xpath('(//*[@id="forumposts"]/div/h3)/text()').extract()[2]
        print("title:")
        print(title)

        user = response.selector.xpath('//a[contains(@title, "View the profile of")]//text()').extract()
        print(user)

        post = soup.find_all('div', attrs={'class': 'post'})


        edited_time = []

        for i in range(0, len(user)):
            t = response.selector.xpath('(//div[contains(@class, "keyinfo")]//div[@class="smalltext"])[' + str(i+1) + ']//text()').extract()[2]
            edited_time.append(t)
        print("time:")
        print(edited_time)


        page_to_csv(self, title, user, post, edited_time)

        try:
            current_page = int(response.selector.xpath('//div[@class="pagelinks floatleft"]//strong//text()').extract()[0].replace("[", "").replace("]", ""))
            next_button = response.selector.xpath('//a[text()="' + str(current_page + 1) + '"]//@href').extract()
            if(len(next_button) >= 1):
                print("going to next page in post!")
                url = response.urljoin(next_button[0])
                time.sleep(1)
                yield scrapy.Request(url=url, callback=self.parse_category)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")
            time.sleep(1)

'''
Put information into CSV file
'''
def page_to_csv(self, title, user, post, edited_time):

    csv_file = open(".\\" + self.forum_folder_name + "\\" + title.strip().replace("/", "").replace("\\", "").replace("|", "").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace(":", "").replace("-", "_").replace(".", "") + ".csv", "a", encoding="utf-8")

    print(len(user))
    print(len(post))
    print(len(edited_time))
    if(len(user) == len(post) == len(edited_time)):
        writer = csv.writer(csv_file, delimiter=",")
        for i in range(0, len(user)):
            writer.writerow((title.strip(), user[i].strip(), post[i].text.strip(), edited_time[i].strip()))
    else:
        print("different amount of users to posts/timestamps")

    csv_file.close()



