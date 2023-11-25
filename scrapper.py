import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd



#custom condition for WebdriverWait to check if all elementes are in the filtered city
# class check_all_elements_present(object):
#     def __init__(self, locator, city):
#         self.locator = locator
#         self.city = city

#     def __call__(self, driver):
#         elements = driver.find_elements(*self.locator)
#         #if all elements are in the filtered city, return True
#         if all(element.text == self.city for element in elements):
#             return elements
#         else:
#             return False
    
def convert_to_int(x):   
    return 0 if x == 'No Tiene' or x == '' else x

def get_property_details(driver, href):
    driver.get(href)
    # print('-'*50)
    # print(href)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/main/section/article/section/div/ul/li[2]/div/div[2]/div/div/div/div/section/article/ul/li[1]/ul'))
        )
        # print('Success')
        # num_success += 1
    except Exception as e:
        # print(f'Error: {e}')
        print(f'Error in {href}')
        # num_errors += 1
        return None

    property_soup = BeautifulSoup(driver.page_source, 'html.parser')
    details = property_soup.find_all('div', class_='detail-item')

    details_to_add = {'conjunto': '', 'administración': '', 'estrato': '', 'antiguedad': '', 'remodelado': '',
                      'área': '', 'habitaciones': '', 'baños': '', 'garajes': '', 'elevadores': '', 'tipo_de_inmueble': '',
                      'deposito': '', 'porteria': '', 'zona_de_lavanderia': '', 'gas': '', 'parqueadero': '',
                      'precio': '', 'direccion': '', 'nombre': '', 'descripcion': ''}
    
    for detail in details:
        detail_title = detail.find('p', class_='item-title').text.lower().replace(' ', '_').replace('*', '')
        detail_description = detail.find('p', class_='item-description').text
        details_to_add[detail_title] = detail_description

    details_to_add.update({
        'precio': property_soup.find('p', class_='current-price').text,
        'direccion': property_soup.find('div', class_='title-location').text,
        'nombre': property_soup.find('h1', class_='header-title').text,
        'descripcion': property_soup.find('p', class_='description-text').text
    })

    return details_to_add

def scrape_page(driver, city, page):
    driver.get(f'https://habi.co/venta-apartamentos/{city}?page={page}')
    # WebDriverWait(driver, 10).until(check_all_elements_present((By.CLASS_NAME, 'card-city'), 'BOGOTÁ'))
    time.sleep(7)
        
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    titles = soup.find_all('a', class_='card-details')
    hrefs = [title.get('href') for title in titles]

    properties_data = [get_property_details(driver, href) for href in hrefs if href] #filter out None values
    properties_data = [property for property in properties_data if property] #filter none values from properties_data
    # num_errors = len([property for property in properties_data if property is None])
    properties_df = pd.DataFrame(properties_data)


    # print(f'Page {page} scraped with {num_errors} errors')
    return properties_df

city = 'bogota'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
num_pages_to_scrape = 19
properties_df = pd.DataFrame()
# total_errors = 0
for page in range(1, num_pages_to_scrape + 1):
    properties_df= pd.concat([properties_df, scrape_page(driver, city, page)])
    print(f'Page {page} scraped')
driver.quit()

#cleaning process of the dataframe
properties_df['administración'] = properties_df['administración'].apply(lambda x: '0' if x == '' else x.replace('$', '').replace('.', '').strip()).astype('int')
properties_df['elevadores'] = properties_df['elevadores'].apply(convert_to_int).astype('int')
properties_df['área'] = properties_df['área'].apply(lambda x: x.replace('m2', '').replace(',', '.')).astype('float')
properties_df['habitaciones'] = properties_df['habitaciones'].apply(convert_to_int).astype('int')
properties_df['baños'] = properties_df['baños'].apply(convert_to_int).astype('int')
properties_df['garajes'] = properties_df['garajes'].apply(convert_to_int).astype('int')
properties_df['antiguedad'] = properties_df['antiguedad'].str.extract(r'(\d+)').astype('int')
properties_df['deposito'] = properties_df['deposito'].apply(convert_to_int).astype('int')
properties_df['precio'] = properties_df['precio'].str.replace('.','').str.extract(r'(\d+)').astype('float')
properties_df['barrio'] = properties_df['direccion'].apply(lambda x: x.split('/')[1].strip())
properties_df['direccion'] = properties_df['direccion'].apply(lambda x: x.split('/')[0].strip())
properties_df['nombre'] = properties_df['nombre'].apply(lambda x: x.split('Bogotá')[1].strip())


#saving the dataframe to a csv file
properties_df.to_csv('properties.csv', index=False)
print('Scrapping finished')