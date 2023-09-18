import scrapy
import openai
from falcospy.items import FalcospyItem

#OpenAI API key
api_key = "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"

custom_settings = {
        'FEEDS': {'data.json': {'format': 'json'}}
        }

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
        # Create an empty dictionary to store characteristic-name pairs
        characteristic_dict = {}
        # Extract characteristics and store them in a list
        characteristics = response.css('div.markup.-pam ul li::text').getall()
        
        for characteristic in characteristics:
            characteristic = characteristic.replace('\t',' ')
            name = self.generate_name_with_gpt3(characteristic)
            # Add the characteristic and its generated name to the dictionary
            characteristic_dict[name] = characteristic
        
        pc['images'] = response.css("div.sldr a").attrib['href']
        pc['url'] = response.url
        pc['title'] = response.css("h1::text").get()
        pc['brand'] = response.css('div.-pvxs a._more::text').get()
        pc['price'] = response.css('div.df span::text').get()
        pc['rate'] = response.css('div.stars::text').get()
        pc['description'] = response.css('div.markup b::text').get()  #prb
        pc['cpu'] = characteristic_dict['cpu']
        pc['ram'] = characteristic_dict['ram']
        pc['storage'] = characteristic_dict['storage']
        pc['screen'] = characteristic_dict['screen']
        pc['integrated_gpu'] = characteristic_dict['integrated_gpu']
        pc['dedicated_gpu'] = characteristic_dict['dedicated_gpu']
        pc['os'] = characteristic_dict['os']
        pc['battery'] = characteristic_dict['dedicated_gpu']
        pc['state'] = characteristic_dict['state']
        
        yield pc 
        
        
    def generate_name_with_gpt3(self, characteristic):
        # Make an API call to GPT-3
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Choose from this list (cpu,ram,storage,screen,integrated_gpu,dedicated_gpu,os,battery,state,other) the name of the following characteristic: {characteristic}",
            max_tokens=50,  # Adjust the maximum length of the response
            api_key=api_key
        )
        
        return response.choices[0].text.strip()