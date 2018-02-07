import csv
import json
import os
import scrapy
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class bitcoin_talk_scraper(scrapy.Spider):
    name = "btc"
    forum_folder_name = "bitcoin_talk_forum"
    start_urls = ['https://bitcointalk.org/index.php']

    ''''
    This web scraper can be used to web scrape all posts from the bitcoin talk forum at https://bitcointalk.org/index.php.
    As the CSV writer appends to the CSV files in the folder, remember to clear the folder each time you run it
    to avoid duplicate text in the CSV.
    '''
    def parse(self, response):
        print("in main parse")

        if not os.path.exists(self.forum_folder_name):
            os.makedirs(self.forum_folder_name)


        boards = ['https://bitcointalk.org/index.php?board=1.0',
                  'https://bitcointalk.org/index.php?board=6.0',
                  'https://bitcointalk.org/index.php?board=14.0'
                  'https://bitcointalk.org/index.php?board=4.0',
                  'https://bitcointalk.org/index.php?board=12.0',
                  'https://bitcointalk.org/index.php?board=7.0',
                  'https://bitcointalk.org/index.php?board=5.0',
                  'https://bitcointalk.org/index.php?board=8.0',
                  'https://bitcointalk.org/index.php?board=67.0',
                  'https://bitcointalk.org/index.php?board=159.0',
                  'https://bitcointalk.org/index.php?board=160.0',
                  'https://bitcointalk.org/index.php?board=161.0',
                  'https://bitcointalk.org/index.php?board=224.0']

        for board in boards:
            yield scrapy.Request(url=board, callback=self.parse_category)

    '''
    Parsing category which contains multiple pages of information
    '''
    def parse_category(self, response):
        forum_post_links = response.xpath('//td[3][@class="windowbg"]/span/a/@href').extract()


        for link in forum_post_links:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_page)

        try:
            next_button = response.selector.xpath('//span[@class = "prevnext"]/a/@href').extract()
            if(len(next_button) >= 1):
                print("going to next category page!")
                url = response.urljoin(next_button[1])
                time.sleep(2)
                yield scrapy.Request(url=url, callback=self.parse_category)
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

        title = response.selector.xpath('//*[@id="bodyarea"]/div[1]/div/b[4]/a/text()').extract()[0]
        print(title)
        user = soup.find_all('td', attrs={'class': 'poster_info'})
        post = soup.find_all('div', attrs={'class': 'post'})
        edited_time = soup.find_all('div', attrs={'class': 'subject'})
        page_to_csv(self, title, user, post, edited_time)

        #try going to next page
        try:
            next_button = response.selector.xpath('//span[@class = "prevnext"]/a/@href').extract()
            if(len(next_button) >= 1):
                print("going to next page")
                # url = response.urljoin(next_button[0])
                url = response.urljoin(next_button[1])
                # time.sleep(2)
                print(next_button[1])
                print(url)
                time.sleep(3)
                yield scrapy.Request(url=url, callback=self.parse_page)
            else:
                print("last page")
        except:
            print("No next page found, you must be on the last page")

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
            writer.writerow((title.strip(), user[i].text.strip(), post[i].text.strip(), edited_time[i].text.strip()))
    else:
        print("different amount of users to posts/timestamps")

    csv_file.close()



