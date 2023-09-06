# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FalcospyItem(scrapy.Item):
   url = scrapy.Field()
   title = scrapy.Field()
   category = scrapy.Field()
   brand = scrapy.Field()
   price = scrapy.Field()
   old_price = scrapy.Field()
   