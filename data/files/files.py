import os
import pandas as pd
import json
import logging
from data.files.model import file_models

logger = logging.getLogger(__name__)


class Files:
    def __init__(self, output_path):
        self.output_path = os.path.join(output_path, 'files')
        self.model = {}

        for file_model in file_models:
            self.add_file_model(*file_model)

    def is_file(self, pipeline_name, stage_name, file_name):
        file_model = self.model[pipeline_name][stage_name][file_name]
        file_exists = os.path.isfile(file_model['path'])
        if file_exists:
            logger.debug(f'file exists (file "{file_model["path"]}")')
        else:
            logger.debug(f'file NOT exists (file "{file_model["path"]}")')

        return file_exists

    def add_file_model(self, pipeline_name, stage_name, file_name, file_extension, r_kwargs, w_kwargs):
        path_dir = os.path.join(self.output_path, f'{pipeline_name}/{stage_name}')

        new_file = {
            file_name: {
                'path': os.path.join(path_dir, f'{file_name}.{file_extension}'),
                'path_dir': path_dir,
                'type': file_extension,
                'r_kwargs': r_kwargs,
                'w_kwargs': w_kwargs
            }
        }

        if pipeline_name not in self.model:
            self.model[pipeline_name] = {}
            if stage_name not in self.model[pipeline_name]:
                self.model[pipeline_name][stage_name] = {}

        self.model[pipeline_name][stage_name].update(new_file)

        logger.debug(f'added file model (file "{new_file[file_name]["path"]}")')

    def read_file(self, pipeline_name, stage_name, file_name):
        def read_pandas(file_path, kwargs):
            return pd.read_csv(file_path, **kwargs)

        def read_json(file_path, kwargs):
            with open(file_path) as json_file:
                json_content = json.load(json_file, **kwargs)
            return json_content

        file_model = self.model[pipeline_name][stage_name][file_name]

        if file_model['type'] == 'csv':
            file_content = read_pandas(file_model['path'], file_model['r_kwargs'])
        elif file_model['type'] == 'json':
            file_content = read_json(file_model['path'], file_model['r_kwargs'])
        else:
            raise ValueError('error: unknown file type')

        logger.debug(f'file read (file "{file_model["path"]}")')

        return file_content

    def write_file(self, pipeline_name, stage_name, file_name, file_content):
        def write_pandas(df, file_path, kwargs):
            df.to_csv(file_path, **kwargs)

        def write_json(json_content, file_path, kwargs):
            with open(file_path, 'w') as json_file:
                json.dump(json_content, json_file, **kwargs)

        file_model = self.model[pipeline_name][stage_name][file_name]

        if not os.path.exists(file_model['path_dir']):
            os.makedirs(file_model['path_dir'])

        if file_model['type'] == 'csv':
            write_pandas(file_content, file_model['path'], file_model['w_kwargs'])
        elif file_model['type'] == 'json':
            write_json(file_content, file_model['path'], file_model['w_kwargs'])
        else:
            raise ValueError('error: unknown file type')

        logger.debug(f'file written (file "{file_model["path"]}")')
