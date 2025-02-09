import scrapy
from pen_scrapers.items import FountainPenItem

class SailorSpider(scrapy.Spider):

    name = "sailor"
    allowed_domains = ["en.sailor.co.jp"]
    start_urls = ["https://en.sailor.co.jp/category_product/fountain-pen/?taxonomy-detail=fountain-pen-all"]
    

    def parse(self, response):

        links = response.xpath("//a[@class='Common__productLink']/@href").extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_product)
        
        next_page = response.css("a.Common__paginationNext::attr(href)").get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_product(self, response):
        """ Get more information from each product """
        pen = FountainPenItem()
        pen['brand'] = 'sailor'
        pen['name'] = response.css("h2.ProductEyecatch__productNameMain::text").get()
        pen['colors'] = response.css("label.ProductEyecatch__colorLabel::attr(style)").re(r"background-color:\s*(#[0-9a-fA-F]{6})")
        pen['color_names'] = response.css("label.ProductEyecatch__colorLabel::attr(data-color)").extract()
        pen['description'] = response.css("div.Common__inputArticle::text").extract()
        detail_names = response.css("div.ProductInfoTab__tabTarget dt::text").extract()
        
        details = {} 
        for _name in detail_names:
            detail_value = response.css(f"dt.ProductInfoTab__itemHead:contains('{_name}') + dd::text").getall()
            details[_name] = [val.strip() for val in detail_value]
        pen['details'] = details
        yield pen
