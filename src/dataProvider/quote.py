import requests
from datetime import datetime
import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../../"


class TiingoProvider:
    def __init__(self, token):
        self.token = token
        self.headers = {'Content-Type': 'application/json'}

    def _getCachedFileName(self, ticker, queryDate):
        queryMonth = queryDate.strftime('%Y-%m')
        return f'{ROOT_DIR}/data/{ticker}-{queryMonth}.json'


    def _adjustSplit(self, data):
        cumulative_split_factor = 1.0
        for entry in reversed(data):
            entry_date = datetime.strptime(entry['date'].split('T')[0], "%Y-%m-%d")
            if entry['splitFactor'] != 1:
                    cumulative_split_factor *= entry['splitFactor']
            else:
                # Adjust the prices of the previous data points
                entry['close'] = entry['close'] / cumulative_split_factor

    def queryDaily(self, ticker):
        ticker = ticker.lower()
        # always query max range
        today = datetime.now()
        cachedFile = self._getCachedFileName(ticker, today)
        if os.path.exists(cachedFile):
            with open(cachedFile, 'r') as f:
                data = json.load(f)
            # read from cached file
        else:
            url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={self.token}&startDate=1990-1-1&endDate={today.strftime("%Y-%m-%d")}'
            requestResponse = requests.get(url, headers=self.headers)
            data = requestResponse.json()
            with open(cachedFile, 'w') as f:
                json.dump(data, f)
        self._adjustSplit(data)
        return data
                

