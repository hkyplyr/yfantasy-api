from yfantasy_api.models.common import Player, Team
from yfantasy_api.models.helpers import flatten_attributes, as_float, as_bool, as_int
from yfantasy_api.models.transaction import Add, AddDrop, Drop, Trade


class League:
    def __init__(self, json):
        attributes = flatten_attributes(json)
        self.key = attributes.get('league_key')
        self.id = as_int(attributes.get('league_id'))
        self.name = attributes.get('name')
        self.url = attributes.get('url')
        self.logo_url = attributes.get('logo_url')
        self.draft_status = attributes.get('draft_status')
        self.num_teams = as_int(attributes.get('num_teams'))
        self.scoring_type = attributes.get('scoring_type')
        self.league_type = attributes.get('league_type')
        self.add_injured_to_ir = as_bool(attributes.get('allow_add_to_dl_extra_pos'))
        self.current_week = as_int(attributes.get('current_week'))
        self.start_week = as_int(attributes.get('start_week'))
        self.start_date = attributes.get('start_date')
        self.end_week = as_int(attributes.get('end_week'))
        self.end_date = attributes.get('end_date')
        self.game_code = attributes.get('game_code')
        self.season = as_int(attributes.get('season'))
        self.__parse_sub_resources(json)
    
    def __repr__(self):
        return str(self.__dict__) # pragma: no cover

    def __parse_sub_resources(self, json):
        for data in json:
            if 'draft_results' in data:
                self.__parse_draft_results(data['draft_results'])
            if 'players' in data:
                self.__parse_players(data['players'])
            if 'scoreboard' in data:
                self.__parse_scoreboard(data['scoreboard'])
            if 'settings' in data:
                self.__parse_settings(data['settings'])
            if 'standings' in data:
                self.__parse_standings(data['standings'])
            if 'teams' in data:
                self.__parse_teams(data['teams'])
            if 'transactions' in data:
                self.__parse_transactions(data['transactions'])

    def __parse_draft_results(self, json):
        self.draft_results = [DraftResult(json[str(d)]['draft_result']) for d in range(json['count'])]

    def __parse_players(self, json):
        self.players = [Player(json[str(d)]['player']) for d in range(json['count'])]

    def __parse_scoreboard(self, json):
        json = json['0']['matchups']
        self.matchups = [Matchup(json[str(d)]['matchup']) for d in range(json['count'])]

    def __parse_settings(self, json):
        self.settings = Settings(json)

    def __parse_standings(self, json):
        json = json[0]['teams']
        self.standings = [Team(json[str(d)]['team']) for d in range(json['count'])]

    def __parse_teams(self, json):
        self.teams = [Team(json[str(d)]['team']) for d in range(json['count'])]

    def __parse_transactions(self, json):
        self.transactions = []

        if not json:
            return

        for t in reversed(range(json['count'])):
            transaction = json[str(t)]['transaction']
            transaction_type = transaction[0]['type']

            if transaction_type == 'add':
                self.transactions.append(Add(transaction))
            elif transaction_type == 'drop':
                self.transactions.append(Drop(transaction))
            elif transaction_type == 'add/drop':
                self.transactions.append(AddDrop(transaction))
            elif transaction_type == 'trade':
                self.transactions.append(Trade(transaction))


class DraftResult:
    def __init__(self, json):
        self.pick = as_int(json['pick'])
        self.round = as_int(json['round'])
        self.team_key = json['team_key']
        self.player = Player(json['0']['players']['0']['player'])
    
    def __repr__(self):
        return str(self.__dict__) # pragma: no cover

