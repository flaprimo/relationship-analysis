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

    @staticmethod
    def parse_chat_file(tree):
        chat_history_root = tree.xpath('/html/body/div[@class="page_wrap"]/div/div[@class="history"]')[0]
        m_media_xpath = './a[contains(@class, "{0}")]'

        message_list = []
        for m in chat_history_root.xpath('./div[contains(@class, "message") and not(contains(@class, "service"))]'):
            m_body = m.xpath('./div[@class="body"]')[0]

            # parse html message
            message = {
                'id': m.xpath('./@id')[0].replace('message', ''),
                'user': re.search(r'^(?P<user>.*?)( via @(?P<bot>[a-zA-Z0-9_-]+))?$',
                                  m_body.xpath('./div[@class="from_name"]/text()')[0]
                                  .strip()).group('user')
                if len(m_body.xpath('./div[@class="from_name"]')) > 0 else message_list[-1]['user'],
                'date': datetime.strptime(m_body.xpath('./div[contains(@class, "date")]/@title')[0],
                                          '%d.%m.%Y %H:%M:%S'),
                'text': next(iter(m_body.xpath('./div[@class="text"]/text()')), '').strip(),
                'links': [link for link in m_body.xpath('./div[@class="text"]/a/@href')],
                'reply': re.search(r'([0-9]+)$', m_body.xpath('./div[contains(@class, "reply_to")]/a/@href')[0])[0]
                if len(m_body.xpath('./div[contains(@class, "reply_to")]')) > 0 else None
            }

            # check for media
            m_media = next(iter(m_body.xpath('./div[contains(@class, "media_wrap")]')), None)
            if m_media is not None:
                message['video'] = len(m_media.xpath(m_media_xpath.format('media_video'))) > 0
                message['image'] = next(iter(m_media.xpath(m_media_xpath.format('photo_wrap') + '/@href')), None)
                message['audio'] = next(iter(m_media.xpath(m_media_xpath.format('media_voice_message') +
                                                           '/@href')), None)
                message['location'] = tuple(
                    re.findall(r'([0-9]+\.[0-9]+)',
                               m_media.xpath(m_media_xpath.format('media_location') +
                                             '/div[@class="body"]/div[contains(@class, "details")]/text()')[0]))\
                    if len(m_media.xpath(m_media_xpath.format('media_location'))) > 0 else None

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
