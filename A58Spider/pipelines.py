# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime

from openpyxl import Workbook
from scrapy.exceptions import DropItem


class FilterPipeline:
    def process_item(self, item, spider):
        if item['community'] in spider.settings.get('COMMUNITY_BLACKLIST'):
            raise DropItem(f'Drop {item["community"]}, community blacklist')
        if item['subway_station'] in spider.settings.get('SUBWAY_STATION_BLACKLIST'):
            raise DropItem(f'Drop {item["community"]}, subway blacklist: {item["subway_station"]}')
        if item['distance'] > spider.settings.get('MIN_DISTANCE_TO_SUBWAY'):
            raise DropItem(f'Drop {item["community"]}, too far way from subway: {item["distance"]}')
        return item


class ExcelFilePipeline:
    def open_spider(self, spider):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['URL', 'Area', 'Community', 'Rooms', 'Price', 'Date', 'Metro', 'Subway Station', 'Distance'])

    def close_spider(self, spider):
        file_path = f'{spider.settings.get("DATA_FILE_PATH")}/{spider.name}_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
        self.wb.save(file_path)

    def process_item(self, item, spider):
        self.ws.append([item['url'],
                        item['area'],
                        item['community'],
                        item['rooms'],
                        item['price'],
                        item['date'],
                        item['metro'],
                        item['subway_station'],
                        item['distance']])
        return item
