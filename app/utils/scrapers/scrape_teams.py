import requests
from bs4 import BeautifulSoup
from pprint import pprint

def scrape_teams():
    url = "https://www.formula1.com"
    try:
        response = requests.get(url + "/en/teams")
        response.raise_for_status()
        html = response.text
        document = BeautifulSoup(html, 'html.parser')

        teams = []
        team_elements = document.select('a.group')
        rank = 1
        for team_element in team_elements:
            team_name = team_element.select_one('.f1-heading').text.strip() if team_element.select_one('.f1-heading') else None
            team_link = url + team_element['href']
            print("")
            print(f"Scraping {team_name}")
            team_images = [img['src'] for img in team_element.select('.f1-c-image')]
            
            team_logo = next((img for img in team_images if "logo.png" in img), None)
            team_car = next((img for img in team_images if "_team_car_" in img), None)
            
            team_response = requests.get(team_link)
            team_response.raise_for_status()
            team_html = team_response.text
            team_document = BeautifulSoup(team_html, 'html.parser')   
            
            teams_table = team_document.select_one('.f1-dl')
            team_info = {}

            keys = [k.text.strip().lower().replace(' ', '_') for k in teams_table.select('dt.f1-heading') ]
            
            values = [v.text for v in teams_table.select('dd.f1-text') ]
            
            for i in range(len(keys)):
                team_info[keys[i]] = values[i]

            drivers_div = [a for a in team_document.select('a') if 'en/drivers/' in a['href']]            
            drivers = []
            for driver in drivers_div:
                driver_picture = driver.select_one('img')['src']
                info = [n.text for n in driver.select('p.f1-heading') ]
                name = info[1]
                number = info[0]

                drivers.append({
                    'name': name,
                    'number': int(number),
                    'picture': driver_picture
                })
            pprint(drivers)

            images = [img['src'] for img in team_document.select('div.f1-carousel__slide img')]
            
            description = team_document.select_one('div.f1-atomic-wysiwyg p.f1-text').text.strip()        
            team_info['description'] = description
            
            teams.append({
                "id": team_name.lower().replace(" ", "_"),
                'name': team_name,
                'points': 0,
                'rank': rank,
                'logo': team_logo,
                'car': team_car,
                'drivers': drivers,
                'images': images,
                'info': team_info
            })
            rank += 1
            print("")
        return teams

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

scrape_teams()
