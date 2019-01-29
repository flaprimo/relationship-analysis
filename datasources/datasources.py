from datasources.calls import Calls
from datasources.telegram import Telegram
from datasources.whatsapp import Whatsapp


class Datasources:
    def __init__(self, input_path):
        self.telegram = Telegram(input_path)
        self.whatsapp = Whatsapp(input_path)
        self.calls = Calls(input_path)
