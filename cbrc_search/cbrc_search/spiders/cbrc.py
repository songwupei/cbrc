# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest
from ..items import CbrcSearchItem

class CbrcSpider(CrawlSpider):
    name = 'cbrc'
    allowed_domains = ['www.cbrc.gov.cn']
    start_urls = ['http://www.cbrc.gov.cn/']

    rules = (
        Rule(LinkExtractor(deny=r'.*/chinese/.*', allow=r'/govView_.*\.html')),
        #Rule(LinkExtractor(restrict_xpaths=r'//div[@id="sousuo"]/div[4]/a[3]')),
        #Rule(LinkExtractor(allow=r'//div[@id="sousuo"]/div[3]/ul/li[d+]/a'), callback="parse_item", follow=True)
        )

    def parse_item(self, response):
        item['wh']=response.xpath('string(/html/body/center/div[1]/table[2]/tbody/tr[2]/td/div/div)').extract()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
