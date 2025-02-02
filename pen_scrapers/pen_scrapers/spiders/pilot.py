import scrapy


class PilotSpider(scrapy.Spider):
    name = "pilot"
    allowed_domains = ["www.pilotpen.eu"]
    start_urls = ["https://www.pilotpen.eu/our-universes/fine-writing/"]

    def parse(self, response):
        links = response.xpath("//div[@id='fountains-pens']//a/@href").extract() 
        for link in links:
            yield scrapy.Request(link, callback=self.parse_product)


    def parse_product(self, response):
        pass
