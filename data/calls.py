import csv
import os
from datetime import datetime, timedelta
import re


class Calls:
    def __init__(self, input_path):
        self.input_calls_path = os.path.join(input_path, 'calls/')

    def get_chat_files(self):
        chat_filenames = [f for f in os.listdir(self.input_calls_path) if f.endswith('.csv')]
        chat_files = [os.path.join(self.input_calls_path, file_name) for file_name in chat_filenames]

        return chat_files

    @staticmethod
    def parse_calls_file(calls_csv):
        def parse_dates(date_str):
            months = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic']
            date = re.search(
                r'^(?P<day>[0-9]{2}) (?P<month>[a-z]{3}) (?P<year>[0-9]{4}) (?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})$',
                date_str)

            return datetime(year=int(date.group('year')), month=months.index(date.group('month'))+1,
                            day=int(date.group('day')), hour=int(date.group('hour')), minute=int(date.group('minute')))

        calls_list = []
        next(calls_csv)  # skip first row
        for row in calls_csv:
            call = {
                'user': row[0] if row[5] == 'Outgoing' else 'Flavio Primo',
                'date': parse_dates(row[2]),
                'duration': timedelta(seconds=int(row[4]))
            }

            calls_list.append(call)

        return calls_list

    def get_calls_history(self):
        calls_history = []
        for calls_file_path in self.get_chat_files():
            with open(calls_file_path, 'r') as calls_file:
                calls_csv = csv.reader(calls_file, delimiter=';')

                calls_history.extend(self.parse_calls_file(calls_csv))

        return calls_history
