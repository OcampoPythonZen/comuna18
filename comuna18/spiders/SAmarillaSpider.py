import scrapy

class SAmarillaSpider(scrapy.Spider):
    name = 'samarilla'
    allowed_domain = ['https://www.seccionamarilla.com.mx/']

    def start_requests(self):
        url = 'https://www.seccionamarilla.com.mx/'
        print("¿Palabra a Buscar? ", end="")
        palabra_clave = input()
        tag = getattr(self, 'tag', palabra_clave)
        if tag is not None:
            url = url + 'resultados/' + tag + '/1'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        
        for sa in response.css('div.row.l-info'):
            cont = 1
            yield {
                'nombre' : sa.css('span::text').extract_first(),
                'direccion' : sa.css('div.l-address span::text').extract_first(),
                'telefono' : sa.xpath('/html/body/div[6]/div[2]/div[2]/div[1]/ul/li['+str(cont)+']/div[1]/div[2]/div[2]/a/span/text()').extract_first(),
            }
            cont += 1
        next_page = response.xpath('/html/body/div[6]/div[2]/div[3]/div/ul/li[7]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)