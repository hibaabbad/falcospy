import scrapy

from falcospy.items import FalcospyItem



class JumiaspiderSpider(scrapy.Spider):
    name = "jumiaspider"
    allowed_domains = ["www.jumia.dz"]
    start_urls = ["https://www.jumia.dz/mlp-ordinateurs-accessoires-informatique/ordinateurs-tablettes-ordinateurs-portables-traditionnels/"]
                

    def parse(self, response):
        pcs = response.css('article.prd')
        for pc in pcs:
            relative_url = pc.css('a').attrib['href']
            pc_url = 'https://www.jumia.dz/' + relative_url
            yield scrapy.Request(pc_url, callback=self.parse_pc_page)

    def parse_pc_page(self, response):
        
        pc = FalcospyItem()
        
        pc['images'] = response.css("div.sldr a::attr(href)").getall()
        pc['url'] = response.url
        pc['title'] = response.css("h1::text").get()
        pc['brand'] = response.css('div.-pvxs a._more::text').get()
        pc['price'] = response.css('div.df span::text').get()
        pc['rate'] = response.css('div.stars::text').get()
        description= response.css('div.markup b::text').get()  #prb
        pc['description'] = description.replace('\n',' ')
        # Extract characteristics and store them in a list
        characteristics = response.css('div.markup.-pam ul li::text').getall()
        
        for character in characteristics:
            
            character = character.replace('\t',' ')
            character = character.replace('\n',' ')
            
            character = character.replace('é','e')
            character = character.lower()
            
            if "processeur" in character or "cpu" in character : 
                pc['cpu'] = character
            if "memoire" in character or "ram" in character : 
                pc['ram'] = character
            if "disque" in character or "stockage" in character : 
                pc['storage'] = character
            if "ecran" in character: 
                pc['screen'] = character
            if "carte graphique integre"  in character : 
                pc['integrated_gpu'] = character
            else: pc['integrated_gpu'] = None
            if "carte graphique dediee"  in character : 
                pc['dedicated_gpu'] = character
            else: pc['dedicated_gpu'] = None
        yield pc 
    