# -*- coding: utf-8 -*-
import scrapy


class Hm2infoSpider(scrapy.Spider):
    name = 'hm2Info'
    #allowed_domains = ['https://www2.hm.com/en_cn/ladies/shop-by-product/jeans.html']
    start_urls = ['https://www2.hm.com/en_cn/ladies/shop-by-product/jeans.html/']

    def parse(self, response):
        #pass
        #print(response.body)
        selector = scrapy.Selector(response)
        # items = selector.xpath('//li[@class="product-item"]')

        title = selector.xpath('//h3[@class="item-heading"]/a/text()').extract()
        price = selector.xpath('//span[@class="price regular"]/text()').extract()
        a = selector.xpath('//a[@class="link"]/@href').extract()
        # for each in items:
            #print(each)
            # for each in items:
            # title = each.xpath('div[@class="title"]/a/text()').extract()[0]
        # author = re.search('<div class="abstract">(.*?)<br', each.extract(), re.S).group(1)
        for each in title:
            print(each)
        for each in price:
            print(each)
        for each in a:
            print("https://www2.hm.com/"+each)


        # print(response.body)
        # selector = scrapy.Selector(response)
        # items = selector.xpath('//li[@class="product-item"]')
        # print(items)
        # # title = selector.xpath('//h3[@class="item-heading"]/a/text()').extract()
        # # price = selector.xpath('//span[@class="price regular"]/text()').extract()
        # # a = selector.xpath('//a[@class="link"]/@href').extract()
        # for each in items:
        #     print(each)
        #     print("shit")
        #     title = each.xpath('//div[@class="item-details"/h3[@class="item-heading"]/a/text()').extract()[0]
        #     rate = each.xpath('//div[@class="item-details"/strong/span[@class="price regular"]/text()').extract()[0]
        #     print('标题:' + title)
        #     print('评分:' + rate)