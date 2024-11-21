import fastf1
from app.utils.scrapers.scrape_teams import scrape_teams

def load_teams():
    schedule = fastf1.get_event_schedule(2024)
    race = schedule.get_event_by_round(21)
    race_session = race.get_race()
    race_session.load()

    teams = scrape_teams()
    updated_teams = []
    for d in race_session.drivers:
        driver = race_session.get_driver(d)
        driver_team = next((team for team in teams if team['id'] == driver.TeamId or driver.TeamName.lower() in team['name'].lower()), None)

        if 'drivers' not in driver_team:
            driver_team["drivers"] = [{
                "broadcast_name": driver.BroadcastName,
                "full_name": driver.FullName,
                "image": driver.HeadshotUrl,
                "number": driver.DriverNumber,
                "code": driver.Abbreviation,
                "country_code": driver.CountryCode,
            }]
        else:
            driver_team['drivers'].append({
                "broadcast_name": driver.BroadcastName,
                "full_name": driver.FullName,
                "image": driver.HeadshotUrl,
                "number": driver.DriverNumber,
                "code": driver.Abbreviation,
                "country_code": driver.CountryCode,
            })
        updated_teams.append(driver_team)

    return updated_teams