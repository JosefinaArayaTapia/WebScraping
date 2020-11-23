from requests.models import Response
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
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
      soup = BeautifulSoup(response.body)
      Contenedor=soup.find_all('div',class_='view-content')

      for container in Contenedor:
          #b4s = Solo hijos directos del contenedor
          notices=container.find_all('div',class_='posts',recursive=False)

          for notice in notices:
              item = ItemLoader(Noticias(),response.body)
              tittle =notice.find('h2').text
              description = notice.find('p')
              if (description != None):
                  description = description.text
              else:
                  description='N/A'
                   
              item.add_value('titulo',tittle)
              item.add_value('descripcion',description)

              yield item.load_item()
            

     
         
