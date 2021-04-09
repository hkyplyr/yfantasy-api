from yfantasy_api.models.helpers import flatten_attributes


class Team:
    def __init__(self, json):
        self.json = json
        self.info = self.__parse_team_info(json)
        self.__parse_sub_resources(json)

    def __parse_team_info(self, json):
        if type(json) == list:
            return TeamInfo(json[0])
        else:
            return TeamInfo([json])

    def __parse_sub_resources(self, json):
        for data in json:
            if 'roster' in data:
                self.__parse_roster(data['roster'])
            if 'team_standings' in data:
                self.__parse_team_standings(data['team_standings'])
            if 'team_points' in data:
                self.__parse_team_points(data['team_points'])
            if 'team_stats' in data:
                self.__parse_team_stats(data['team_stats'])

    def __parse_roster(self, json):
        json = json['0']['players']
        self.players = [Player(json[str(d)]['player']) for d in range(json['count'])]

    def __parse_team_standings(self, json):
        self.rank = int(json['rank'])
        self.playoff_seed = int(json.get('playoff_seed', 0))
        self.wins = int(json['outcome_totals']['wins'])
        self.losses = int(json['outcome_totals']['losses'])
        self.ties = int(json['outcome_totals']['ties'])
        self.percentage = float(json['outcome_totals']['percentage'])
        self.points_for = float(json['points_for'])
        self.points_against = float(json['points_against'])

        if 'divisional_outcome_totals' in json:
            self.div_wins = int(json['divisional_outcome_totals']['wins'])
            self.div_losses = int(json['divisional_outcome_totals']['losses'])
            self.div_ties = int(json['divisional_outcome_totals']['ties'])

        if 'streak' in json:
            self.streak_type = json['streak']['type']
            self.streak_value = json['streak']['value']

    def __parse_team_points(self, json):
        self.points = json['total']

    def __parse_team_stats(self, json):
        self.stats = {d['stat']['stat_id']: d['stat']['value'] for d in json['stats']}


class TeamInfo:
    def __init__(self, json):
        attributes = flatten_attributes(json)
        self.team_key = attributes['team_key']
        self.team_id = attributes['team_id']
        self.name = attributes['name']
        self.url = attributes['url']
        self.team_logos = attributes.get('team_logos')
        self.waiver_priority = attributes.get('waiver_priority')
        self.faab_balance = attributes.get('faab_balance')
        self.number_of_moves = attributes.get('number_of_moves')
        self.number_of_trades = attributes.get('number_of_trades')
        self.roster_adds = attributes.get('roster_adds')
        self.league_scoring_type = attributes.get('league_scoring_type')
        self.has_draft_grade = attributes.get('has_draft_grade')
        self.managers = self.__parse_managers(attributes.get('managers', []))
        self.clinched_playoffs = attributes.get('clinched_playoffs', 0)

    def __parse_managers(self, json):
        return [Manager(d) for d in json]


class Manager:
    def __init__(self, json):
        json = json['manager']
        self.manager_id = json['manager_id']
        self.nickname = json['nickname']
        self.guid = json['guid']
        self.email = json.get('email')
        self.image_url = json['image_url']
        self.felo_score = json.get('felo_score')
        self.felo_tier = json.get('felo_tier')
        self.is_commissioner = json.get('is_commissioner', 0)


class Player:
    def __init__(self, json):
        attributes = flatten_attributes(json[0])
        self.player_key = attributes['player_key']
        self.player_id = attributes['player_id']
        self.first_name = attributes['name']['first']
        self.last_name = attributes['name']['last']
        self.full_name = attributes['name']['full']
        self.editorial_player_key = attributes.get('editorial_player_key')
        self.editorial_team_key = attributes.get('editorial_team_key')
        self.editorial_team_name = attributes.get('editorial_team_full_name')
        self.editorial_team_abbr = attributes['editorial_team_abbr']
        self.uniform_number = attributes.get('uniform_number')
        self.display_position = attributes['display_position']
        self.headshot_url = attributes.get('headshot', {}).get('url')
        self.image_url = attributes.get('image_url')
        self.is_undroppable = attributes.get('is_undroppable', 0)
        self.position_type = attributes['position_type']
        self.primary_position = attributes.get('primary_position')
        self.eligible_positions = [d['position'] for d in attributes.get('eligible_positions', [])]
        self.has_player_notes = attributes.get('has_player_notes', 0)
        self.has_recent_player_notes = attributes.get('has_recent_player_notes', 0)
        self.player_notes_last_timestamp = attributes.get('player_notes_last_timestamp', None)
        self.status = attributes.get('status', None)
        self.status_full = attributes.get('status_full', None)
        self.injury_note = attributes.get('injury_note', None)
        self.on_disabled_list = attributes.get('on_disabled_list', 0)
        self.__parse_sub_resources(json)

    def __parse_sub_resources(self, json):
        for data in json:
            if 'player_stats' in data:
                self.__parse_stats(data)
            if 'player_points' in data:
                self.__parse_points(data)
            if 'ownership' in data:
                self.__parse_ownership(data)
            if 'percent_owned' in data:
                self.__parse_percent_owned(data)
            if 'draft_analysis' in data:
                self.__parse_draft_analysis(data)

    def __parse_stats(self, json):
        json = json['player_stats']
        self.coverage_type = json['0']['coverage_type']
        self.coverage_value = json['0'][self.coverage_type]
        self.stats = {d['stat']['stat_id']: d['stat']['value'] for d in json['stats']}

    def __parse_points(self, json):
        json = json['player_points']
        self.points = json['total']

    def __parse_ownership(self, json):
        json = json['ownership']
        self.team = None if json['ownership_type'] != 'team' \
            else Team(json['0']['teams']['0']['team'])

    def __parse_percent_owned(self, json):
        json = json['percent_owned']
        for data in json:
            if 'value' in data:
                self.percent_owned = data['value']
            if 'delta' in data:
                self.percent_changed = data['delta']

    def __parse_draft_analysis(self, json):
        json = json['draft_analysis']
        self.average_pick = json[0]['average_pick']
        self.average_round = json[1]['average_round']
        self.average_cost = json[2]['average_cost']
        self.percent_drafted = json[3]['percent_drafted']
