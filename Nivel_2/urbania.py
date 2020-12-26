from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule
from scrapy.loader.processors import MapCompose


class Inmueble(Item):
    Nombre = Field()
    Direccion = Field()


class Urbania(CrawlSpider):  # Cuando es Spider Vertical u Horizatonal
    name = "Urbania"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
        'CLOSESPIDER_ITEMCOUNT': 2,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': 'API'
    }

    allowed_domains = ['urbania.pe']

    start_urls = [
        'https://urbania.pe/buscar/casas?page=1',
        'https://urbania.pe/buscar/casas?page=2'

    ]
    # Tiempo a Esperar entre cada requerimiento que Scrapy haga a la pagina semilla
    Rule(
        # Verticalidad
        LinkExtractor(
            allow=r'/proyecto-'
        ), follow=True, callback='parse_inmueble'

    ),

# Self va por estar dentro de una clase

    def parse_inmueble(self, response):
        sel = Selector(response)
        item = ItemLoader(Inmueble(), sel)

        item.add_xpath('nombre', '//h2[@class="info-title"]/text()')
        item.add_xpath('direccion', '//h2[@class="info-location"]/text()')

        yield item.load_item()
