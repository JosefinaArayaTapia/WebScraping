from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
#Scrapy-> para hacer el requerimientos y BeautifulSoup-> Libreria para parsear el arbol

class Noticias(Item):
    titulo=Field()
    descripcion=Field()


class ElUniverso(Spider):
  name="UniversoSpider"
  custom_settings ={
          'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
  }
  start_urls=['https://www.eluniverso.com/deportes']

  def parse(self, response):
     sel= Selector(response)
     Not=sel.xpath('//div[@class="view-content"]//div[@class="posts"]')

     for noticia in Not:

         item = ItemLoader(Noticias(),noticia)
         item.add_xpath('titulo','.//h2/a/text()')
         item.add_xpath('descripcion','.//p/text()')

         yield item.load_item()
         
