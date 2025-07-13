from scrapy_selenium import SeleniumRequest
import scrapy


class InproSpider(scrapy.Spider):
    name = "inpro"
    allowed_domains = ["inprocorp.com"]
    start_urls = ["https://www.inprocorp.com/markets/"]

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse
        )

    def parse(self, response):
        markets = response.xpath('//div[@class="text-grid__list"]/a[@class="text-grid__item"]')
        for market in markets:
            title = market.xpath('.//p[@class="text-grid__title"]/text()').get(default='').strip()
            description = market.xpath('.//div[@class="text-grid__content"]/p[2]//text()').get(default='').strip()
            relative_url = market.xpath('./@href').get()
            full_url = response.urljoin(relative_url)
            icon_url = response.urljoin(market.xpath('.//img[@class="text-grid__icon"]/@src').get(default=''))

            # Pass collected metadata to the next request
            yield SeleniumRequest(
                url=full_url,
                callback=self.parse_inner_page,
                cb_kwargs={
                    'title': title,
                    'description': description,
                    'url': full_url,
                    'icon_url': icon_url
                }
            )

    def parse_inner_page(self, response, title, description, url, icon_url):
        # Extract visible text from the page body
        content_blocks = response.xpath('//main//text()').getall()
        content = ' '.join([text.strip() for text in content_blocks if text.strip()])

        yield {
            "title": title,
            "description": description,
            "url": url,
            "icon_url": icon_url,
            "inner_page_content": content
        }
