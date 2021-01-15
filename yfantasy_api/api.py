import requests
import sys
import time

from yfantasy_api.auth import AuthenticationService

BASE_URL = 'https://fantasysports.yahooapis.com/fantasy/v2'


class YahooFantasyApi:
    def __init__(self, league_id, game_id='nhl'):
        self.league_id = league_id
        self.game_id = game_id
        self.auth_service = AuthenticationService()
        self.__set_tokens()

    def __set_tokens(self):
        self.access_token = self.auth_service.get_access_token()
        self.refresh_token = self.auth_service.get_refresh_token()
        self.expires_by = self.auth_service.get_expires_by()

    def __check_tokens(self):
        if time.time() > self.expires_by - 300:
            self.auth_service.refresh_tokens()
            self.__set_tokens()

    #############################
    # Yahoo Fantasy Api methods
    #############################
    def __get_resource(self, path):
        self.__check_tokens()
        params = {'format': 'json'}
        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        url = '{}/{}'.format(BASE_URL, path)

        time.sleep(1)

        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()['fantasy_content']
        else:
            print(response.status_code, response.text)
            sys.exit()

    def __get(self, resource, key, sub_resource, with_metadata):
        path = f'{resource}/{key}/{sub_resource}'
        response = self.__get_resource(path)[resource]
        if with_metadata:
            return response[0], response[1][sub_resource]
        else:
            return response[1][sub_resource]

    def __get_user_resource(self, sub_resource, with_metadata):
        return self.__get_resource(f'users;use_login=1/{sub_resource}')['users']

    def __get_game_resource(self, sub_resource, with_metadata):
        game_key = f'{self.game_id}'
        return self.__get('game', game_key, sub_resource, with_metadata)

    def __get_league_resource(self, sub_resource, with_metadata):
        league_key = f'{self.game_id}.l.{self.league_id}'
        return self.__get('league', league_key, sub_resource, with_metadata)

    def __get_team_resource(self, sub_resource, team_id, with_metadata):
        team_key = f'{self.game_id}.l.{self.league_id}.t.{team_id}'
        return self.__get('team', team_key, sub_resource, with_metadata)

    #############################
    # Public facing Api methods
    #############################
    def get_user_teams(self, with_metadata=False):
        return self.__get_user_resource('teams', with_metadata)

    def get_game_weeks(self, with_metadata=False):
        return self.__get_game_resource('game_weeks', with_metadata)

    def get_stat_categories(self, with_metadata=False):
        return self.__get_game_resource('stat_categories', with_metadata)

    def get_position_types(self, with_metadata=False):
        return self.__get_game_resource('position_types', with_metadata)

    def get_roster_positions(self, with_metadata=False):
        return self.__get_game_resource('roster_positions', with_metadata)

    def get_league_settings(self, with_metadata=False):
        return self.__get_league_resource('settings', with_metadata)

    def get_league_standings(self, with_metadata=False):
        return self.__get_league_resource('standings', with_metadata)

    def get_league_scoreboard(self, week, with_metadata=False):
        return self.__get_league_resource(f'scoreboard;week={week}', with_metadata)

    def get_league_teams(self, with_metadata=False):
        return self.__get_league_resource('teams', with_metadata)

    def get_roster(self, team_id, with_metadata=False):
        return self.__get_team_resource('roster', team_id, with_metadata)

    def get_league_players(self, start, with_metadata=False):
        return self.__get_league_resource(f'players;start={start};type=season/ownership', with_metadata)

    def get_league_keepers(self, start, with_metadata=False):
        return self.__get_league_resource(f'players;start={start};status=K', with_metadata)

    def get_league_draft_results(self, with_metadata=False):
        return self.__get_league_resource('draftresults', with_metadata)

    def get_leage_transactions(self, with_metadata=False):
        return self.__get_league_resource('transactions', with_metadata)

    def get_team_matchups(self, team_id, weeks_arr, with_metadata=False):
        weeks = ','.join(str(c) for c in weeks_arr)
        return self.__get_team_resource(f'matchups;weeks{weeks}', team_id, with_metadata)

    def get_team_stats(self, team_id, date, week, with_metadata=False):
        if not date and not week:
            return None
        elif week:
            time_filter = f'type=week;week={week}'
        else:
            time_filter = f'type=date;date={date}'
        return self.__get_team_resource(f'roster;{time_filter}/players/stats', team_id, with_metadata)

    # TODO - Finish updating the rest of the endpoints
    def get_league_player_ownership(self, start, with_metadata=False):
        return self.__get_league_resource(f'players;start={start};type=season/ownership', with_metadata)

    def get_league_player_stats(self, start, date, with_metadata=False):
        return self.__get_league_resource(f'players;start={start};out=ownership/stats;type=date;date={date}', with_metadata)

    def get_stats_players_season(self, start, with_metadata=False):
        return self.__get_league_resource('players;start={};sort=AR/stats;type=season;season=2020'.format(start),
                                          with_metadata)
