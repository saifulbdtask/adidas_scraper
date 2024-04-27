# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AdidasScraperPipeline:
    def process_item(self, item, spider):
        return item

# pipelines.py

import csv

class CSVPipeline:
    def open_spider(self, spider):
        self.csv_file = open('adidas_products.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=['breadcrumb_category', 'Category', 'Product_name', 'Pricing', 'Available_size', 'Sense_of_the_size'])
        self.csv_writer.writeheader()

    def close_spider(self, spider):
        self.csv_file.close()

    def process_item(self, item, spider):
        self.csv_writer.writerow(item)
        return item
