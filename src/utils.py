import requests
import structlog

from sqlalchemy import URL


logger = structlog.get_logger('__name__')


def get_api_response(url, params=None, headers=None, data_schema=None):
    response = requests.get(url=url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()
    if data_schema is not None:
        data = [data_schema(**record).model_dump() for record in data]

    return data


def build_db_uri(username, password, port, host, database):
    return URL.create(
        'postgresql',
        username=username,
        password=password,
        port=port,
        host=host,
        database=database,
    ) if all([username, password, port, host, database]) else None
