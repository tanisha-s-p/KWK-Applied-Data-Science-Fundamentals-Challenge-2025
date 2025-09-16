import scrapy


class MsScraperSpider(scrapy.Spider):
    name = "ms_scraper"
    allowed_domains = ["www.marksandspencer.com"]
    start_urls = ["https://www.marksandspencer.com/l/women/all-new-in"]

    def parse(self, response):
        for link in response.xpath("//a[@class='product-card_cardWrapper__GVSTY']/@href"):
            yield response.follow(link, self.product_parse)


    def product_parse(self, response):
        categories = response.xpath("//li[@class='breadcrumb_listItem__oW_Gf']//a/text()").getall()

        yield {
            "product_name" : response.xpath("//h1[@class='media-0_headingSm__aysOm']/text()").get(),
            "parent_category" : categories[2] if len(categories) > 2 else "",
            "child_category": categories[3] if len(categories) > 3 else "",
            "price" : response.xpath("//p[@class='media-0_headingSm__aysOm']/text()").get(),
            "materials" : response.xpath("//p[contains(text(), 'Composition')]/following-sibling::p[1]/text()").get()

        }