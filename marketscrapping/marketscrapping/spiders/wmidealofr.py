import scrapy
import sqlite3
import re

class WmidealofrSpider(scrapy.Spider):
    name = "wmidealofr"
    start_urls = ["https://www.idealo.fr/cat/1941F1203607/lave-linge.html"]

    def parse(self, response):
        
        name = response.css("div.sr-productSummary div.sr-productSummary__title::text").getall()
        brand_name = []
        model_name = []
        for i in name:
            parts = i.split(' ')
            brand = parts[0]
            model = ' '.join(parts[1:])
            brand_name.append(brand)
            model_name.append(model)

        temp_list_capacity_rpm = response.css("div.sr-productSummary__description p span::text").getall()
        for i in range(len(temp_list_capacity_rpm)):
            temp_list_capacity_rpm[i].replace(u'\xa0',u'')
        print(temp_list_capacity_rpm)
        #Capacity Operations
            