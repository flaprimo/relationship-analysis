import os


class ConfigBase:
    def __init__(self, pipeline_name, project_input_path, project_output_path, datasources,
                 skip_output_check=False, save_io_output=True, save_db_output=True):
        self.pipeline_name = pipeline_name

        self.base_dir = {
            'input': project_input_path,
            'output': os.path.join(project_output_path, pipeline_name + '/')
        }

        self.postfix = ''
        self.datasources = datasources

        self.skip_output_check = skip_output_check
        self.save_io_output = save_io_output
        self.save_db_output = save_db_output

    def get_path(self, stage_name, file_name, file_type='csv'):
        directory = os.path.join(self.base_dir['output'], stage_name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        return f'{directory}/{file_name}{self.postfix}.{file_type}'
