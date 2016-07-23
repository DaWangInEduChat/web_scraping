import scrapy
from myproject.items import MyprojectItem
from myproject.stripper import MLStripper
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = "new_my_spider"
    allowed_domains = ["engineering.nyu.edu"]
    start_urls = [
        #"http://www.nyu.edu/footer/site-map.html"
        "http://engineering.nyu.edu/"
    ]

    rules = (
        Rule(LinkExtractor(
                
                deny=(
                    '.*/events/.*',
                    '.*biomolecular/.*',
                    '.*/multimedia/.*',
                    '.*/preview_course_nopop.*',
                    '.*/download/.*',
                    '.*/calendar/.*',
                    '.*/themasses/books/.*',
                    '.*/svn/.*',
                    '.*/pipermail/.*',
                    '.*nypg\.bio\.nyu\.edu/sequences/.*',
                    '.*dlib\.nyu\.edu/undercover/.*', 
                    '.*/sca\.calendar.*', 
                    '.*math\.nyu\.edu/student_resources/wwiki/index\.php.*',
                    '.*dlib\.nyu\.edu/awdl/.*',
                    '.*skirball\.med\.nyu\.edu/facilities/.*',
                    '.*gallatin\.nyu\.edu/academics/courses.*',
                    '.*www\.stern\.nyu\.edu/networks/.*', 
                ), 
                deny_domains=(
                    'ifp.nyu.edu', 
                    'nyuad.nyu.edu', 
                    'wikis.nyu.edu', 
                    'nyuscholars.nyu.edu', 
                    'geo.nyu.edu',
                    'medhum.med.nyu.edu'), 
            ), callback='parse_website', follow=True, 
            ),
    )

    def parse_website(self, response):
        for temp in response.xpath('//p').extract():
            s = MLStripper()
            s.feed(temp)
            data = s.get_data().strip(' \t\n\r')
            if (data != ""):
                yield MyprojectItem(text=data, current_url=response.url)
        # for url in response.xpath('//a/@href').extract():
        #     yield scrapy.Request(response.urljoin(url), callback=self.parse_website)