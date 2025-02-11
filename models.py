from dataclasses import dataclass
from datetime import datetime
import pandas as pd

@dataclass
class Competition:
    id: str
    name: str
    city: str
    start_date: datetime
    registration_open: datetime
    registration_close: datetime
    delegates: str

    @classmethod
    def from_api_response(cls, api_response):
        return cls(
            id = api_response['id'],
            name = api_response['name'],
            city = api_response['city'],
            start_date = datetime.fromisoformat(api_response['start_date'].replace('Z', '+00:00')).replace(tzinfo=None),
            registration_open = datetime.fromisoformat(api_response['registration_open'].replace('Z', '+00:00')).replace(tzinfo=None),
            registration_close = datetime.fromisoformat(api_response['registration_close'].replace('Z', '+00:00')).replace(tzinfo=None),
            delegates = ", ".join([delegate['name'] for delegate in api_response['delegates']])
        )

    @classmethod
    def from_series(cls, row: pd.Series):
        return cls(
            id = str(row["id"]),
            name = str(row["name"]),
            city = str(row["city"]),
            start_date = row["start_date"],
            registration_open = row["registration_open"],
            registration_close = row["registration_close"],
            delegates = str(row["delegates"])
        )

    def __eq__(self, other):
        return self.id == other.id

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
