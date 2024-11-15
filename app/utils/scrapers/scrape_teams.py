import requests
from bs4 import BeautifulSoup
from pprint import pprint

def scrape_teams():
    url = "https://www.formula1.com/en/teams"
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        document = BeautifulSoup(html, 'html.parser')

        teams = []

        team_elements = document.select('.f1-driver-listing-card')

        for team_element in team_elements:
            team_name = team_element.select_one('.f1-heading').text.strip() if team_element.select_one('.f1-heading') else None
            team_link = f"https://www.formula1.com/en/teams/{team_name}".replace(' ', '-').lower()
            team_images = [img['src'] for img in team_element.select('.f1-c-image')]
            
            # pprint(team_images)
            
            team_logo = next((img for img in team_images if "logo.png" in img), None)
            team_car = next((img for img in team_images if "_team_car_" in img), None)


            # team_response = requests.get(team_link)
            # team_response.raise_for_status()
            # team_html = response.text
            # team_document = BeautifulSoup(team_html, 'html.parser')   
            
            # table = team_document.select_one('.f1-dl')
            # pprint(table)
        
            
            # images = [img['src'] for img in team_document.select('img')]
            # pprint(images)
            
            teams.append({
                "id": team_name.lower().replace(" ", "_"),
                'name': team_name,
                'logo': team_logo,
                'car': team_car,
            })
        return teams

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# teams = scrape_teams()

# pprint(teams)
