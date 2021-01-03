import random
from time import sleep
from selenium import webdriver

# REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
driver = webdriver.Chrome(
    'D:\\Proyectos Personales\\WebScraping\\Nivel_3\\chromedriver.exe')
driver.get('https://www.olx.com.ec/autos_c378')
sleep(3)
driver.refresh()  # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh o al darle click a algun elemento
sleep(5)

boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
for i in range(3):  # click 3 veces
    try:
        boton.click()
        sleep(random.uniform(8.0, 10.0))
        boton = driver.find_element_by_xpath(
            '//button[@data-aut-id="btnLoadMore"]')
    except:
        break
autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
for auto in autos:
    precio = auto.find_element_by_xpath(
        './/span[@data-aut-id="itemPrice"]').text
    print(precio)
    descripcion = auto.find_element_by_xpath(
        './/span[@data-aut-id="itemTitle"]').text
    print(descripcion)
