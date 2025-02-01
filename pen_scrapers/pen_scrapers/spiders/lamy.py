import scrapy


class LamySpider(scrapy.Spider):
    name = "lamy"
    allowed_domains = ["www.lamy.com"]
    start_urls = ["https://www.lamy.com/fr-de/writing-tools/fountain-pens"]

    def parse(self, response):
        pass
