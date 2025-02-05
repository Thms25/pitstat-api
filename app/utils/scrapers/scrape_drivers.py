import requests
from bs4 import BeautifulSoup
from pprint import pprint

def scrape_drivers():
    url = 'https://www.formula1.com/en/drivers'
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        document = BeautifulSoup(html, 'html.parser')

        drivers = []

        # driver_elements = document.select('.f1-driver-listing-card')
        driver_elements = document.select('a.group.focus-visible\\:outline-0')

        for driver_element in driver_elements:
            print("")
            names = driver_element.select('.f1-driver-name p')
            full_name = names[0].text.strip() + ' ' + names[1].text.strip()

            driver_link ='https://www.formula1.com' + driver_element['href']
            print(full_name)
            print(driver_link)
            print("")
            
            
            driver_response = requests.get(driver_link)
            driver_response.raise_for_status()
            driver_html = driver_response.text
            driver_document = BeautifulSoup(driver_html, 'html.parser')
        
            driver_images = [img['src'] for img in driver_document.select('.f1-c-image')]
            driver_picture = driver_images[0] if len(driver_images) > 0 else ''
            driver_helmet = driver_images[1] if len(driver_images) > 1 else ''

            driver_bio = driver_document.select_one('.f1-atomic-wysiwyg').text.strip() if driver_document.select_one('.f1-atomic-wysiwyg') else None
            
            driver_data = driver_document.select_one('.f1-dl') if driver_document.select_one('.f1-dl') else None

            driver_info = {
                "bio":driver_bio
            }
            keys = [k.text.strip().lower().replace(' ', '_') for k in driver_data.select('.f1-heading') ] if driver_data else ['no_data']
            values = [v.text.strip() for v in driver_data.select('.f1-text')] if driver_data else ['no_data']

            for i in range(len(keys)):
                driver_info[keys[i]] = values[i]
            
            all_images = []
            journalist_articles = driver_document.select('div.grid.gap-normal.auto-rows-fr.f1-grid')
            articles_photos = journalist_articles[0].select('img')
            if len(articles_photos) > 0:
                for img in articles_photos: 
                    all_images.append(img['src'].replace(' ', '%20'))
                
            caroussel_div = driver_document.select('div.f1-carousel__slide')
            if len(caroussel_div) > 0:
                for div in caroussel_div:   
                    all_images.append(div.select('img')[0]['src'].replace(' ', '%20'))


            drivers.append({
                "id": full_name.lower().replace(" ", "_"),
                'name': full_name,
                'picture': driver_picture,
                'helmet': driver_helmet,
                'info': driver_info,
                'images': all_images
            })
        
        return drivers

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

drivers = scrape_drivers()

pprint(drivers)
