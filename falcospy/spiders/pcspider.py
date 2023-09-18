import scrapy

from falcospy.items import FalcospyItem

class PcspiderSpider(scrapy.Spider):
    name = "pcspider"
    allowed_domains = ["www.jumia.dz"]
    start_urls = ["https://www.jumia.dz/ordinateurs-pc/"]
    


    def parse(self, response):
        for pc in response.css('a.core'):
            pc_item = FalcospyItem(
            title = pc.css('div h3::text').get(),
            brand = pc.css('a').attrib['data-brand'],
            category = pc.css('a').attrib['data-category'],
            price = pc.css('div.prc::text').get(),
            old_price = pc.css('div.s-prc-w  div.old::text').get(),
            url = pc.css('a').attrib['href'],)
            yield pc_item
            
            
         