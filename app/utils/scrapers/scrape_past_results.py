import requests
from bs4 import BeautifulSoup
# from pprint import pprint

url = 'https://www.formula1.com/en/results'
def get_driver_standings(year):
    try:
        response = requests.get(url + f'/{year}/drivers')
        response.raise_for_status()
        html = response.text
        document = BeautifulSoup(html, 'html.parser')
        table = document.select_one('table.f1-table.f1-table-with-data')
        rows = table.select('tr')
        driver_standings = []
        for row in rows[1:]:
            if row.select_one('th'):
                continue
            columns = row.select('td')
            driver_name_code = columns[1].text.strip()
            name_parts = driver_name_code.split('\xa0')
            full_name = name_parts[0] + ' ' + name_parts[-1][:-3]
            code = name_parts[-1][-3:]
            driver_standings.append({
                'position': int(columns[0].text),
                'name': full_name,
                'code': code,
                'nationality': columns[2].text,
                'team': columns[3].text,
                'points': float(columns[4].text)
            })
        return driver_standings
    except Exception as e:
        print(e)
        return []

def get_team_standings(year):
    try:
        response = requests.get(url + f'/{year}/team')
        response.raise_for_status()
        html = response.text
        document = BeautifulSoup(html, 'html.parser')
        table = document.select_one('table.f1-table.f1-table-with-data')
        rows = table.select('tr')
        team_standings = []
        for row in rows[1:]:
            if row.select_one('th'):
                continue
            columns = row.select('td')
            team_standings.append({
                'position': int(columns[0].text),
                'name': columns[1].text,
                'points': float(columns[2].text)
            })
        return team_standings
    except Exception as e:
        print(e)
        return []
    
def get_races_results(year):
    try:
        response = requests.get(url + f'/{year}/races')
        response.raise_for_status()
        html = response.text
        document = BeautifulSoup(html, 'html.parser')
        table = document.select_one('table.f1-table.f1-table-with-data')
        if not table:
            return []
        rows = table.select('tr')
        races = []
        for row in rows[1:]:
            if row.select_one('th'):
                continue
            columns = row.select('td')

            results = []
            results_link = f'https://www.formula1.com/en/results/{year}/' + columns[0].select_one('a')['href']
            results_response = requests.get(results_link)
            results_response.raise_for_status()
            results_html = results_response.text
            results_document = BeautifulSoup(results_html, 'html.parser')
            results_table = results_document.select_one('table.f1-table.f1-table-with-data')
            if results_response.ok and results_table:
                results_rows = results_table.select('tr')
                for result_row in results_rows[1:]:
                    if result_row.select_one('th'):
                        continue
                    result_columns = result_row.select('td')
                    if len(result_columns) < 7:
                        continue
                    
                    name = result_columns[2].text
                    driver_name = name.split('\xa0')[0] + ' ' + name.split('\xa0')[-1][:-3]

                    results.append({
                        'position': result_columns[0].text,
                        'driver': driver_name,
                        'driver_number': int(result_columns[1].text),
                        'driver_code': result_columns[2].text[-3:],
                        'team': result_columns[3].text,
                        'laps': result_columns[4].text,
                        'time': result_columns[5].text,
                        'points': float(result_columns[6].text)
                    })
                
            fastest_laps = []
            fastest_laps_link = results_link.replace("race-result", "fastest-laps")
            fastest_laps_response = requests.get(fastest_laps_link)
            fastest_laps_response.raise_for_status()
            fastest_laps_html = fastest_laps_response.text
            fastest_laps_document = BeautifulSoup(fastest_laps_html, 'html.parser')
            laps_table = fastest_laps_document.select_one('table.f1-table.f1-table-with-data')
            if fastest_laps_response.ok and laps_table:
                laps_rows = laps_table.select('tr')
                for lap_row in laps_rows[1:]:
                    if lap_row.select_one('th'):
                        continue
                    lap_columns = lap_row.select('td')
                    if len(lap_columns) < 4:
                        continue
                    fastest_laps.append({
                        'position': lap_columns[0].text,
                        'driver_number': int(lap_columns[1].text),
                        'driver': lap_columns[2].text.split('\xa0')[0] + ' ' + lap_columns[2].text.split('\xa0')[-1][:-3],
                        'driver_code': lap_columns[2].text[-3:],
                        'team': lap_columns[3].text,
                        'lap': lap_columns[4].text,
                        'time': lap_columns[6].text,
                        'avg_speed': lap_columns[7].text
                    })

            qualifying = []
            qualifying_link = results_link.replace("race-result", "qualifying")
            qualifying_response = requests.get(qualifying_link)
            qualifying_response.raise_for_status()
            qualifying_html = qualifying_response.text
            qualifying_document = BeautifulSoup(qualifying_html, 'html.parser')
            qualifying_table = qualifying_document.select_one('table.f1-table.f1-table-with-data')
            if qualifying_response.ok and qualifying_table:
                qualifying_rows = qualifying_table.select('tr')
                for q_row in qualifying_rows[1:]:
                    if q_row.select_one('th'):
                        continue
                    q_columns = q_row.select('td')
                    if len(q_columns) < 5:
                        continue
                    qualifying.append({
                        'position': q_columns[0].text,
                        'driver_number': int(q_columns[1].text),
                        'driver': q_columns[2].text.split('\xa0')[0] + ' ' + q_columns[2].text.split('\xa0')[-1][:-3],
                        'driver_code': q_columns[2].text[-3:],
                        'team': q_columns[3].text,
                        'q1': q_columns[4].text,
                        'q2': q_columns[5].text,
                        'q3': q_columns[6].text
                    })
                
            races.append({
                'name': columns[0].text,
                'date': columns[1].text,
                'laps': columns[4].text,
                'duration': columns[5].text,
                'race_results': results,
                'qualifying_results': qualifying,
                'fastest_laps': fastest_laps
            })
            print("Successfully got data for ", columns[0].text)
        return races
    except Exception as e:
        print(e)
        return []

def get_past_data(year):
    print("")
    print("Getting data for ", year)
    driver_standings = get_driver_standings(year)
    print("Driver standings successfully fetched")
    constructor_standings = get_team_standings(year)
    print("Constructor standings successfully fetched")
    races = get_races_results(year)
    print("Races data successfully fetched")
    print("")
    return {
        'year': year,
        'driver_standings': driver_standings,
        'constructor_standings': constructor_standings,
        'races_data': races
    }
