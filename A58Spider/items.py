# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class A58SpiderItem(scrapy.Item):
    url = scrapy.Field()
    area = scrapy.Field()
    community = scrapy.Field()
    date = scrapy.Field()
    metro = scrapy.Field()
    subway_station = scrapy.Field()
    distance = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
