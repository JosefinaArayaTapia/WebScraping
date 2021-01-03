import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
driver = webdriver.Chrome(
    'D:\\Proyectos Personales\\WebScraping\\Nivel_3\\chromedriver.exe')
driver.get('https://www.olx.com.ec/')
sleep(3)
driver.refresh()  # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh o al darle click a algun elemento
sleep(5)

for i in range(3):  # click 3 veces
    try:
        boton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )
        boton.click()
        # 20 anuncios de carga inicial, y luego 20 anuncios por cada click que he dado
        nAnuncios = 20 + ((i + 1) * 20)
        # Espero hasta 10 segundos a que toda la informacion del ultimo anuncio este cargada
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//li[@data-aut-id="itemBox"][' + str(nAnuncios) + ']'))
        )
    except:
        break


eventos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
for evento in eventos:
    precio = evento.find_element_by_xpath(
        './/span[@data-aut-id="itemPrice"]').text
    print(precio)
    descripcion = evento.find_element_by_xpath(
        './/span[@data-aut-id="itemTitle"]').text
    print(descripcion)
