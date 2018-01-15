# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Article(Item):
    title = Field()
    desc = Field()

class Commit(Item):
    title = Field()
    desc = Field()
    time = Field()


class Release(Item):
    title = Field()
    ownership = Field()
    desc = Field()
    time = Field()

class Contributor(Item):
    name = Field()
    info = Field()
