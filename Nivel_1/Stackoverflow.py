import requests
from bs4 import BeautifulSoup

encabezados={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

url="https://es.stackoverflow.com/questions"

respuesta=requests.get(url,headers=encabezados)

soup=BeautifulSoup(respuesta.text)

Contenedor=soup.find(id='questions')
Summary=Contenedor.find_all('div',class_='question-summary')

for questions in Summary:
    titulo = questions.find('h3').text
    descripcion = questions.find(class_='excerpt').text
    descripcion = descripcion.replace('\n','').replace('\r','').strip()
    print(titulo)
    print(descripcion)

