from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import pytz

@dataclass
class Competition:
    id: str
    name: str
    city: str
    start_date: datetime
    end_date: datetime
    registration_open: datetime
    registration_close: datetime
    competitor_limit: int
    delegates: str
    organizers: str

    @classmethod
    def from_api_response(cls, api_response):
        return cls(
            id = api_response['id'],
            name = api_response['name'],
            city = api_response['city'],
            start_date = datetime.fromisoformat(api_response['start_date'].replace('Z', '+00:00')).replace(tzinfo=None),
            end_date = datetime.fromisoformat(api_response['end_date'].replace('Z', '+00:00')).replace(tzinfo=None),
            registration_open = datetime.fromisoformat(api_response['registration_open'].replace('Z', '+00:00')).replace(tzinfo=None),
            registration_close = datetime.fromisoformat(api_response['registration_close'].replace('Z', '+00:00')).replace(tzinfo=None),
            competitor_limit = api_response['competitor_limit'],
            delegates = ', '.join([delegate ['name'] for delegate in api_response['delegates']]),
            organizers = ', '.join([organizer['name'] for organizer in api_response['organizers']])
        )

    @classmethod
    def from_series(cls, row: pd.Series):
        return cls(
            id = str(row['id']),
            name = str(row['name']),
            city = str(row['city']),
            start_date = row['start_date'],
            end_date = row['end_date'],
            registration_open = row['registration_open'],
            registration_close = row['registration_close'],
            competitor_limit = int(row['competitor_limit']),
            delegates = str(row['delegates']),
            organizers = str(row['organizers'])
        )

    def __eq__(self, other):
        return self.id == other.id

    def format_dates(self) -> str:
        if self.start_date == self.end_date:
            return self.start_date.strftime("%b %d, %Y")

        if self.start_date.year == self.end_date.year and self.start_date.month == self.end_date.month:
            return f"{self.start_date.strftime('%b %d')} - {self.end_date.strftime('%d, %Y')}"
        else:
            return f"{self.start_date.strftime('%b %d, %Y')} - {self.end_date.strftime('%b %d, %Y')}"

    def list_officials(self):
        return f'{self.organizers}, {self.delegates}'

    def registration_open_with_timezone(self, timezone: str) -> datetime:
        tz = pytz.timezone(timezone)
        return self.registration_open.replace(tzinfo=pytz.utc).astimezone(tz)

    def registration_close_with_timezone(self, timezone: str) -> datetime:
        tz = pytz.timezone(timezone)
        return self.registration_close.replace(tzinfo=pytz.utc).astimezone(tz)

@dataclass
class EmailSubscriber:
    email: str
    name: str
    last_name: str 
    wca_id: str | None

    @classmethod
    def from_series(cls, row: pd.Series):
        return cls(
            email=str(row['email']),
            name=str(row['name']),
            last_name=str(row['last_name']),
            wca_id=str(row['wca_id']) if pd.notna(row['wca_id']) else None
        )
