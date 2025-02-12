import pandas as pd
from pandas.core.api import DataFrame 
from mailer import notify
from models import Competition, EmailSubscriber
import requests

def fetch_competitions(api_url: str):
    """
    Norske konkurranser: "https://www.worldcubeassociation.org/api/v0/competitions?country_iso2=NO"
    """
    competitions = []
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        competitions = response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching competitions: {e}')
        exit()

    return competitions

if __name__ == "__main__":
    SUBSCRIBER_DB = "./data/subscribers.xlsx"
    COMPETITION_DB = './data/competitions.xlsx'
    API_URL = 'https://www.worldcubeassociation.org/api/v0/competitions?country_iso2=NO'

    competitions = [Competition.from_api_response(competition) for competition in fetch_competitions(API_URL)]
    stored_competitions: list[Competition] = [Competition.from_series(row[1]) for row in pd.read_excel(COMPETITION_DB).iterrows()]
    email_subscribers: list[EmailSubscriber] = [EmailSubscriber.from_series(row[1]) for row in pd.read_excel(SUBSCRIBER_DB).iterrows()]

    for competition in competitions:
        # Break if competition is already handled
        if competition in stored_competitions:
            continue
        for person in email_subscribers:
            notify(person, competition)

    competitions_df = DataFrame(competitions)
    competitions_df.to_excel(COMPETITION_DB)
