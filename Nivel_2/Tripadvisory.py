#Spider Vertical a Hoteles -> primera pagina y entrar a cada uno
#Obtener Nombre, precio y Comodidades
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule
from scrapy.loader.processors import MapCompose


class Hotel(Item):
    Nombre=Field()
    Precio=Field()
    Descripcion=Field()
    Comodidades=Field()

class TripAdvisory(CrawlSpider):  #Cuando es Spider Vertical u Horizatonal
  name="TripAdvisory"
  custom_settings ={
          'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
  }
  start_urls=['https://www.tripadvisor.cl/Hotels-g187791-Rome_Lazio-Hotels.html']
  #Tiempo a Esperar entre cada requerimiento que Scrapy haga a la pagina semilla
  download_delay= 2

  rules=(
      Rule(
          LinkExtractor(
              allow=r'/Hotel_Review-'
          ),follow=True,callback='parse_hotel'
      ),

  )
  def quitarSimboloPeso(self,texto):
      nuevoText=texto.replace("$","")
      return nuevoText


  def parse_hotel(self, response):
      sel= Selector(response)
      item = ItemLoader(Hotel(),sel)
      item.add_xpath('Nombre','.//h1[@id="HEADING"]/text()')
      item.add_xpath('Precio',
        './/div[@id="taplc_resp_hr_atf_meta_component_0"]/div/div/div[1]/div/div/div[2]/div[1]/div/text()',
        MapCompose(self.quitarSimboloPeso))
      item.add_xpath('Descripcion','.//div[@id="ABOUT_TAB"]/div[2]/div[1]/div[7]/div[1]/div[1]/div/p/text()')
      item.add_xpath('Comodidades','.//div[contains(@data-test-target, "amenity_text")]/text()')

      yield item.load_item()

