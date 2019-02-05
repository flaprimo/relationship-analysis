from .files import Files
from .calls import Calls
from .telegram import Telegram
from .whatsapp import Whatsapp


class Datasources:
    def __init__(self, input_path, output_path):
        self.files = Files(output_path)
        self.telegram = Telegram(input_path)
        self.whatsapp = Whatsapp(input_path)
        self.calls = Calls(input_path)
