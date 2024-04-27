import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Selector
import csv
from ..pipelines import CSVPipeline  # Import CSVPipeline from pipelines module

class AdidasSpider(scrapy.Spider):
    name = "adidas"

    def __init__(self, *args, **kwargs):
        super(AdidasSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://shop.adidas.jp/men/']
        

    def parse(self, response):
        base_url = response.url.split('/')[:3]
        self.base_url = '/'.join(base_url)

        # Parse category list
        category_list = response.css('div.lpc-ukLocalNavigation_item a::attr(href)').getall()
        category_full_links = [f'{self.base_url}{link}' for link in category_list]

        # Parse pagination or get page list
        for cat_url in category_full_links:
            yield scrapy.Request(cat_url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        pagination = response.css('span.pageTotal::text').get()
        pages_num = int(pagination.strip()) if pagination else 1
        pagi_url = response.url
        #print(f'================={pagi_url}===============')
        for i in range(1, pages_num + 1):
            yield scrapy.Request(f'{pagi_url}&page={i}', callback=self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.css('a.image_link::attr(href)').getall()
        for l in [f'{self.base_url}{link}'for link in product_links]:
            print(f'Link_ url:=========={l}=======================')
            yield scrapy.Request(l, callback=self.parse_product)

    def parse_product(self, response):
        print(f'From Response:{response.url}======================')
        product_details = {}

        # Extract breadcrumb category
        breadcrumb_category = '/'.join(response.css('li.breadcrumbListItem.breadcrumbLink.test-breadcrumbLink::text').getall())
        product_details['breadcrumb_category'] = breadcrumb_category
        print(f'================={breadcrumb_category}===================')
        # Extract category
        category = response.css('span.categoryName::text').get()
        product_details['Category'] = category

        # Extract product name
        product_name = response.css('h1.itemTitle.test-itemTitle::text').get()
        product_details['Product_name'] = product_name

        # Extract pricing
        pricing = response.css('span.price-value::text').get()
        product_details['Pricing'] = pricing

        # Extract available sizes
        available_sizes = response.css('li.sizeSelectorListItem button.sizeSelectorListItemButton::text').getall()
        available_sizes = '/'.join(available_sizes)
        product_details['Available_size'] = available_sizes

        # Extract sense of size
        sense_of_size = '/'.join(response.css('div.label.test-label span::text').getall())
        product_details['Sense_of_the_size'] = sense_of_size
        print(product_details)
        yield product_details


# Run the spider with the pipeline
# process = CrawlerProcess(settings={
#     'ITEM_PIPELINES': {'__main__.CSVPipeline': 1},
# })
# process.crawl(AdidasSpider)
# process.start()
