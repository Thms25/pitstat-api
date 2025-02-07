import fastf1
import datetime
from ...scrapers.scrape_drivers import scrape_drivers
# from pprint import pprint

def load_drivers():
    today_timestamp = datetime.datetime.now()
    today = datetime.date.today()
    year = today.year
    schedule = fastf1.get_event_schedule(year)
    
    drivers = {}
    print("Starting FastF1 driver data load")
    for round in schedule['RoundNumber']:
        print(f"Loading data for round {round}")
        if round == 0:
            continue
        
        event = schedule.get_event_by_round(round)

        if event.EventDate > today_timestamp:
            continue

        race = event.get_race()
        race.load()

        for d in race.results['DriverNumber']:
            race_driver = race.get_driver(d)
            print("race driver:")
            print(race_driver)
            print("")
            code = race_driver.Abbreviation
            if code in drivers:
                drivers[code]['points'] += race_driver.Points
                if drivers[code]['best_race_finish'] > int(race_driver.Position):
                    drivers[code]['best_race_finish'] = int(race_driver.Position)
            else:
                drivers[code] = {
                    'id': race_driver.FullName.lower().replace(" ", "_"),
                    "number": race_driver.DriverNumber,
                    "broadcast_name": race_driver.BroadcastName,
                    'full_name': race_driver.FullName,
                    'code': race_driver.Abbreviation,
                    "points": race_driver.Points,
                    'best_race_finish': int(race_driver.Position),
                    'best_sprint_finish': 25,
                    'team': {
                        'id': race_driver.TeamId,
                        'name': race_driver.TeamName,
                        'color': race_driver.TeamColor,
                    },
                    'images': {
                        'headshot': race_driver.HeadshotUrl,
                    },
                    'country_code': race_driver.CountryCode
                }
        
            if event.EventFormat != 'conventional':
                sprint = event.get_sprint()
                sprint.load()
                sprint_driver = sprint.get_driver(d)
                drivers[code]['points'] += int(sprint_driver.Points)
                if drivers[code]['best_sprint_finish'] > int(sprint_driver.Position):
                    drivers[code]['best_sprint_finish'] = int(sprint_driver.Position)
                    
    drivers_list = list(drivers.values())
    scraped_drivers = scrape_drivers()
    
    if len(drivers_list) == 0:
        return scraped_drivers
    
    for driver in drivers_list:
        for scraped_driver in scraped_drivers:
            if driver['id'] == scraped_driver['id']:
                driver['info'] = scraped_driver['info']
                driver['images']['helmet'] = scraped_driver['helmet']
                driver['images']['picture'] = scraped_driver['picture']
                break
    
    sorted_drivers = sorted(drivers_list, key=lambda x: (-x['points'], x['best_race_finish'], x['best_sprint_finish']))
    return sorted_drivers