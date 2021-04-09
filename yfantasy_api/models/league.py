from yfantasy_api.models.common import Player, Team
from yfantasy_api.models.transaction import Add, AddDrop, Drop, Trade


class League:
    def __init__(self, json):
        self.json = json
        self.info = LeagueInfo(json[0])
        self.__parse_sub_resources(json)

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
        self.week = json['week']
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
        self.pick = json['pick']
        self.round = json['round']
        self.team_key = json['team_key']
        self.__parse_player(json)

    def __parse_player(self, json):
        if '0' in json:
            self.player = Player(json['0']['players']['0']['player'])
        else:
            self.player_key = json['player_key']


class Matchup:
    def __init__(self, json):
        self.week = json['week']
        self.week_start = json['week_start']
        self.week_end = json['week_end']
        self.status = json['status']
        self.is_playoffs = json['is_playoffs']
        self.is_consolation = json['is_consolation']
        self.stat_winners = json.get('stat_winners')
        self.is_matchup_recap_available = json.get('is_matchup_recap_available')
        self.matchup_recap_url = json.get('matchup_recap_url')
        self.matchup_recap_title = json.get('matchup_recap_title')
        self.matchup_grades = json.get('matchup_grades')
        self.is_tied = json.get('is_tied')
        self.winner_team_key = json.get('winner_team_key')
        json = json['0']['teams']
        self.teams = [MatchupTeam(json[str(d)]) for d in range(json['count'])]


class MatchupTeam:
    def __init__(self, json):
        json = json['team']
        self.team = Team(json)
        self.team_points = json[1]['team_points']['total']
        self.team_stats = self.__parse_team_stats(json[1].get('team_stats', []))
        self.team_live_projected_points = json[1].get('team_live_projected_points')
        self.team_projected_points = json[1]['team_projected_points']['total']
        self.win_probability = json[1].get('win_probability')
        self.__parse_remaining_games(json[1].get('team_remaining_games', []))

    def __parse_team_stats(self, json):
        if not json:
            return []
        return {d['stat']['stat_id']: d['stat']['value'] for d in json['stats']}

    def __parse_remaining_games(self, json):
        if not json:
            return []
        json = json['total']
        self.remaining_games = json['remaining_games']
        self.live_games = json['live_games']
        self.completed_games = json['completed_games']


class LeagueInfo:
    def __init__(self, json):
        self.league_key = json['league_key']
        self.league_id = json['league_id']
        self.name = json['name']
        self.url = json['url']
        self.logo_url = json['logo_url']
        self.password = json.get('password')
        self.draft_status = json['draft_status']
        self.num_teams = json['num_teams']
        self.edit_key = json['edit_key']
        self.weekly_deadline = json['weekly_deadline']
        self.league_update_timestamp = json['league_update_timestamp']
        self.scoring_type = json['scoring_type']
        self.league_type = json['league_type']
        self.renew = json['renew']
        self.renewed = json['renewed']
        self.iris_group_chat_id = json['iris_group_chat_id']
        self.short_invitation_url = json.get('short_invitation_url')
        self.allow_add_to_dl_extra_pos = json['allow_add_to_dl_extra_pos']
        self.is_pro_league = json['is_pro_league']
        self.is_cash_league = json['is_cash_league']
        self.current_week = json['current_week']
        self.start_week = json['start_week']
        self.start_date = json['start_date']
        self.end_week = json['end_week']
        self.end_date = json['end_date']
        self.game_code = json['game_code']
        self.season = json['season']


class Settings:
    def __init__(self, json):
        json = json[0]
        self.draft_type = json['draft_type']
        self.is_auction_draft = json['is_auction_draft']
        self.scoring_type = json['scoring_type']
        self.persistent_url = json.get('persistent_url')
        self.uses_playoff = json['uses_playoff']
        self.has_playoff_consolation_games = json['has_playoff_consolation_games']
        self.playoff_start_week = json['playoff_start_week']
        self.uses_playoff_reseeding = json['uses_playoff_reseeding']
        self.uses_lock_eliminated_teams = json['uses_lock_eliminated_teams']
        self.num_playoff_teams = json['num_playoff_teams']
        self.num_playoff_consolation_teams = json['num_playoff_consolation_teams']
        self.has_multiweek_championship = json['has_multiweek_championship']
        self.uses_roster_import = json['uses_roster_import']
        self.roster_import_deadline = json['roster_import_deadline']
        self.waiver_type = json['waiver_type']
        self.waiver_rule = json['waiver_rule']
        self.uses_faab = json['uses_faab']
        self.draft_time = json['draft_time']
        self.draft_pick_time = json['draft_pick_time']
        self.post_draft_players = json['post_draft_players']
        self.max_teams = json['max_teams']
        self.waiver_time = json['waiver_time']
        self.trade_end_date = json['trade_end_date']
        self.trade_ratify_type = json['trade_ratify_type']
        self.trade_reject_time = json['trade_reject_time']
        self.player_pool = json['player_pool']
        self.cant_cut_list = json['cant_cut_list']
        self.draft_together = json['draft_together']
        self.can_trade_draft_picks = json['can_trade_draft_picks']
        self.sendbird_channel_url = json['sendbird_channel_url']
        self.pickem_enabled = json.get('pickem_enabled')
        self.uses_fractional_points = json.get('uses_fractional_points')
        self.uses_negative_points = json.get('uses_negative_points')
        self.roster_positions = self.__parse_roster_positions(json['roster_positions'])
        self.stat_categories = self.__parse_stat_categories(json['stat_categories']['stats'], json['stat_modifiers']['stats'])
        self.divisions = self.__parse_divisions(json.get('divisions', []))

    def __parse_roster_positions(self, json):
        return [RosterPosition(data['roster_position']) for data in json]

    def __parse_stat_categories(self, categories, modifiers):
        return [Stat(cat['stat'], mod['stat']) for (cat, mod) in zip(categories, modifiers)]

    def __parse_divisions(self, json):
        return [Division(d['division']) for d in json]


class Division:
    def __init__(self, json):
        self.division_id = json['division_id']
        self.name = json['name']


class RosterPosition:
    def __init__(self, json):
        self.position = json['position']
        self.position_type = json.get('position_type', '')
        self.count = int(json['count'])


class Stat:
    def __init__(self, category, modifier):
        self.stat_id = category['stat_id']
        self.enabled = category['enabled']
        self.name = category['name']
        self.display_name = category['display_name']
        self.sort_order = category['sort_order']
        self.position_type = category['position_type']
        self.stat_position_types = [data['stat_position_type']['position_type'] for data in category['stat_position_types']]
        self.modifier = float(modifier['value'])


class TeamStandings:
    def __init__(self, json):
        self.team = Team(json[0])
        self.__parse_team_stats(json[1])
        self.__parse_team_standings(json[2])

    def __parse_team_standings(self, json):
        json = json['team_standings']
        self.rank = json['rank']
        self.playoff_seed = json['playoff_seed']
        self.wins = json['outcome_totals']['wins']
        self.losses = json['outcome_totals']['losses']
        self.ties = json['outcome_totals']['ties']
        self.percentage = json['outcome_totals']['percentage']
        self.points_for = json['points_for']
        self.points_against = json['points_against']

    def __parse_team_stats(self, json):
        json = json['team_stats']
        self.coverage_type = json['coverage_type']
        self.season = json['season']
        self.stats = {d['stat']['stat_id']: d['stat']['value'] for d in json['stats']}
