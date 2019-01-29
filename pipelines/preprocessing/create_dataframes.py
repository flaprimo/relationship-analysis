import logging
import pandas as pd
import re
from datasources import PipelineIO

logger = logging.getLogger(__name__)


class CreateDataframes:
    def __init__(self, config, stage_input=None, stage_input_format=None):
        self.config = config
        self.input = PipelineIO.load_input([], stage_input, stage_input_format)
        self.output_prefix = 'cd'
        self.output_format = {
            'calls': {
                'type': 'pandas',
                'path': self.config.get_path(self.output_prefix, 'calls'),
                'r_kwargs': {
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
                'w_kwargs': {
                    'index': False
                }
            },
            'whatsapp': {
                'type': 'pandas',
                'path': self.config.get_path(self.output_prefix, 'whatsapp'),
                'r_kwargs': {
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
                'w_kwargs': {
                    'index': False
                }
            },
            'telegram': {
                'type': 'pandas',
                'path': self.config.get_path(self.output_prefix, 'telegram'),
                'r_kwargs': {
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
                'w_kwargs': {
                    'index': False
                }
            }
        }
        self.output = PipelineIO.load_output(self.output_format)
        logger.info(f'INIT for {self.config.pipeline_name}-{self.output_prefix}')

    def execute(self):
        logger.info(f'EXEC for {self.config.pipeline_name}-{self.output_prefix}')

        if self.config.skip_output_check or not self.output:
            self.output['calls'] = self.__create_calls_df(self.config.datasources.calls)
            self.output['whatsapp'] = self.__create_whatsapp_df(self.config.datasources.whatsapp)
            self.output['telegram'] = self.__create_telegram_df(self.config.datasources.telegram)

            if self.config.save_io_output:
                PipelineIO.save_output(self.output, self.output_format)

        logger.info(f'END for {self.config.pipeline_name}-{self.output_prefix}')

        return self.output, self.output_format

    @staticmethod
    def __create_calls_df(calls):
        logger.info('create calls df')

        calls_df = pd.DataFrame(calls.get_calls_history())

        return calls_df

    @staticmethod
    def __create_whatsapp_df(whatsapp):
        logger.info('create whatsapp df')

        whatsapp_df = pd.DataFrame(whatsapp.get_chat_history())

        return whatsapp_df

    @staticmethod
    def __create_telegram_df(telegram):
        logger.info('create telegram df')

        telegram_df = pd.DataFrame(telegram.get_chat_history())

        return telegram_df
