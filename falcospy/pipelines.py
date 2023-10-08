# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class FalcospyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        value = adapter.get('price')
        if value != None :
            value = value.replace('DA','')
            value = value.replace(' ','')
            adapter['price'] = value
            
       
        value = adapter.get('rate')
        if value != None :
            value = value.replace('out of 5','')
            value = value.replace(' ','')
            adapter['rate'] = int(value)
        return item
    
"""class SaveToMySQLPipeline:

    def __init__(self):
       self.conn = mysql.connector.connect(
            host = 'localhost',database = 'falcospy',user = 'root',password = 'jiminssilove')
       
        ## Create cursor, used to execute commands
        
       self.cur = self.conn.cursor()
        
        ## Create books table if none exists
       self.cur.execute(
       CREATE TABLE IF NOT EXISTS Pcs(
            id int NOT NULL auto_increment,
            url VARCHAR(255),
            title VARCHAR(255), 
            price DECIMAL(10, 1),
            description TEXT, 
            cpu VARCHAR(255),
            ram VARCHAR(255),
            storage VARCHAR(255),
            screen VARCHAR(255),
            integrated_gpu VARCHAR(255),
            dedicated_gpu VARCHAR(255),
            os VARCHAR(255),
            battery VARCHAR(255),
            images TEXT,
            rate INTEGER,
            brand VARCHAR(255),
            source VARCHAR(255),
            PRIMARY KEY (id)
        )
        )

    def process_item(self, item, spider):
         ## Define insert statement
        self.cur.execute(insert into Pcs(
            url,
            title, 
            price,
            description, 
            cpu,
            ram,
            storage,
            screen,
            integrated_gpu,
            dedicated_gpu,
            os,
            battery,
            images,
            rate,
            brand,
            source,
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                GETDATE(),
                'Jumia'
                ), (
            item["url"],
            item["title"],
            item["price"],
            item["description"],
            item["cpu"],
            item["ram"],
            item["storage"],
            item["screen"],
            item["integrated_gpu"],
            item["dedicated_gpu"],
            item["os"],
            item["battery"],
            item["images"],
            item["rate"],
            item["state"],
            item["brand"],
        ))

        ## Execute insert of data into database
        self.conn.commit()
        

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()"""
