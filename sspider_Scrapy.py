import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field


class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['testaspnet.vulnweb.com']
    start_urls = ['http://testaspnet.vulnweb.com']


    

    def parse_item(self, response):
        self.log('%s' % response.url)

        hxs = HtmlXPathSelector(response)
        text_input=hxs.select("//input[(@id or @name) and (@type = 'text' )]").extract()
        pass_input=hxs.select("//input[(@id or @name) and (@type = 'password')]").extract()     
        file_input=hxs.select("//input[(@id or @name) and (@type = 'file')]").extract()

        print (text_input) 
