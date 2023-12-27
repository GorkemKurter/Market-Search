import scrapy


class WmeuronicsitaSpider(scrapy.Spider):
    name = "wmeuronicsITA"
    start_urls = ["https://www.euronics.it/elettrodomestici/grandi-elettrodomestici/lavatrici/?prefn1=tipoCarica&prefv1=Frontale"]

    def parse(self, response):
        
        product_urls = response.css("#maincontent  div.container.search-results.px-0  div:nth-child(4)  div:nth-child(4)  div  div.col-sm-12.col-md-9  div.row.product-grid  div:contains('product')  div  div.product-tile  div.tile-body  div.tile-hover-hidden  div.pdp-link  a::attr(href)").getall()
        print(product_urls)
        
        for i in product_urls:
            yield scrapy.Request(url ="https://www.euronics.it/" + i, callback = self.parse_product)
        
        next_url = next_page_url = response.css('button[data-url-full]::attr(data-url-full)').get()
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        
    def parse_product(self, response):
        
        #Brand/Model name operations
        brand_name = response.css("div.product-details-js h1::text").get().split("-")[0]
        model_name = response.css("div.product-details-js h1::text").get().split("-")[1].replace("Lavatrice",'')
        
        #Capacity operations
        capacity = response.css("#body-technicalSpecifications > div > div > div > ul:nth-child(2) > li:nth-child(2) > span.keyMapRight::text").get().replace("\n","")
        
        #RPM operations
        rpm = response.css("#body-technicalSpecifications > div > div > div > ul:nth-child(2) > li:nth-child(1) > span.keyMapRight::text").get().replace("\n","")
        
            