from bs4 import BeautifulSoup
import requests

# html_txt = requests.get('https://habi.co/venta-apartamentos/bogota?page=1').content

# with open('html.html', 'w', encoding='utf-8') as f:
#     f.write(str(html_txt))
# soup = BeautifulSoup(html_txt, 'html.parser')
# titles = soup.find_all('a', class_='card-details')
# with open('soup.html', 'w', encoding='utf-8') as f:
#     f.write(str(soup))
# print(len(titles))
# for title in titles:
#     print(title.text)

# we are going to use selenium to get the data from the page
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()
driver.get('https://habi.co/venta-apartamentos/bogota?page=1')
time.sleep(4)
soup = BeautifulSoup(driver.page_source, 'html.parser')
titles = soup.find_all('a', class_='card-details')
hrefs = [title.get('href') for title in titles]
print('-'*30)
for href in hrefs[0:1]:
    print(href)
    driver.get(href)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/section/article/section/div/ul/li[2]/div/div[2]/div/div/div/div/section/article/ul/li[1]/ul')))
    # element = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/section/article/section/div/ul/li[2]/div/div[2]/div/div/div/div/section/article/ul/li[1]/ul')
    # print(element.text)
    property_soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(property_soup.find('ul', class_='details-container'))
    
    
    
# conjunto administracion estrato antiguedad remodelado area habitaciones banos parqueadero deposito elevador garaje porteria zona_lavanderia gas precio direccion



