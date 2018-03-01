import scrapy
import sys


service_name = input("Input Industry: ")
city = input("Input The City: ")

class Item(scrapy.Item):
    business_name = scrapy.Field()
    phone_number = scrapy.Field()
    website = scrapy.Field()


class QuotesSpider(scrapy.Spider):


   
    name = "quotes"

    start_urls = [
        "http://www.yellowbook.com/s/" + service_name + "/" + city 
    ]
    def __init__(self):
        self.seen_business_names = []
        self.seen_websites = []


    def parse(self, response):
        for business in response.css('div.listing-info'):
            item = Item()
            item['business_name'] = business.css('div.info.l h2 a::text').extract()
            item['website'] = business.css('a.s_website::attr(href)').extract()
            for x in item['business_name']:
                #new code here, call to self.seen_business_names
                if (x not in self.seen_business_names):
                    if item['business_name']:
                        if item['website']:
                            item['phone_number'] = business.css('div.phone-number::text').extract_first()
                            yield item
                            self.seen_business_names.append(x)
            

        # next_page = response.css('div.pagination a::attr(href)').extract()
        for href in response.css('ul.page-nav.r li a::attr(href)'):
            yield response.follow(href, self.parse)