import scrapy


class MexxScraperSpider(scrapy.Spider):
    name = "mexx_scraper"
    allowed_domains = ["www.mexx.com"]
    start_urls = ["https://www.mexx.com/en/women/clothing/new?product_list_limit=48"]
    base_url = "https://www.mexx.com"

    def parse(self, response):
        for link in response.xpath("//a[@class='product-item-link']/@href"):
            yield response.follow(link, self.product_parse)

    def product_parse(self, response):
        yield {
            "product_name" : response.xpath("//span[@class='base' and @itemprop='name']/text()").get(),
            "parent_category" : response.xpath("//span[@itemprop='name']/text()").getall()[4],
            "child_category": "",
            "price" : response.xpath("//span[@class='price']/text()").get(),
            "materials" : response.xpath("(//span[@class='data']/text())[last()]").get()}



