import pandas as pd
import json
import logging
import helper

logger = logging.getLogger(__name__)


class PipelineIO:
    @staticmethod
    def __read_files(io_format):
        def read_pandas(path, kwargs):
            return pd.read_csv(path, **kwargs)

        def read_json(path):
            with open(path) as json_file:
                json_content = json.load(json_file)
            return json_content

        io_values = {}
        for o_name, o_format in io_format.items():
            if o_format['type'] == 'pandas':
                io_values[o_name] = read_pandas(o_format['path'], o_format['r_kwargs'])

            elif o_format['type'] == 'json':
                io_values[o_name] = read_json(o_format['path'])

            else:
                raise ValueError('error: unknown file type')

        return io_values

    @staticmethod
    def __write_files(io_format, io_values):
        def write_pandas(df, path, kwargs):
            df.to_csv(path, **kwargs)

        def write_json(json_content, path):
            with open(path, 'w') as json_file:
                json.dump(json_content, json_file, indent=4)

        debug_output = ''
        for o_name, o_value in io_values.items():
            o_format = io_format[o_name]

            if o_format['type'] == 'pandas':
                write_pandas(o_value, o_format['path'], o_format['w_kwargs'])
                o_debug = helper.df_tostring(o_value, 5)

            elif o_format['type'] == 'json':
                write_json(o_value, o_format['path'])
                o_debug = 'json file'

            else:
                raise ValueError('error: unknown file type')

            debug_output += f'{o_name} file path: {o_format["path"]}\n' + o_debug

        return debug_output

    @staticmethod
    def load_input(stage_input_expected, stage_input, input_format=None):
        logger.info('load input')

        # if all inputs already present in memory -> return input
        if stage_input is not None and \
                isinstance(stage_input, dict) and \
                all(i in stage_input for i in stage_input_expected):
            logger.debug('input present')
            return stage_input
        # if some input not present in memory -> load input from disk
        else:
            logger.debug('input not present, loading input')
            filtered_input_format = {k: v for k, v in input_format.items() if k in stage_input_expected}
            return PipelineIO.__read_files(filtered_input_format)

    @staticmethod
    def load_output(output_format):
        logger.info('load output')
        output = {}
        try:
            output = PipelineIO.__read_files(output_format)
            logger.debug('output present, not executing stage')
        except IOError as e:
            logger.debug(f'output not present, executing stage: {e}')
        except ValueError as e:
            logger.error(f'wrong output format, executing stage: {e}')

        return output

    @staticmethod
    def save_output(output, output_format):
        logger.info('save output')
        logger.debug(PipelineIO.__write_files(output_format, output))
