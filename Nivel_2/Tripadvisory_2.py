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


# Cuando es Spider Vertical u Horizatonal
class TripAdvisoryReviews(CrawlSpider):
    name = "TripAdvisoryReviews"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 10
    }
    start_urls = [
        'https://www.tripadvisor.cl/Hotels-g2615228-Los_Rios_Region-Hotels.html']
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
                    '//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]/a[@data-clicksource="HotelName "]']
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
                    '//div[@data-test-target="reviews-tab"]//a[contains(@class,"ui_header_link")]']
            ), follow=True, callback='parse_opinion'
        ),
    )

    def parse_opinion(self, response):
        # Como  existen muchas opiniones por usuario, se debe recorrer
        sel = Selector(response)
        opiniones = sel.xpath('//div[@class="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get()

        for opinion in opiniones:
            item = ItemLoader(Opinion(), response)
            item.add_xpath(
                'titulo', './/a[contains(@href,"Show")]/div/div[1]/text()')
            item.add_xpath(
                'contenido', './/q/text()')
            item.add_value(
                'autor', autor)

            yield item.load_item()
