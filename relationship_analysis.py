import os
from datasources.telegram import Telegram

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
INPUT_PATH = os.path.join(PROJECT_PATH, 'input/')
OUTPUT_PATH = os.path.join(PROJECT_PATH, 'output/')


def main():
    Telegram(INPUT_PATH)


if __name__ == "__main__":
    main()
