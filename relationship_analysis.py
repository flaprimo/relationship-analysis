import os
from datasources.telegram import Telegram
from datasources.whatsapp import Whatsapp
from datasources.calls import Calls

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
INPUT_PATH = os.path.join(PROJECT_PATH, 'input/')
OUTPUT_PATH = os.path.join(PROJECT_PATH, 'output/')


def main():
    print(Telegram(INPUT_PATH).get_chat_history())
    print(Whatsapp(INPUT_PATH).get_chat_history())
    print(Calls(INPUT_PATH).get_calls_history())


if __name__ == "__main__":
    main()
