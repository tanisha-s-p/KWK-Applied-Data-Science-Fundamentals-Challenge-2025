import scrapy


class SuperdryScraperSpider(scrapy.Spider):
    name = "superdry_scraper"
    allowed_domains = ["www.superdry.com"]
    start_urls = ["https://www.superdry.com/us/womens/new-in/"]


    def parse(self, response):
        for link in response.xpath("//div[@class='tile-name']/a/@href"):
            yield response.follow(link, self.product_parse)



    def product_parse(self, response):
        yield {
            "product_name" : response.xpath("//h1[@class='product-name']/text()").get(),
            "parent_category" : response.xpath("//li[@class='breadcrumb-item']//a/text()").getall()[2].strip(),
            "child_category": "",
            "price" : response.xpath("//span[@class='value' and @content]/@content").get(),
            "materials" : response.xpath("normalize-space(//div[contains(@class, 'composition-care')]//div[@class='col-9']/text())").get()


        }

