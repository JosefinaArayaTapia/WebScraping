from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule
from scrapy.loader.processors import MapCompose


class Articulo(Item):
    Nombre = Field()
    Precio = Field()
    Descripcion = Field()


class MercadoLibre(CrawlSpider):  # Cuando es Spider Vertical u Horizatonal
    name = "MercadoLibre"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
        'CLOSESPIDER_PAGECOUNT': 20
    }

    allowed_domains = ['listado.mercadolibre.cl', 'articulo.mercadolibre.cl']

    start_urls = [
        'https://listado.mercadolibre.cl/trekking-montanismo'
    ]
    # Tiempo a Esperar entre cada requerimiento que Scrapy haga a la pagina semilla
    download_delay = 1

    rules = (
        Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
                allow=r'/_Desde_\d+'
            ), follow=True),
        Rule(  # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/MLC-'
            ), follow=True, callback='parse_articulo'),  # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )


# Self va por estar dentro de una clase

    def parse_articulo(self, response):

        item = ItemLoader(Articulo(), response)
        item.add_xpath('Nombre', './/h1[@class="ui-pdp-title"]/text()')
        item.add_xpath(
            'Precio', '//div[@class="ui-pdp-price__second-line"]/span[@class="price-tag ui-pdp-price__part"]/span[@class="price-tag-fraction"]/text()')
        item.add_xpath(
            'Descripcion', './/div[@class="ui-pdp-description"]/p/text()')

        yield item.load_item()
