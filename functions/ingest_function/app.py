from dotenv import load_dotenv

load_dotenv(override=True)


import structlog
import json

import pandas as pd
import src.utils

from datetime import datetime, timedelta
from unittest.mock import patch

from src.transform import clean_data
from src.load import load_data
from src.schema import APIResponse


logger = structlog.get_logger('__name__')


@patch('src.utils.get_api_response',
       return_value={
            'page': 1,
            'total_pages': 2,
            'data': [
                APIResponse(**record).model_dump()
                for record in (pd.read_csv('data/challenge_dataset.csv')
                               .to_dict(orient='records'))]})
def lambda_handler(event, context, mock_api_response):
    date = event.get('date')
    page = event.get('page', 1)
    if date is not None:
        date = datetime.strptime(date, '%Y-%m-%d')
    else:
        date = datetime.now()

    yesterday_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')

    params = {
        'page': page,
        'filter': json.dumps(
            [{'field': 'date', 'operator': 'ge', 'value': yesterday_date}])
    }
    response = src.utils.get_api_response(
        'https://url.com', params=params, data_schema=APIResponse)

    data = pd.DataFrame.from_records(response['data'])
    cleaned_data = clean_data(data)
    logger.info(f'Cleaned data contains {cleaned_data.shape[0]} rows'
                f' and {cleaned_data.shape[1]} columns.')
    load_data(cleaned_data)

    return {
        'total_pages': response['total_pages'],
        'page': response['page'] + 1
    }
