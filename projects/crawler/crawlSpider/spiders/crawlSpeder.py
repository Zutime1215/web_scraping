from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "spiderBot"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    rules = (
        Rule(LinkExtractor(allow="catalogue/category")),
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback="parse_item")
    )

    def parse_item(self, response):
        yield {
            "title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "description": response.css(".product_page p::text")[10].get(),
            "url": response.url
        }