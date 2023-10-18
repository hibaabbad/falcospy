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
            value = value.replace(',','.')
            adapter['price'] = value
            
       
        value = adapter.get('rate')
        if value != None :
            value = value.replace('out of 5','')
            value = value.replace(' ','')
            adapter['rate'] = float(value)
        return item
    
class SaveToMySQLPipeline:

    def __init__(self):
       self.conn = mysql.connector.connect(
            host = 'localhost',database = 'jimin',user = 'root',password = 'jiminssilove')
       
        ## Create cursor, used to execute commands
        
       self.cur = self.conn.cursor()
        
        ## Create books table if none exists
       self.cur.execute("""
       CREATE TABLE IF NOT EXISTS Pcs(
            id int NOT NULL auto_increment,
            url VARCHAR(255),
            title VARCHAR(255), 
            price INTEGER,
            description TEXT, 
            cpu VARCHAR(255),
            ram VARCHAR(255),
            storage VARCHAR(255),
            screen VARCHAR(255),
            integrated_gpu VARCHAR(255),
            dedicated_gpu VARCHAR(255),
            rate INTEGER,
            brand VARCHAR(255),
            source VARCHAR(255),
            PRIMARY KEY (id)
        );""")
       self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Photos(
            id_ph int NOT NULL auto_increment,
            url_ph VARCHAR(1000),
            pc_id int NOT NULL,
            PRIMARY KEY (id_ph)
        );
        ALTER TABLE Photos ADD CONSTRAINT fk_photos_pc FOREIGN KEY (pc_id) REFERENCES Pcs(id) ON DELETE CASCADE;
        """)
    def process_item(self, item, spider):
         ## Define insert statement
        self.cur.execute("""INSERT INTO Pcs(
            url,title,price,description,cpu,ram,storage,screen,integrated_gpu,dedicated_gpu,
            rate,brand,source
            ) VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,'Jumia'
                )""", (
            item["url"],
            item["title"],
            float(item["price"]),
            item["description"],
            item["cpu"],
            item["ram"],
            item["storage"],
            item["screen"],
            item["integrated_gpu"],
            item["dedicated_gpu"],
            item["rate"],
            item["brand"]
        ))
        self.cur.execute(""" SELECT LAST_INSERT_ID();
        SET @pc_id = LAST_INSERT_ID();
        """)
        for i in item['images']:
            self.cur.execute("""INSERT INTO photos (pc_id,url_ph)
        VALUES (@pc_id, i);""")
        
        


        ## Execute insert of data into database
        self.conn.commit()
        

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
