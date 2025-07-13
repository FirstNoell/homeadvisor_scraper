import scrapy
import re
from scrapy.http import Response


class CostSpider(scrapy.Spider):
    name = "cost_spider"
    allowed_domains = ["homeadvisor.com"]
    start_urls = ["https://www.homeadvisor.com/cost/"]

    def parse(self, response: Response, **kwargs):
        # Collect links to all project pages
        links = response.xpath('//a[contains(@href, "/cost/") and contains(@href, "-")]/@href').getall()
        unique_links = list(set(links))  # Remove duplicates

        for link in unique_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(url=full_url, callback=self.parse_project)

    def parse_project(self, response: Response):
        # Extract all required fields for a single project page
        highlights = response.xpath(
            '//div[contains(@class, "CalloutBlock_calloutText")]//li/p/text()'
        ).getall()

        cost_range = response.xpath(
            '//div[contains(@class,"Hero_normalRange")]/span/text()'
        ).get(default='').strip()

        low_cost = high_cost = ''
        if " - " in cost_range:
            low_cost, high_cost = [c.strip() for c in cost_range.split(" - ")]

        average_cost = ''
        if highlights:
            match = re.search(r'\$\d{1,3}(?:,\d{3})*', highlights[0])
            if match:
                average_cost = match.group(0)

        cost_factors = response.xpath(
            '//h2[contains(text(), "Cost Factors")]/following-sibling::p/text()'
        ).getall()

        yield {
            "website_url": response.url,
            "title_of_project": response.xpath(
                '//h1[contains(@class, "Hero_headline")]/text()'
            ).get(default='').strip(),
            "normal_range_low_cost": low_cost,
            "average_cost": average_cost,
            "normal_range_high_cost": high_cost,
            "highlights": '; '.join([h.strip() for h in highlights]),
            "cost_factors": '\n'.join([p.strip() for p in cost_factors if p.strip()])
        }
