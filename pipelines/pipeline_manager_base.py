class PipelineManagerBase:
    def __init__(self, config, pipeline_input, pipeline_input_format):
        self.config = config
        self.input = pipeline_input
        self.input_format = pipeline_input_format

    def execute(self):
        pass
