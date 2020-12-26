from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule
from scrapy.loader.processors import MapCompose

# 2 niveles de profundidad (Extracción de TRIP ADVISOR con Scrapy PT.3)


class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()
    hotel = Field()


# Cuando es Spider Vertical u Horizatonal
class TripAdvisoryReviews(CrawlSpider):
    name = "TripAdvisoryReviews"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100
    }
    start_urls = [
        'https://www.tripadvisor.cl/Hotels-g294292-Los_Lagos_Region-Hotels.html']
    # Tiempo a Esperar entre cada requerimiento que Scrapy haga a la pagina semilla
    download_delay = 1
    allowed_domains = ['tripadvisor.cl']

    rules = (
        # Paginacion de Hoteles
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-'
            ), follow=True
        ),
        # Detalle de hotels
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=[
                    '//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]']
            ), follow=True
        ),
        # Paginacion de Reviews de Hoteles
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ), follow=True
        ),

        # Detalla de Reviews
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=[
                    '//div[@data-test-target="reviews-tab"]']
            ), follow=True, callback='parse_opinion'
        ),
    )

    def parse_opinion(self, response):
        # Como  existen muchas opiniones por usuario, se debe recorrer
        sel = Selector(response)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get()

        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_value('autor', autor)
            item.add_xpath(
                'titulo', './/div[@class="_3IEJ3tAK _2K4zZcBv"]/text()')
            # div[@title] => divs que contengan el atributo title
            item.add_xpath(
                'hotel', './/div[contains(@class, "ui_card section")]//div[@title]/text()')
            item.add_xpath('contenido', './/q/text()',
                           MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
            item.add_xpath(
                'calificacion', './/div[contains(@class, "ui_card section")]//a/div/span[contains(@class, "ui_bubble_rating")]/@class', MapCompose(lambda i: i.split('_')[-1]))
            yield item.load_item()
