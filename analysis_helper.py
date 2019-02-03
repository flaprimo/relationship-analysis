from data import Files
import pandas as pd


class AnalysisHelper:
    """
    Helper class that supports analysis results in Jupyter Notebooks.
    """

    @staticmethod
    def load_ds_results(pipeline_outputs, ds_results):
        """Returns the desired pipeline outputs for a dataset.

        :param pipeline_outputs: dictionary which specifies the desired results names.

        At the first level of the dictionary are the pipeline stage names and
        at the second level, are a list of the desired output names.

        example:
        {
            'pipeline_name': ['output1', ...],
            ...
        }
        :param ds_results: single dataset output format that is returned after a pipeline execution.
        :return: dictionary with the desired results for a single dataset.

        At the first level of the dictionary are the pipeline stage names and
        at the second level, are a the desired output names together with the actual results.

        example:
        {
            'pipeline_name1': {
                'output_name1': {},
                ...
            },
            ...
        }
        """
        res = {}
        for pipeline_name, output_name_list in pipeline_outputs.items():
            res[pipeline_name] = Files.load_input(output_name_list, None, ds_results[pipeline_name])

        return res

    @staticmethod
    def load_all_results(pipeline_outputs, results):
        """Returns the desired pipeline outputs for all datesets.

        :param pipeline_outputs: dictionary which specifies the desired results names.

        At the first level of the dictionary are the pipeline stage names and
        at the second level, are a list of the desired output names.

        example:
        {
            'pipeline_name1': ['output_name1', ...],
            ...
        }
        :param results: output format that is returned after a pipeline execution.
        :return: dictionary with the desired results from all datasets.

        At the first level of the dictionary are the dataset names,
        at the second level are the pipeline stage names and
        at the third level, are a the desired output names together with the actual results.

        example:
        {
            'dataset_name1': {
                'pipeline_name1': {
                    'output_name1': {},
                    ...
                },
                ...
            },
            ...
        }
        """
        res = {}
        for ds_name, ds in results.items():
            res[ds_name] = AnalysisHelper.load_ds_results(pipeline_outputs, ds)

        return res

    @staticmethod
    def get_single_summary(pipeline_name, output_name, results):
        """Returns a merged summary of metrics for a desired output result.

        :param pipeline_name: name of the pipeline to which the desired output belongs to.
        :param output_name: name of the output to which the desired output belongs to.
        :param results: output format that is returned after a pipeline execution.
        :return: pandas dataframe.
        """

        # get results of interest
        filtered_results = AnalysisHelper.load_all_results({pipeline_name: [output_name]}, results)

        # set column 'name'
        for ds_name, ds in filtered_results.items():
            ds[pipeline_name][output_name]['name'] = ds_name

        # merge results in a single dataframe
        merge_results = pd.concat([ds[pipeline_name][output_name] for ds_name, ds in filtered_results.items()],
                                  sort=True).set_index('name')

        return merge_results
