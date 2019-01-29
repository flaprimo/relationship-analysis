import logging
from ..pipeline_manager_base import PipelineManagerBase
from .create_dataframes import CreateDataframes

logger = logging.getLogger(__name__)


class PipelineManager(PipelineManagerBase):
    def __init__(self, config, pipeline_input, pipeline_input_format):
        super(PipelineManager, self).__init__(config, pipeline_input, pipeline_input_format)
        logger.info(f'INIT pipeline for {self.config.pipeline_name}')

    def execute(self):
        logger.info(f'EXEC pipeline for {self.config.pipeline_name}')

        cd = CreateDataframes(self.config, self.input, self.input_format)
        cd_output, cd_output_format = cd.execute()

        logger.info(f'END pipeline for {self.config.pipeline_name}')

        return cd_output, cd_output_format
