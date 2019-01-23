import os
from lxml import html
from datetime import datetime
import re


class Telegram:
    def __init__(self, input_path):
        self.input_telegram_path = os.path.join(input_path, 'telegram/')

        self.parse_chat_files()

    def get_chat_files(self):
        def get_file_number(file_name):
            re_number = re.findall(r'messages([0-9]*).html', file_name)[0]
            number = int(re_number) if re_number != '' else 0

            return number

        chat_filenames = [f for f in os.listdir(self.input_telegram_path) if f.endswith('.html')]
        chat_filenames.sort(key=lambda x: get_file_number(x))
        chat_files = [os.path.join(self.input_telegram_path, file_name) for file_name in chat_filenames]

        return chat_files

    @staticmethod
    def parse_chat_file(tree):
        chat_history_root = tree.xpath('/html/body/div[@class="page_wrap"]/div/div[@class="history"]')[0]

        last_user = ''
        message_list = []
        for m in chat_history_root.xpath('./div[contains(@class, "message") and not(contains(@class, "service"))]'):
            if 'joined' in m.xpath('./@class')[0].split():
                user = last_user
            else:
                user = m.xpath('./div[@class="body"]/div[@class="from_name"]/text()')[0].splitlines()[1]
                last_user = user
            date = datetime.strptime(m.xpath('./div[@class="body"]/div[contains(@class, "date")]/@title')[0],
                                     '%d.%m.%Y %H:%M:%S')
            message_list.append({'user': user, 'date': date})

        return message_list

    def parse_chat_files(self):
        chat_history = []
        for chat_file in self.get_chat_files():
            with open(chat_file, 'r') as f:
                page = f.read()

            tree = html.fromstring(page)
            chat_parsed = Telegram.parse_chat_file(tree)
            chat_history.extend(chat_parsed)

        print(chat_history)
