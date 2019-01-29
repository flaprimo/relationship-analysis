import os

from datasources import Datasources
from pipelines import preprocessing
import logging
import time

logging.basicConfig(level=logging.DEBUG, filename='logs/debug.log',
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, project_name, input_path, output_path):
        self.project_name = project_name
        self.project_input_path = os.path.join(input_path, project_name + '/')
        self.project_output_path = os.path.join(output_path, project_name + '/')

        self.datasources = Datasources(self.project_input_path)

        logger.info(f'INIT orchestrator')

    def execute(self):
        start_time = time.time()
        logger.info(f'EXEC orchestrator')

        results = self.sequential_exec()

        logger.info(f'END orchestrator')
        logger.debug(f'elapsed time: {round(time.time() - start_time, 4)} s')

        return results

    def sequential_exec(self):
        pp_config = preprocessing.Config(self.project_input_path, self.project_output_path, self.datasources)
        pp = preprocessing.PipelineManager(pp_config, {}, {})
        pp_results = pp.execute()

        results = {
            'preprocessing': pp_results[1],
        }

        return results
