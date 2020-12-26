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


class CruzVerde(CrawlSpider):  # Cuando es Spider Vertical u Horizatonal
    name = "CruzVerde"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
        'CLOSESPIDER_PAGECOUNT': 2
    }

    allowed_domains = ['cruzverde.cl']

    start_urls = [
        'https://www.cruzverde.cl/ofertas/ofertas-imperdibles/'
    ]
    # Tiempo a Esperar entre cada requerimiento que Scrapy haga a la pagina semilla
    download_delay = 1

    rules = (
        Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            # INFORMATION : Agrega parametros adicionales para crear la regla de paginas en base a un Boton
            # Si no coloco este parametro adicional siempre buscara en los tag <a> y href
            LinkExtractor(
                # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
                allow=r'start=\d+',
                tags=('button'),
                attrs=('data-url')
            ), follow=True, callback="parse_articulo"),
    )


# Self va por estar dentro de una clase


    def parse_articulo(self, response):
        sel = Selector(response)

        productos = sel.xpath('//div[@class="col-12 col-lg-4"]')

        for producto in productos:
            item = ItemLoader(Articulo(), producto)

            item.add_xpath(
                'Nombre', './/div[@class="tile-body px-3 pt-3 pb-0 d-flex flex-column pb-0"]//div[@class="pdp-link"]/a/text()')

            item.add_xpath('Precio',
                           './/span[contains(@class, "value ")]/text()')

            yield item.load_item()
