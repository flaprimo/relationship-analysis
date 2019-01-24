import os
from datetime import datetime
import re


class Whatsapp:
    def __init__(self, input_path):
        self.input_whatsapp_path = os.path.join(input_path, 'whatsapp/')

    def get_chat_files(self):
        chat_filenames = [f for f in os.listdir(self.input_whatsapp_path) if f.endswith('.txt')]
        chat_files = [os.path.join(self.input_whatsapp_path, file_name) for file_name in chat_filenames]

        return chat_files

    @staticmethod
    def parse_chat_file(chat_file_name):
        message_list = []
        with open(chat_file_name, 'r') as chat_file:
            next(chat_file)  # skip first row
            for line in chat_file:
                message_start = re.search(
                    r'^(?P<date>[0-9]{2}\/[0-9]{2}\/[0-9]{2}, [0-9]{2}:[0-9]{2}) - (?P<user>.*?): (?P<text>.*?)$', line)

                if message_start:
                    message = {
                        'date': datetime.strptime(message_start.group('date'), '%d/%m/%y, %H:%M'),
                        'user': message_start.group('user'),
                        'text': message_start.group('text'),
                        'media': message_start.group('text') == '<Media omessi>',
                        'links': [link[0] for link in re.findall(
                            r'(^(http|https):\/\/[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(([0-9]{1,5})?\/.*)?$)',
                            message_start.group('text'))]
                    }
                    message_list.append(message)
                else:
                    message_list[-1]['text'] = message_list[-1]['text'] + ' ' + line.strip()

        return message_list

    def get_chat_history(self):
        chat_history = []
        for chat_file in self.get_chat_files():
            chat_history.extend(self.parse_chat_file(chat_file))

        return chat_history
