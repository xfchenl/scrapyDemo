import scrapy
from Douban.items import DoubanItem

import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")

class Movie250Spider(scrapy.Spider):
  """docstring for Movie250Spider"""
  name = 'movie250'
  allowed_domains = ["douban.com"]
  start_urls = [
    "http://movie.douban.com/top250/"
  ]

  def parse(self, response):
    for info in response.xpath('//div[@class="item"]'):
      item = DoubanItem()
      item['rank'] = info.xpath('div[@class="pic"]/em/text()').extract()
      item['title'] = info.xpath('div[@class="pic"]/a/img/@alt').extract()
      item['link'] = info.xpath('div[@class="pic"]/a/@href').extract()
      item['star'] = info.xpath('div[@class="info"]/div[@class="bd"]/p[1]/text()').extract()[0].strip()
      item['rate'] = info.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span/text()').extract()
      item['quote'] = info.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
 
      yield item

    
    next_page = response.xpath('//span[@class="next"]/a/@href')
    if next_page:
      url = response.urljoin(next_page[0].extract())
      yield scrapy.Request(url, self.parse)
 