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
        lowercase_keys = ['category']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if value != None :
                value = value.lower()
                adapter[lowercase_key] = value.replace('computing/computers & accessories/computers & tablets/laptops','')
            
        price_keys = ['price', 'old_price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value != None :
               value = value.replace('DA','')
               value = value.replace(' ','')
               adapter[price_key] = value

        return item
    
class SaveToMySQLPipeline:

    def __init__(self):
       self.conn = mysql.connector.connect(
            host = 'localhost',database = 'falcospy',user = 'root',password = 'jiminssilove')
       
        ## Create cursor, used to execute commands
        
       self.cur = self.conn.cursor()
        
        ## Create books table if none exists
       self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pcs(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title text,
            price DECIMAL,
            old_price DECIMAL,
            category VARCHAR(255),
            brand text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
         ## Define insert statement
        self.cur.execute(""" insert into pcs(
            url, 
            title, 
            price,
            old_price,
            category,
            brand
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["price"],
            item["old_price"],
            item["category"],
            item["brand"]
        ))

        ## Execute insert of data into database
        self.conn.commit()
        

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
