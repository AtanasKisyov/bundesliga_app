import requests
import json


class API:

    HOST = 'https://api.openligadb.de/'
    MATCH_DATA_SUFFIX = 'getmatchdata/'
    TABLE_SUFFIX = 'getbltable/'
    BUNDESLIGA_ID = 'bl1/'
    SEASON = '2021/'
    URL = HOST + BUNDESLIGA_ID + SEASON

    def get_all_matches(self):
        url = self.HOST + self.MATCH_DATA_SUFFIX + self.BUNDESLIGA_ID + self.SEASON
        matches = requests.get(url)
        return json.loads(matches.content)

    def get_table(self):
        url = self.HOST + self.TABLE_SUFFIX + self.BUNDESLIGA_ID + self.SEASON
        table = requests.get(url)
        return json.loads(table.content)
