import os
import logging
import time
from data import Datasources
from pipelines import Preprocessing

logging.basicConfig(level=logging.DEBUG, filename='logs/debug.log',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s')
logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, project_name, input_path, output_path):
        self.project_name = project_name
        self.project_input_path = os.path.join(input_path, project_name)
        self.project_output_path = os.path.join(output_path, project_name)
        self.datasources = Datasources(self.project_input_path, self.project_output_path)

        logger.info(f'INIT {__name__}')

    def execute(self):
        start_time = time.time()
        logger.info(f'EXEC {__name__}')

        pp = Preprocessing(self.datasources)
        pp.execute()

        logger.info(f'END {__name__}')
        logger.debug(f'elapsed time: {round(time.time() - start_time, 4)} s')
