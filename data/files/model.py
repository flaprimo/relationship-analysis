import pandas as pd
import re

file_models = [
    (
        'preprocessing',
        'create_dataframes',
        'calls',
        'csv',
        {
            'dtype': {
                'name': str,
                'date': str
            },
            'parse_dates': ['date'],
            'index_col': 'date',
            'converters': {
                'duration': pd.to_timedelta
            }
        },
        {
            'index': False
        }
    ),
    (
        'preprocessing',
        'create_dataframes',
        'telegram',
        'csv',
        {
            'dtype': {
                'id': 'uint16',
                'user': str,
                'date': str,
                'text': str,
                'image': str,
                'reply': 'uint16',
                'video': bool
            },
            'parse_dates': ['date'],
            'index_col': 'date',
            'converters': {
                'links': lambda x: x.strip('[]').replace('\'', '').split(', '),
                'location': lambda x: tuple(re.findall(r'([0-9]+\.[0-9]+)', x))
            }
        },
        {
            'index': False
        }
    ),
    (
        'preprocessing',
        'create_dataframes',
        'whatsapp',
        'csv',
        {
            'dtype': {
                'user': str,
                'date': str,
                'media': bool,
                'text': str
            },
            'parse_dates': ['date'],
            'index_col': 'date',
            'converters': {
                'links': lambda x: x.strip('[]').replace('\'', '').split(', ')
            }
        },
        {
            'index': False
        }
    )
]
