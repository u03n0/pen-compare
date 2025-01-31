import scrapy


class KawecoSpider(scrapy.Spider):
    name = "kaweco"
    allowed_domains = ["www.kaweco-pen.com"]
    start_urls = ["https://www.kaweco-pen.com/en/pens/fountain-pens/?p=1"]

    def parse(self, response):

        links = response.css("a.product--title::attr(href)").extract()

        for link in links:
            yield scrapy.Request(link, callback=self.parse_product)


        next_page_url = self.get_next_page_url(response)
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):

        name = response.css("h1.product--title::text").extract()
        price = response.css("span.price--content::text").extract()
        sizes = response.css("div.variant--group label::text").extract()
        detail_keys = response.css("table.product--properties-table td.product--properties-label::text").extract()
        detail_values = response.css("table.product--properties-table td.product--properties-value::text").extract()
        details = dict(zip(detail_keys, detail_values))

        yield {
                "name": name,
                "price": price,
                "sizes": sizes,
                "details": details
                }

    def get_next_page_url(self, response):

        current_url = response.url
        current_page = self.extract_page_number(current_url)
        next_page_number = current_page + 1
        next_page_url = current_url.replace(f"?p={current_page}", f"?p={next_page_number}")
        return None if self.has_previous_page(response) else next_page_url

    def extract_page_number(self, url):

        return int(url.split("?p=")[-1])

    def has_previous_page(self, response):

        previous_button = response.xpath('//a[contains(text(), "Load previous articles")]')

        return bool(previous_button)
