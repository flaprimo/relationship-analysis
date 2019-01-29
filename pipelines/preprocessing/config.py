from ..config_base import ConfigBase


class Config(ConfigBase):
    def __init__(self, project_input_path, project_output_path, datasources):
        super(Config, self).__init__('preprocessing', project_input_path, project_output_path, datasources)
