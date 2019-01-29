import logging
import helper
import pandas as pd
from datasources import PipelineIO

logger = logging.getLogger(__name__)


class CreateDataframes():
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
            }
        }
        self.output = PipelineIO.load_output(self.output_format)
        logger.info(f'INIT for {self.config.pipeline_name}-{self.output_prefix}')

    def execute(self):
        logger.info(f'EXEC for {self.config.pipeline_name}-{self.output_prefix}')

        if self.config.skip_output_check or not self.output:
            self.output['calls'] = self.__create_calls_df(self.config.datasources.calls)

            if self.config.save_io_output:
                PipelineIO.save_output(self.output, self.output_format)

        logger.info(f'END for {self.config.pipeline_name}-{self.output_prefix}')

        return self.output, self.output_format

    @staticmethod
    def __create_calls_df(calls):
        logger.info('create calls df')

        calls_df = pd.DataFrame(calls.get_calls_history())

        print(calls_df)

        return calls_df
