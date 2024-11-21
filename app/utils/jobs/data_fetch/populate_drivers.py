import fastf1
import datetime
from pprint import pprint

def load_drivers():
    today_timestamp = datetime.datetime.now()
    today = datetime.date.today()
    year = today.year
    schedule = fastf1.get_event_schedule(year)
    
    drivers = []
    
    for round in schedule['RoundNumber']:
        if round == 0:
            continue
        # if round == 4:
        #     break
        
        event = schedule.get_event_by_round(round)

        if event.EventDate > today_timestamp:
            continue
        

        race = event.get_race()
        race.load()
        print("")
        for d in race.results['DriverNumber']:
            driver = race.get_driver(d)
            if driver.DriverNumber in [d['number'] for d in drivers]:
                driver_index = next((i for i, d in enumerate(drivers) if d['number'] == driver.DriverNumber), None)
                drivers[driver_index]['points'] += driver.Points
            else:
                drivers.append({
                    "number": driver.DriverNumber,
                    "broadcast_name": driver.BroadcastName,
                    'full_name': driver.FullName,
                    'code': driver.Abbreviation,
                    'team': driver.TeamName,
                    "points": driver.Points
                })

    drivers.sort(key=lambda x: x['points'], reverse=True)
    return drivers

drivers = load_drivers()
pprint(drivers)