import os
from lxml import html
from datetime import datetime
import re


class Telegram:
    def __init__(self, input_path):
        self.input_telegram_path = os.path.join(input_path, 'telegram/')

    def get_chat_files(self):
        def get_file_number(file_name):
            re_number = re.search(r'^messages(?P<number>[0-9]*).html', file_name).group('number')
            number = int(re_number) if re_number != '' else 0

            return number

        chat_filenames = [f for f in os.listdir(self.input_telegram_path) if f.endswith('.html')]
        chat_filenames.sort(key=lambda x: get_file_number(x))
        chat_files = [os.path.join(self.input_telegram_path, file_name) for file_name in chat_filenames]

        return chat_files

    def parse_chat_file(self, tree):
        chat_history_root = tree.xpath('/html/body/div[@class="page_wrap"]/div/div[@class="history"]')[0]

        last_user = ''
        message_list = []
        for m in chat_history_root.xpath('./div[contains(@class, "message") and not(contains(@class, "service"))]'):
            # parse html message
            message = {
                'id': m.xpath('./@id')[0].replace('message', ''),
                'user': next(iter(m.xpath('./div[@class="body"]/div[@class="from_name"]/text()')), None),
                'date': datetime.strptime(m.xpath('./div[@class="body"]/div[contains(@class, "date")]/@title')[0],
                                          '%d.%m.%Y %H:%M:%S'),
                'text': next(iter(m.xpath('./div[@class="body"]/div[@class="text"]/text()')), '').strip(),
                'links': [link for link in m.xpath('./div[@class="body"]/div[@class="text"]/a/@href')],
                'image': next(iter(m.xpath('./div[@class="body"]/div[contains(@class, "media_wrap")]/'
                                           'a[contains(@class, "photo_wrap")]/@href')), None),
                # TODO: check support for video
                'video': len(m.xpath('./div[@class="body"]/div[contains(@class, "media_wrap")]/'
                                     'a[contains(@class, "media_video")]/@href')) > 0,
                'audio': next(iter(m.xpath('./div[@class="body"]/div[contains(@class, "media_wrap")]/'
                                           'a[contains(@class, "media_voice_message")]/@href')), None),
                'reply': next(iter(m.xpath('./div[@class="body"]/div[contains(@class, "reply_to")]/a/@href')), None),
            }

            # clean message fields
            # TODO: use regex with xpath 2
            if message['user']:
                # can also match bots selecting the end
                message['user'] = re.search(
                    r'^(?P<user>.*?)( via @(?P<bot>[a-zA-Z0-9_-]+))?$', message['user'].strip()).group('user')
                last_user = message['user']
            else:
                message['user'] = last_user

            if message['image']:
                message['image'] = os.path.join(self.input_telegram_path, message['image'])

            if message['audio']:
                message['audio'] = os.path.join(self.input_telegram_path, message['audio'])

            if message['reply']:
                message['reply'] = re.findall(r'([0-9]+)$', message['reply'])[0]

            message_list.append(message)

        return message_list

    def get_chat_history(self):
        chat_history = []
        for chat_file_path in self.get_chat_files():
            with open(chat_file_path, 'r') as chat_file:
                page = chat_file.read()

            tree = html.fromstring(page)
            chat_history.extend(self.parse_chat_file(tree))

        return chat_history
