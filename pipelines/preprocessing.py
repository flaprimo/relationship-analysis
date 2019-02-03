import logging
import pandas as pd

logger = logging.getLogger(__name__)


class Preprocessing:
    def __init__(self, datasources):
        self.datasources = datasources
        logger.info(f'INIT for {__name__}')

    def execute(self):
        logger.info(f'EXEC for {__name__}')

        self.__create_dataframes()

        logger.info(f'END for {__name__}')

    def __create_dataframes(self):
        logger.info(self.__create_dataframes.__name__)

        if not self.datasources.files.is_file('preprocessing', 'create_dataframes', 'calls'):
            calls_df = pd.DataFrame(self.datasources.calls.get_calls_history())
            self.datasources.files.write_file('preprocessing', 'create_dataframes', 'calls', calls_df)

        if not self.datasources.files.is_file('preprocessing', 'create_dataframes', 'whatsapp'):
            whatsapp_df = pd.DataFrame(self.datasources.whatsapp.get_chat_history())
            self.datasources.files.write_file('preprocessing', 'create_dataframes', 'whatsapp', whatsapp_df)

        if not self.datasources.files.is_file('preprocessing', 'create_dataframes', 'telegram'):
            telegram_df = pd.DataFrame(self.datasources.telegram.get_chat_history())
            self.datasources.files.write_file('preprocessing', 'create_dataframes', 'telegram', telegram_df)
