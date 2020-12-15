from typing import Callable
from scrapy import linkextractors
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule
from scrapy.loader.processors import MapCompose

# Varios tipos de Items y 2 dimensiones
# horizontales (Extracción de IGN)


class Articulo(Item):
    Titulo = Field()
    Contenido = Field()


class Reviews(Item):
    Titulo = Field()
    Calificacion = Field()


class Videos(Item):
    Titulo = Field()
    FechaPublicacion = Field()


class IGNSpider(CrawlSpider):  # Cuando es Spider Vertical u Horizatonal
    name = "IGN"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
        'CLOSESPIDER_PAGECOUNT': 30
    }

    allowed_domains = ['latam.ign.com']

    start_urls = [
        'https://latam.ign.com/se/?type=video&q=nintendo%20switch'
    ]
    # Tiempo a Esperar entre cada requerimiento que Scrapy haga a la pagina semilla
    download_delay = 1

    rules = (
        # Horizotalidad por Tipo de Informacion
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True

        ),
        # Horizantalidad por Paginacion
        Rule(
            LinkExtractor(
                allow=r'&page=\d+'
            ), follow=True

        ),
        # Regla por cada tipo de contenido
        # Articulo
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback='parse_articulo'

        ),
        # Review
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ), follow=True, callback='parse_review'
        ),
        # Videos
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ), follow=True, callback='parse_video'
        ),

    )

    def parse_articulo(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_xpath('Titulo', './/h1/text()')
        item.add_xpath(
            'Contenido', './/div[@id="id_text"]//*/text()')

        yield item.load_item()

    def parse_review(self, response):
        item = ItemLoader(Reviews(), response)
        item.add_xpath('Titulo', './/div[@class="article-headline"]/h1/text()')
        item.add_xpath(
            'Calificacion', '//span[@class="side-wrapper side-wrapper hexagon-content"]/text()')

        yield item.load_item()

    def parse_video(self, response):
        item = ItemLoader(Videos(), response)
        item.add_xpath('Titulo', './/h1/text()')
        item.add_xpath(
            'FechaPublicacion', './/span[@class="publish-date"]/text()')

        yield item.load_item()
