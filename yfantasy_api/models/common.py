from yfantasy_api.models.helpers import flatten_attributes, as_float, as_bool, as_int


class Team:
    def __init__(self, json):
        attributes = self.__flatten_attributes(json)
        self.key = attributes.get('team_key')
        self.id = as_int(attributes.get('team_id'))
        self.name = attributes.get('name')
        self.priority = as_int(attributes.get('waiver_priority'))
        self.faab = as_int(attributes.get('faab_balance'))
        self.moves = as_int(attributes.get('number_of_moves'))
        self.trades = as_int(attributes.get('number_of_trades'))
        self.draft_grade = attributes.get('draft_grade')
        self.managers = self.__parse_managers(attributes)
        self.clinched_playoffs = as_bool(attributes.get('clinched_playoffs'))
        self.url = attributes.get('url')
        self.team_logos = self.__parse_team_logo(attributes)

        self.__parse_sub_resources(json)

    def __repr__(self):
        return str(self.__dict__) # pragma: no cover

    def __flatten_attributes(self, json):
        json = json[0] if type(json) == list else [json]
        return flatten_attributes(json)

    def __parse_sub_resources(self, json):
        for data in json:
            if 'roster' in data:
                self.__parse_roster(data)
            if 'team_standings' in data:
                self.__parse_team_standings(data)
            if 'team_points' in data:
                self.__parse_team_points(data)
            if 'team_projected_points' in data:
                self.__parse_projected_points(data)
            if 'team_stats' in data:
                self.__parse_team_stats(data)

    def __parse_roster(self, json):
        json = json['roster']['0']['players']
        self.players = [Player(json[p]['player']) for p in json if p != 'count']

    def __parse_team_standings(self, json):
        json = json['team_standings']
        self.rank = as_int(json['rank'])
        self.playoff_seed = as_int(json.get('playoff_seed', 0))
        self.wins = as_int(json['outcome_totals']['wins'])
        self.losses = as_int(json['outcome_totals']['losses'])
        self.ties = as_int(json['outcome_totals']['ties'])
        self.percentage = as_float(json['outcome_totals']['percentage'])
        self.points_for = as_float(json['points_for'])
        self.points_against = as_float(json['points_against'])

        if 'divisional_outcome_totals' in json:
            self.div_wins = as_int(json['divisional_outcome_totals']['wins'])
            self.div_losses = as_int(json['divisional_outcome_totals']['losses'])
            self.div_ties = as_int(json['divisional_outcome_totals']['ties'])

        if 'streak' in json:
            self.streak_type = json['streak']['type']
            self.streak_value = as_int(json['streak']['value'])

    def __parse_team_points(self, json):
        self.points = as_float(json['team_points']['total'])
    
    def __parse_projected_points(self, json):
        self.projected_points = as_float(json['team_projected_points']['total'])

    def __parse_team_stats(self, json):
        self.stats = {d['stat']['stat_id']: d['stat']['value'] for d in json['team_stats']['stats']}
    
    def __parse_team_logo(self, json):
        json = json.get('team_logos')
        if not json:
            return None
        return json[0]['team_logo']['url']
    
    def __parse_managers(self, json):
        return [Manager(m) for m in json.get('managers', [])]


class Manager:
    def __init__(self, json):
        json = json['manager']
        self.manager_id = as_int(json['manager_id'])
        self.name = json['nickname']
        self.felo_score = as_int(json.get('felo_score'))
        self.felo_tier = json.get('felo_tier')
        self.is_commissioner = as_bool(json.get('is_commissioner'))
    
    def __repr__(self):
        return str(self.__dict__) # pragma: no cover


class Player:
    def __init__(self, json):
        attributes = flatten_attributes(json[0])
        self.key = attributes['player_key']
        self.id = as_int(attributes['player_id'])
        self.name = attributes['name']['full']
        self.first_name = attributes['name']['first']
        self.last_name = attributes['name']['last']
        self.nfl_team = attributes.get('editorial_team_abbr').upper()
        self.team_name = attributes.get('editorial_team_full_name')
        self.number = as_int(attributes.get('uniform_number'))
        self.position = attributes.get('display_position')
        self.is_undroppable = as_bool(attributes.get('is_undroppable'))
        self.status = attributes.get('status')
        self.status_full = attributes.get('status_full')
        self.injury_note = attributes.get('injury_note')
        self.bye_week = as_int(attributes.get('bye_weeks', {}).get('week'))

        self.eligible_positions = self.__parse_eligible_positions(attributes)
        self.image_url = self.__parse_image_url(attributes)

        self.__parse_sub_resources(json)
    
    def __repr__(self):
        return str(self.__dict__) # pragma: no cover

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
            if 'selected_position' in data:
                self.__parse_selected_position(data)

    def __parse_stats(self, json):
        json = json['player_stats']['stats']
        self.stats = {as_int(s['stat']['stat_id']): as_int(s['stat']['value']) for s in json}

    def __parse_points(self, json):
        self.points = as_float(json['player_points']['total'])

    def __parse_ownership(self, json):
        # TODO
        json = json['ownership']
        self.team = None if json['ownership_type'] != 'team' \
            else Team(json['0']['teams']['0']['team'])

    def __parse_percent_owned(self, json):
        json = flatten_attributes(json['percent_owned'])
        self.percent_owned = as_int(json.get('value'))
        self.percent_changed = as_int(json.get('delta'))

    def __parse_draft_analysis(self, json):
        json = flatten_attributes(json['draft_analysis'])
        self.average_pick = as_float(json['average_pick'])
        self.average_round = as_float(json['average_round'])
        self.average_cost = as_float(json['average_cost'])
        self.percent_drafted = as_float(json['percent_drafted'])

    def __parse_selected_position(self, json):
        json = flatten_attributes(json['selected_position'])
        self.selected_position = json['position']
        self.is_flex = as_bool(json['is_flex'])
    
    def __parse_eligible_positions(self, json):
        return [ep['position'] for ep in json.get('eligible_positions', [])]
    
    def __parse_image_url(self, json):
        image_url = json.get('image_url', '')
        start = image_url.find('/https') + 1
        return image_url[start:]
