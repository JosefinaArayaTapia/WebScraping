from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Questions(Item):
    titulo=Field()
    descripcion=Field()


class StackoverFlow(Spider):
  name="Spider"
  custom_settings ={
          'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
  }
  start_urls=['https://es.stackoverflow.com/questions']



  def parse(self, response):
     sel= Selector(response)
     preguntas=sel.xpath('//div[@id="questions"]//div[@class="question-summary"]')

     for pregunta in preguntas:
         item = ItemLoader(Questions(),pregunta)
         item.add_xpath('titulo','.//h3/a/text()')
         item.add_xpath('descripcion','.//div[@class="excerpt"]/text()')

         yield item.load_item()
