from bs4 import BeautifulSoup
import requests
from transform_tools import *

def scrape_tournament(year:str):
    URL = f'https://www.atptour.com/en/scores/results-archive?year={year}'
    HEADERS = {'User-Agent': 'My User Agent 1.0'}
    
    source = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(source.text, 'html.parser')
    
    tournaments_records = soup.find_all("tr", {"class": "tourney-result"})

    # Tournament names, locations and names

    tournament_names = [regex_striper(tournament.a.text) for tournament in tournaments_records]
    tournament_locations = [regex_striper(tournament.span.text) for tournament in tournaments_records]
    tournament_dates = [regex_striper(tournament.span.find_next('span').text) for tournament in tournaments_records]

    # Splitting date into year, month, day
    tournament_years =  [tournament_day.split('.')[0] for tournament_day in tournament_dates]
    tournament_months =  [tournament_day.split('.')[1] for tournament_day in tournament_dates]
    tournament_days = [tournament_day.split('.')[2] for tournament_day in tournament_dates]

    # Tournament categories
    tournament_category = soup.find_all('img', {"alt": "tournament badge"})

    tournament_types = []
    for tournament in tournament_category:
        if '250' in tournament.get('src'):
            tournament_types.append('ATP 250')
        elif '500' in tournament.get('src'):
            tournament_types.append('ATP 500')
        elif '1000' in tournament.get('src'):
            tournament_types.append('Masters 1000')
        elif 'grandslam' in tournament.get('src'):
            tournament_types.append('Grand Slam')
        elif 'nextgen' in tournament.get('src'):
            tournament_types.append('Next Gen Finals')
        elif 'finals' in tournament.get('src'):
            tournament_types.append('ATP Finals')
        elif 'lvr' in tournament.get('src'):
            tournament_types.append('Laver cup')
        else:
            tournament_types.append('Undefined')

    # Tournament Surfaces
    tournament_surfaces = []
    for tournament in tournaments_records:
        string = regex_striper(tournament.div.find_next('div').find_next('div').div.text)[0:7] + ' ' + regex_striper(tournament.div.find_next('div').find_next('div').span.text)
        string = " ".join(string.split())
        tournament_surfaces.append(string)


    # Tournament Winners    
    tournament_singles_winners = []

    for player in tournaments_records:
        player = regex_striper(player.a.find_next('a').find_next('a').find_next('a').text)
        tournament_singles_winners.append(player)

        
    # Creating output dictionary 
    output = {"name": tournament_names, "location": tournament_locations, 
    "full_date": tournament_dates, "year": tournament_years, 
    "month": tournament_months, "day": tournament_days,
    "type": tournament_types, "surface": tournament_surfaces,
    "winner": tournament_singles_winners}
    
    
    # Exporting as csv

    csv_converter(output, 'tournament')
    print('CSV succesfully created.')
    return tournament_names