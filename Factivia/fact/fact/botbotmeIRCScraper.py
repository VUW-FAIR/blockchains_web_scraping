# -*- coding: utf-8 -*-
import json
import scrapy


class QuotesInfiniteScrollSpider(scrapy.Spider):
    name = "fact2"

    page = 1
    start_urls = 'https://botbot.me/freenode/bitcoin-wizards/2017-12-06/?page=' + str(page)

    def parse(self, response):

        data = json.loads(response.text)

        print(data)

        #
        # for quote in data['quotes']:
        #     yield {
        #         'author_name': quote['author']['name'],
        #         'text': quote['text'],
        #         'tags': quote['tags'],
        #     }
        # if data['has_next']:
        #     next_page = data['page'] + 1
        #     yield scrapy.Request(url=self.api_url.format(next_page), callback=self.parse)