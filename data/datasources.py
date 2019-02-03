from data.files import Files
from data.calls import Calls
from data.telegram import Telegram
from data.whatsapp import Whatsapp


class Datasources:
    def __init__(self, input_path, output_path):
        self.files = Files(output_path)
        self.telegram = Telegram(input_path)
        self.whatsapp = Whatsapp(input_path)
        self.calls = Calls(input_path)