class Matchup:
    def __init__(self, json):
        self.week = as_int(json.get('week'))
        self.week_start = json.get('week_start')
        self.week_end = json.get('week_end')
        self.status = json.get('status')
        self.is_current = self.status == 'midevent'
        self.is_playoffs = as_bool(json.get('is_playoffs'))
        self.is_consolation = as_bool(json.get('is_consolation'))
        self.is_tied = as_bool(json.get('is_tied'))
        
        self.__parse_teams(json)

    def __parse_winning_team(self, teams, winning_team_key):
        return next(team for team in teams if team.key == winning_team_key)

    def __parse_losing_team(self, teams, winning_team_key):
        return next(team for team in teams if team.key != winning_team_key)

    def __parse_teams(self, json):
        winning_team_key = json.get('winner_team_key')
        json = json['0']['teams']
        self.teams = [Team(json[str(t)]['team']) for t in range(json['count'])]
        if winning_team_key:
            self.winning_team = self.__parse_winning_team(self.teams, winning_team_key)
            self.losing_team = self.__parse_losing_team(self.teams, winning_team_key)

    def __repr__(self):
        return str(self.__dict__) # pragma: no cover


class Settings:
    def __init__(self, json):
        json = json[0]
        self.draft_type = json.get('draft_type')
        self.is_auction = as_bool(json.get('is_auction_draft'))
        self.scoring_type = json.get('scoring_type')
        self.persistent_url = json.get('persistent_url')
        self.has_playoff = as_bool(json.get('uses_playoff'))
        self.has_consolation = as_bool(json.get('has_playoff_consolation_games'))
        self.playoff_start_week = as_int(json.get('playoff_start_week'))
        self.has_reseeding = as_bool(json.get('uses_playoff_reseeding'))
        self.lock_eliminatd_teams = as_bool(json.get('uses_lock_eliminated_teams'))
        self.num_playoff_teams = as_int(json.get('num_playoff_teams'))
        self.num_consolation_teams = as_int(json.get('num_playoff_consolation_teams'))
        self.has_multiweek_championship = json.get('has_multiweek_championship')
        self.waiver_type = json.get('waiver_type')
        self.waiver_rule = json.get('waiver_rule')
        self.uses_faab = as_bool(json.get('uses_faab'))
        self.seconds_per_pick = as_int(json.get('draft_pick_time'))
        self.post_draft_players = json.get('post_draft_players')
        self.max_teams = as_int(json.get('max_teams'))
        self.days_on_waivers = as_int(json.get('waiver_time'))
        self.trade_end_date = json.get('trade_end_date')
        self.trade_ratify_type = json.get('trade_ratify_type')
        self.days_to_veto = as_int(json.get('trade_reject_time'))
        self.player_pool = json.get('player_pool')
        self.cant_cut_list = json.get('cant_cut_list')
        self.trade_draft_picks = as_bool(json.get('can_trade_draft_picks'))
        self.fractional_points = as_bool(json.get('uses_fractional_points'))
        self.negative_points = as_bool(json.get('uses_negative_points'))
        self.divisions = self.__parse_divisions(json)
        self.roster_positions = self.__parse_roster_positions(json)
        self.stat_categories = self.__parse_stat_categories(json)
    
    def __repr__(self):
        return str(self.__dict__) # pragma: no cover

    def __parse_roster_positions(self, json):
        json = json.get('roster_positions')
        return {
            data['roster_position']['position']: as_int(data['roster_position']['count'])
            for data in json
        }

    def __parse_stat_categories(self, json):
        modifiers = {s['stat']['stat_id']: as_float(s['stat']['value']) for s in json['stat_modifiers']['stats']}
        categories = json['stat_categories']['stats']
        return [Stat(cat['stat'], modifiers) for cat in categories]

    def __parse_divisions(self, json):
        json = json.get('divisions', [])
        return [Division(d['division']) for d in json]


class Division:
    def __init__(self, json):
        self.id = as_int(json['division_id'])
        self.name = json['name']
    
    def __repr__(self):
        return str(self.__dict__) # pragma: no cover

class Stat:
    def __init__(self, category, modifiers):
        self.id = category['stat_id']
        self.name = category['name']
        self.display_name = category['display_name']
        self.value = modifiers.get(self.id)
    
    def __repr__(self):
        return str(self.__dict__) # pragma: no cover
