import scrapy
import sys

class ArgostestSpider(scrapy.Spider):
    name = "argostest"
    start_urls = ["https://pricespy.co.uk/home-interior/white-goods/laundry-care/washing-machines/bosch-serie-4-wgg04409gb-white--p6467404#properties"]

    def parse(self, response):
        #Brand/Model Name operations
        '''        brand_name = response.css("div.Namestyles__ProductName-sc-269llv-0.kEQsqD.bolt-v2  h1 span::text").get().split()[0]
        model_name = response.css("div.Namestyles__ProductName-sc-269llv-0.kEQsqD.bolt-v2  h1 span::text").get().split()[1]
        
        
        print("******************************") 
        print(brand_name)
        print(model_name)
        

        print("******************************")
         
        capacity = response.css("div section div:nth-child(1) table tbody tr:contains('Precise wash capacity (kg)') td::text").get()
        print(capacity)
        
        rpm = response.css("div section div:nth-child(1)  table  tbody  tr:contains('Maximum spin speed (rpm)') td::text").get()
        print(rpm)
        
        price = response.css("").get()'''
        
        
        '''product_links = response.css("div.SpecCardstyles__ContentBlock-lugbee-4.hTXZJd.xs-row.xs-8--none.sm-10--none.md-8--none div.xs-12--none.sm-6--none a::attr(href)").getall()
        print(product_links)
        sys.exit()
        
        price_currency = response.css("div:nth-child(2) div.xs-block div:nth-child(1) section.xs-12--none.md-5--none.xl-4--none.pdp-right  section  ul  li  h2::text").getall()
       
        capacity = response.css("div section div:nth-child(1) table tbody tr:contains('Wash and Dry Cycle Capacity (kg)') td::text").get()
        print(capacity)

        
        rpm = response.css("div section div:nth-child(1)  table  tbody  tr:contains('spin speed (rpm)') td::text").get()
        print(rpm)'''
        
        '''        #Price operations
        price_currency = response.css("div.SpecCardstyles__PriceText-lugbee-8.hpakUN strong::text").getall()
        price = []
        for i in range(len(price_currency)):
            price.append(price_currency[i].replace("£",""))
        
        #Model/Brand name operations
        temp_name = [extract_model_name(product) for product in response.css('a.SpecCardstyles__Title-lugbee-5.gnfdWf::text').getall()]
        print(temp_name)
        none_indices = [index for index, value in enumerate(temp_name) if value is None]
        print(none_indices)
        temp_name = [i for i in temp_name if i is not None]
        print(temp_name)
        brand_name = []
        model_name = []
        for i in range(len(temp_name)):
            brand_name.append(temp_name[i].split()[0])
            model_name_temp = temp_name[i].split()
            model_name_temp.pop(0)
            model_name.append(" ".join(model_name_temp))
        print(brand_name)
        print(len(brand_name))
            
        #Capacity Operations
        capacity = []    
        #capacity_temp = response.css("tr:nth-child(4) td.WgSpecificationTablestyles__WgSpecTableContentValue-pbju1y-11.llKicb strong::text").getall()
        capacity_temp = response.css("div.SpecCardstyles__SpecContainer-lugbee-17.hcyurR.xs-12--none.md-8--none.md-block tr:contains('Wash capacity (kg)') strong::text").getall()
        print("*****************************************")
        print(capacity_temp)
        print(len(capacity_temp))
        for i in range(len(capacity_temp)):
            if len(capacity_temp) == len(price_currency) :
                capacity.append(capacity_temp[i].split("-")[1].replace(" ","").replace("kg",""))
            else:
                try:
                    capacity.append(response.css('a.SpecCardstyles__Title-lugbee-5.gnfdWf::text').getall()[i].split()[2].replace("kg",""))
                    float(capacity[:-1])
                except:
                    capacity.append("0")
        print(capacity)
        #RPM operations
        rpm_temp = response.css("div.SpecCardstyles__SpecContainer-lugbee-17.hcyurR.xs-12--none.md-8--none.md-block tr:nth-child(2) strong::text").getall()
        rpm = []
        for i in range(len(rpm_temp)) :
            if len(rpm_temp) == len(price_currency):
                rpm.append(rpm_temp[i])
            else:
                try:
                    rpm.append(response.css('a.SpecCardstyles__Title-lugbee-5.gnfdWf::text').getall()[i].split()[3])
                    float(rpm[:-1])
                except:
                    rpm.append("0")     
        
        print(rpm)    
        
        #Currency operations
        currency = []
        for i in range(len(price_currency)):
            currency.append(price_currency[i][0])
        
        #None element fixing
        if len(none_indices) >= 1 :
            for i in none_indices:
                capacity.pop(i)
                rpm.pop(i)
                price.pop(i)
                currency.pop(i)
        print("**********************************************") 
        print(capacity)
        print(rpm)
        print(price)
        print(currency) 
         
            
        #Database operations
        conn = sqlite3.connect('C:\\Users\\gorke\\OneDrive\\Masaüstü\\gorkem\\marketproject\\Market-Search\\marketscrapping\\England_Market\\washingmachines_argos_uk.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="washingmachines"')
        table_exists = cursor.fetchone()

        if not table_exists:
                cursor.execute(''
                CREATE TABLE washingmachines(
                user_id integer primary key not null on conflict ignore,               
                TYPE TEXT ,
                BRAND_NAME TEXT,
                MODEL_NAME TEXT,
                CAPACITY_kg TEXT,
                RPM TEXT,
                PRICE TEXT,
                CURRENCY TEXT 
                )  
                '')

        valid_combinations = [
                (6, 1000), (6, 1200), (6, 1400),
                (7, 1000), (7, 1200), (7, 1400),
                (8, 1000), (8, 1200), (8, 1400), (8, 1600),
                (9, 1000), (9, 1200), (9, 1400),
                (10, 1200), (10, 1400)
            ]             

        for i in range(len(price_currency)):
            try:
                current_combination = (float(capacity[i]), float(rpm[i]))
                if current_combination in valid_combinations:
                        cursor.execute(''
                INSERT OR IGNORE INTO washingmachines(TYPE, BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, CURRENCY)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                '', ("Washing Machine",brand_name[i], model_name[i], capacity[i],rpm[i],price[i],currency[i]))

            except Exception as e:
            #print(brand_name)
            #print(model_name)
                print(f"An error occurred: {e}")

        next_url = response.css("a.Paginationstyles__PageLink-sc-1temk9l-1.ifyeGc[data-test^='component-pagination-arrow-right']::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        
                
        conn.commit()
        conn.close()
        '''
        
        brand_name = response.css('#properties > div > section > section > div > div > div.hideInViewports-sc-0-0.iwivxM > div > section > div:nth-child(3) > div:nth-child(2) > span > a::text').get()
        print(brand_name)
        print("######################")
        
        