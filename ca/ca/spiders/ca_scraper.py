import scrapy
import re
import json


class CaScraperSpider(scrapy.Spider):
    name = "ca_scraper"
    allowed_domains = ["www.c-and-a.com"]
    start_urls = ["https://www.c-and-a.com/eu/en/shop/women-new-in-clothing"]
    base_url = "https://www.c-and-a.com"


    def parse(self, response):
        for link in response.xpath("//div[@class= 'relative']/a/@href"):
            yield response.follow(link, self.product_parse)

    def product_parse(self, response):

        #function needed bc material  composition is within "window.__REACT_QUERY_STATE__ ="

        script_text = response.xpath('//script[contains(text(), "__REACT_QUERY_STATE__")]/text()').get()

        if not script_text:
            self.logger.warning("Could not find __REACT_QUERY_STATE__ script")
            return

        match = re.search(r'window\.__REACT_QUERY_STATE__\s*=\s*"({.*})";',script_text,re.DOTALL)

        if not match:
            self.logger.warning("Could not regex match __REACT_QUERY_STATE__")
            return

        raw_json = match.group(1)
        cleaned = raw_json.encode("utf-8").decode("unicode_escape")

        try:
            data = json.loads(cleaned)
        except Exception as e:
            self.logger.error(f"JSON parse error: {e}")
            return

        outer_materials = []

        if not outer_materials:
            def find_outer_materials(obj):
                found_materials = []
                if isinstance(obj, dict):
                    if "materialComposition" in obj:
                        for comp in obj["materialComposition"]:
                            if (comp.get("name") == "Outer material:" and "materials" in comp):
                                found_materials.extend(comp["materials"])
                    for key, value in obj.items():
                        found_materials.extend(find_outer_materials(value))
                elif isinstance(obj, list):
                    for item in obj:
                        found_materials.extend(find_outer_materials(item))
                return found_materials

            outer_materials = find_outer_materials(data)

        yield {
            "product_name" : response.xpath("//h1[@data-qa='ProductName']/text()").get(),
            "parent_category": response.xpath("//li[@class='sc-btdEvL esEEgE']/a/span/text()").getall()[2],
            "child_category": response.xpath("//li[@class='sc-btdEvL esEEgE']/a/span/text()").getall()[3],
            "price": response.xpath("//div[@class='sc-fkSzgi dxljsZ sc-cVeEvA UfGth']/text()").get(),
            "materials": outer_materials
        }

