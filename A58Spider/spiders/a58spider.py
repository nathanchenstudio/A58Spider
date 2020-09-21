import base64
import re
import time
from datetime import datetime
from fontTools.ttLib import TTFont
from io import BytesIO
import scrapy

from A58Spider.items import A58SpiderItem


class A58Spider(scrapy.Spider):
    name = 'a58'
    allowed_domains = ['58.com']
    start_urls = ['https://hz.58.com/zufang/0/j1/?minprice=1700_2700&sourcetype=5']

    def parse(self, response, **kwargs):
        font_ttf = re.findall("charset=utf-8;base64,(.*?)'\)", response.text)[0]
        font = TTFont(BytesIO(base64.decodebytes(font_ttf.encode())))
        numbering = font.get('cmap').tables[0].ttFont.get('cmap').tables[0].cmap

        lis = response.xpath('//ul[@class="house-list"]/li[@class="house-cell"]')
        for li in lis:
            infor = li.xpath('div[@class="des"]/p[@class="infor"]//text()').extract()
            infor = [x.strip() for x in infor if x.strip()]
            if len(infor) < 2:
                print(infor)
                continue

            item = A58SpiderItem()
            item['url'] = li.xpath('div[@class="des"]/h2/a/@href').extract()[0]
            item['area'] = infor[0]
            item['community'] = infor[1]

            sent_time = li.xpath('div[@class="list-li-right"]/div[@class="send-time"]/text()').extract()
            sent_time = [x.strip() for x in sent_time if x.strip()]
            item['date'] = self.convert_time(sent_time[0].strip()) if sent_time else 'Unknown'

            if len(infor) >= 3:
                metro_data = re.match(r'距(.*)号线(.*?)地铁站步行(.*?)m', infor[2])
                if metro_data:
                    item['metro'] = metro_data.group(1)
                    item['subway_station'] = metro_data.group(2)
                    item['distance'] = int(metro_data.group(3))
                else:
                    print(infor[2])
                    continue
            else:
                # item['metro'] = 'Unknown'
                # item['subway_station'] = 'Unknown'
                # item['distance'] = 'Unknown'
                print('No subway info, drop', item['community'])
                continue

            price = li.xpath('div[@class="list-li-right"]/div[@class="money"]/b/text()').extract()[0]
            item['price'] = self.convert_real_word(numbering, price)

            rooms = li.xpath('div[@class="des"]/h2'
                             '/a/text()').extract()[0].replace(item['community'], '').strip()
            item['rooms'] = self.convert_real_word(numbering, rooms)

            yield item

        next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href').extract()
        if next_page:
            yield scrapy.Request(next_page[0])

    @staticmethod
    def convert_real_word(numbering: dict, fake_word: str) -> str:
        word_list = []
        for char in fake_word:
            decode_num = ord(char)
            if decode_num in numbering:
                num = numbering[decode_num]
                num = int(num[-2:]) - 1
                word_list.append(str(num))
            else:
                word_list.append(char)
        real_word = ''.join(word_list)
        return real_word

    @staticmethod
    def convert_time(t: str) -> datetime:
        min = re.findall('\d+', t)[0]
        if '分钟' in t:
            c = time.time() - int(min) * 60
        elif '小时' in t:
            c = time.time() - int(min) * 60 * 60
        elif '天' in t:
            c = time.time() - int(min) * 60 * 60 * 24
        else:
            c = datetime.strptime(t, '%m-%d').replace(year=2020)
            return c
        c = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(c))
        return datetime.strptime(c, "%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl('a58')
    process.start()
