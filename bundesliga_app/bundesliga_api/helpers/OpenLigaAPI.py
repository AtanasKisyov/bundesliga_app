import requests
import json


class API:

    HOST = 'https://api.openligadb.de/'
    MATCH_DATA_SUFFIX = 'getmatchdata/'
    TABLE_SUFFIX = 'getbltable/'
    TEAMS_SUFFIX = 'getavailableteams/'
    MATCHES_BY_TEAM_SUFFIX = 'getmatchesbyteamid/'
    BUNDESLIGA_ID = 'bl1/'
    SEASON = '2022/'
    URL = HOST + BUNDESLIGA_ID + SEASON

    def get_all_matches(self, team=''):
        url = self.HOST + self.MATCH_DATA_SUFFIX + self.BUNDESLIGA_ID + self.SEASON + team
        matches = requests.get(url)
        return json.loads(matches.content)

    def get_matchday(self, matchday_key):
        url = self.HOST + self.MATCH_DATA_SUFFIX + self.BUNDESLIGA_ID + self.SEASON + str(matchday_key)
        matches = requests.get(url)
        return json.loads(matches.content)

    def get_table(self):
        url = self.HOST + self.TABLE_SUFFIX + self.BUNDESLIGA_ID + self.SEASON
        table = requests.get(url)
        return json.loads(table.content)

    def get_team_names(self):
        url = self.HOST + self.TEAMS_SUFFIX + self.BUNDESLIGA_ID + self.SEASON
        response = requests.get(url)
        return json.loads(response.content)

    def get_team_last_five_matches_and_next_match(self, team_id):
        last_five_parameter = '/5'
        next_match_parameter = '/1'
        url = self.HOST + self.MATCHES_BY_TEAM_SUFFIX + str(team_id) + last_five_parameter + next_match_parameter
        response = requests.get(url)
        return json.loads(response.content)
