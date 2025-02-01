# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def serialer_price(value):
    return 




class FountainPenItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    nib = scrapy.Field()
    color_names = scrapy.Field()
    colors = scrapy.Field()
    size = scrapy.Field()
    weight = scrapy.Field()
    material = scrapy.Field()        
    refill_type = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
