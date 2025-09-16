import scrapy


class HollisterScraperSpider(scrapy.Spider):
    name = "hollister_scraper"
    allowed_domains = ["www.hollisterco.com"]
    start_urls = ["https://www.hollisterco.com/shop/us/womens-new-arrivals"]
    base_url = "https://www.hollisterco.com"


    def parse(self, response):
        for link in response.xpath("//div[@class='catalog-productCard-module__product-details-wrapper']/a/@href"):
            yield response.follow(link, self.product_parse)

    def product_parse(self, response):
        yield {
            "product_name" : response.xpath("//h1[@data-testid='main-product-name']/text()").get(),
            "parent_category" : response.xpath("//nav[@aria-label='Breadcrumb']//a/text()").getall()[1],
            "child_category": response.xpath("//nav[@aria-label='Breadcrumb']//a/text()").getall()[2],
            "price" : response.xpath("//span[@class='product-price-text product-price-font-size']/text()").get(),
            "materials" : response.xpath("//h4[@class='h4 fabric-care-mfe__label']/text()").get()


        }

