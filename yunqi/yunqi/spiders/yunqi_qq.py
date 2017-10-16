# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yunqi.items import BookItem, BookDetail
from scrapy.utils.project import get_project_settings


class YunqiQqSpider(CrawlSpider):
    name = 'yunqi.qq'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n10p1']

    rules = (
        Rule(LinkExtractor(allow=r'bk/so2/n10p\d+'), callback='parse_book', follow=True),
    )

    def parse_book(self, response):
        books = response.xpath('.//div[@class="book"]')
        for book in books:
            img_url = book.xpath('./a/img/@src').extract_first()
            info = book.xpath('./div[@class="book_info"]')
            name = info.xpath('./h3/a/text()').extract_first()
            id = info.xpath('./h3/em/a[2]/@bid').extract_first()
            detail = info.xpath('./dl/dd[@class="w_auth"]')
            author = ''
            category = ''
            last_update = ''
            if len(detail) == 5:
                author, category = detail[:2].xpath('./a/text()').extract()
                last_update, = detail[3].xpath('./text()').extract()
            book_item = BookItem(id=id, name=name, img_url=img_url, author=author,
                                 category=category, last_update=last_update)
            yield book_item
            book_detail_url = info.xpath('./h3/a/@href').extract_first()
            yield scrapy.Request(book_detail_url, callback=self.parse_book_detail, meta={'id': id})

    def parse_book_detail(self, response):
        id = response.meta['id']
        label = response.xpath('.//div[@class="tags"]/text()').extract_first().strip()
        tds = response.xpath('.//div[@id="novelInfo"]/table/tr[position()>1]/td')
        all_click = 0
        all_popular = 0
        all_commend = 0
        month_click = 0
        month_popular = 0
        month_commend = 0
        week_click = 0
        week_popular = 0
        week_commend = 0
        word_num = 0
        comment_num = 0
        status = ''
        if len(tds) == 12:
            details = tds.xpath('string(.)').extract()
            all_click, all_popular, all_commend, month_click, month_popular, month_commend,\
            week_click, week_popular, week_commend, word_num, comment_num, status = details
        yield BookDetail(all_click=all_click, all_popular=all_popular, all_commend=all_commend,
                         month_click=month_click, month_popular=month_popular, month_commend=month_commend,
                         week_click=week_click, week_popular=week_popular, week_commend=week_commend,
                         word_num=word_num, id=id, label=label, comment_num=comment_num, status=status)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(YunqiQqSpider)
    process.start()


