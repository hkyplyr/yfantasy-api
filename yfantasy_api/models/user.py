from yfantasy_api.models.common import Team
from yfantasy_api.models.game import Game
from yfantasy_api.models.league import League


class User:
    def __init__(self, json):
        self.json = json
        self.guid = json[0]['guid']
        self.__parse_sub_resources(json)

    def __parse_sub_resources(self, json):
        for data in json:
            if 'games' in data:
                self.__parse_games(data['games'])
            if 'teams' in data:
                self.__parse_teams(data['teams'])

    def __parse_games(self, json):
        self.games = [Game(json[str(d)]['game']) for d in range(json['count'])]

    def __parse_teams(self, json):
        self.teams = [Team(json[str(d)]['team']) for d in range(json['count'])]
