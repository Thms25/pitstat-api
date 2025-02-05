import fastf1
from app.utils.scrapers.scrape_teams import scrape_teams

# from pprint import pprint

def load_teams():
    try:
        schedule = fastf1.get_event_schedule(2024)
        race = schedule.get_event_by_round(20)
        race_session = race.get_race()
        race_session.load()

        scraped_teams = scrape_teams()

        teams = {}
        for number in race_session.drivers:
            driver = race_session.get_driver(number)
            if driver.TeamId not in teams:
                teams[driver.TeamId] = {
                    'id': driver.TeamId,
                    'name': driver.TeamName,
                    'color': driver.TeamColor,
                    'drivers': [{
                        'id': driver.FullName.lower().replace(" ", "_"),
                        'full_name': driver.FullName,
                        "number": driver.DriverNumber,
                        "broadcast_name": driver.BroadcastName,
                        'code': driver.Abbreviation,
                        'country_code': driver.CountryCode
                    }],
                }
            else:
                teams[driver.TeamId]['drivers'].append({
                    'id': driver.FullName.lower().replace(" ", "_"),
                    'full_name': driver.FullName,
                    "number": driver.DriverNumber,
                    "broadcast_name": driver.BroadcastName,
                    'code': driver.Abbreviation,
                    'country_code': driver.CountryCode
                })
        
        teams = list(teams.values())
        
        for team in teams:
            scraped_team = next((team for team in scraped_teams if team['name'].lower() in team['name'].lower()), None)
            if scraped_team:
                team['logo'] = scraped_team['logo']
                team['car'] = scraped_team['car']
                
        return teams
    except Exception as e:
        print(f"An error occurred: {e}")
        return []