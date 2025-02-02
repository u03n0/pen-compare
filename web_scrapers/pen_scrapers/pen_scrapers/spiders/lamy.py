import scrapy
from pen_scrapers.items import FountainPenItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
import time


class LamySpider(scrapy.Spider):
    name = "lamy"
    allowed_domains = ["www.lamy.com"]
    start_urls = ["https://www.lamy.com/fr-de/writing-tools/fountain-pens"]

    def parse(self, response):
        # Scraping initial content
        stem = "/fr-de"
        base = response.url.split(stem)[0]

        links = response.css("div.select-none a::attr(href)").extract()
        for link in links:
            url = base + link
            yield SeleniumRequest(url, callback=self.parse_product)

    def parse_product(self, response):
        # Initial product parsing logic
        keys = ["size", "weight"]
        pen = FountainPenItem()
        pen['brand'] = 'lamy'
        pen['name'] = response.css("h1::text").extract()
        pen['price'] = response.xpath("//span[@class='h2 tablet:h1']/text()").extract()[0]
        raw_details = response.xpath("//span[@class='text-black text-copy font-normal']/text()").extract()
        reduced_details = [item for item in raw_details if ':' not in item]
        for idx, item in enumerate(reduced_details):
            for key in keys:
                if key in item:
                    pen[key] = reduced_details[idx + 1]

        pen['nib'] = response.xpath("//ul[contains(@aria-label, 'Nib Grade')]/li/a/@aria-labelledby").extract()
        pen['color_names'] = response.xpath("//ul[contains(@aria-label, 'color') or contains(@aria-label, 'Color')]//li/a/@aria-labelledby").extract()
        pen['description'] = response.xpath("//div[@class='text-black text-copy font-normal [&>p]:mb-[1em] last:[&>p]:mb-0']//p/text()").extract()

        # Yield the item
        yield pen

        # Now click "Load More" if button exists and scrape the additional items
        driver = response.meta['driver']  # Get the Selenium WebDriver from response

        # Find and click the "Load More" button (based on class name or other attributes)
        try:
            load_more_button = driver.find_element(By.CLASS_NAME, "container.btn-x-padding.text-buttons.text-center.whitespace-break-spaces.px-2.desktop:px-6.py-4.desktop:py-5.border.motion-reduce:transition-none.transition-all.inline-flex.justify-center.items-center.gap-2.border.border-black.text-black.bg-white.hover:bg-black.hover:text-white.w-auto.cursor-pointer")
            load_more_button.click()
            time.sleep(2)  # Wait for content to load, you may need to adjust this

            # After the page has updated, get the new content and pass it to `parse_product`
            updated_response = scrapy.http.HtmlResponse(url=response.url, body=driver.page_source, encoding='utf-8')
            yield from self.parse_product(updated_response)

        except Exception as e:
            self.log(f"Error or no 'Load More' button: {str(e)}")

