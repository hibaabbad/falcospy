# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FalcospyItem(scrapy.Item):
            images= scrapy.Field()
            url= scrapy.Field()
            title= scrapy.Field()
            brand= scrapy.Field()
            price= scrapy.Field()
            rate= scrapy.Field()
            description= scrapy.Field()
            cpu= scrapy.Field()
            ram= scrapy.Field()
            storage = scrapy.Field()
            screen = scrapy.Field()
            integrated_gpu = scrapy.Field()
            dedicated_gpu = scrapy.Field()
            os = scrapy.Field()
            battery = scrapy.Field()
            state = scrapy.Field()
            date = scrapy.Field()
            source = scrapy.Field()