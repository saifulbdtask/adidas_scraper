import scrapy

class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    start_urls = ['https://shop.adidas.jp/men/']
    # def get_all_link(self,response):
    #     link=[]
    #     for product_link in response.css("div.lpc-ukLocalNavigation_item li a::attr(href)").extract():
    #         link.append(product_link)
    #     print(link)
    def parse(self, response):
        # product_page=response.css("div.lpc-ukLocalNavigation_item li a::attr(href)").extract()
        # print(product_page)
        for product_link in response.css("div.lpc-ukLocalNavigation_item li a::attr(href)").extract():
            print(f'================{product_link}=================')
            yield response.follow(product_link, callback=self.parse_product)

    def parse_product(self, response):
        yield {
            'name': response.css('h1.product-name::text').get(),
            'price': response.css('span.product-price::text').get(),
            'description': response.css('div.product-description::text').get(),
            # Add more fields as needed
        }
