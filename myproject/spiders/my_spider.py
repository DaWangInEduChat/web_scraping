import scrapy
from myproject.items import MyprojectItem
from myproject.stripper import MLStripper

class MySpider(scrapy.spiders.Spider):
    name = "my_spider"
    allowed_domains = ["nyu.edu"]
    start_urls = [
        "http://www.nyu.edu/footer/site-map.html"
    ]

    def parse(self, response):
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
                yield MyprojectItem(text=data)
        for div in response.xpath('//p').extract():
            s = MLStripper()
            s.feed(div)
            data = s.get_data().strip(' \t\n\r')
            if (data != ""):
                yield MyprojectItem(text=data)