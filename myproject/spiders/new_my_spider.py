import scrapy
from myproject.items import MyprojectItem
from myproject.stripper import MLStripper
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = "new_my_spider"
    allowed_domains = ["nyu.edu"]
    start_urls = [
        "http://www.nyu.edu/footer/site-map.html"
    ]

    rules = (
        Rule(LinkExtractor(deny_domains=(
            'ifp.nyu.edu/', 
            'shanghai.nyu.edu/calendar/', 
            'ipk.nyu.edu/calendar/', 
            'cbi.nyu.edu/svn/',
            'cbi.nyu.edu/pipermail/', 
            'dlib.nyu.edu/themasses/books/', 
            'shanghai.nyu.edu', 
            'shanghai.nyu.edu/',
            'nyuad.nyu.edu',  
            'nyuad.nyu.edu/', 
            'nypg.bio.nyu.edu/sequences/', )), callback='parse_website', 
            ),
    )

    def parse_sitemap(self, response):
        # for sel in response.xpath('//div[@class="link"]'):
        #     item = MyprojectItem()
        #     item['text'] = sel.xpath('a/text()').extract()
        #     item['link'] = sel.xpath('a/@href').extract()
        #     yield item

        # for title_text in response.xpath('//div[@class="link"]/a/text()').extract():
        #     yield MyprojectItem(text=title_text)

        for url in response.xpath('//div[@class="link"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_website)

    def parse_website(self, response):
        for temp in response.xpath('//p').extract():
            s = MLStripper()
            s.feed(temp)
            data = s.get_data().strip(' \t\n\r')
            if (data != ""):
                yield MyprojectItem(text=data, current_url=response.url)
        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_website)