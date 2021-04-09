class Game:
    def __init__(self, json):
        self.json = json
        self.info = self.__parse_game_info(json)
        self.__parse_sub_resources(json)

    def __parse_game_info(self, json):
        if type(json) == list:
            return GameInfo(json[0])
        else:
            return GameInfo(json)

    def __parse_sub_resources(self, json):
        for data in json:
            if 'game_weeks' in data:
                self.__parse_game_weeks(data['game_weeks'])
            if 'position_types' in data:
                self.__parse_position_types(data['position_types'])
            if 'roster_positions' in data:
                self.__parse_roster_positions(data['roster_positions'])
            if 'stat_categories' in data:
                self.__parse_stat_categories(data['stat_categories'])

    def __parse_game_weeks(self, json):
        self.game_weeks = [GameWeek(json[str(d)]['game_week']) for d in range(json['count'])]

    def __parse_position_types(self, json):
        self.position_types = [PositionType(d['position_type']) for d in json]

    def __parse_roster_positions(self, json):
        self.roster_positions = [RosterPosition(d['roster_position']) for d in json]

    def __parse_stat_categories(self, json):
        self.stat_categories = [StatCategory(d['stat']) for d in json['stats']]


class GameInfo:
    def __init__(self, json):
        self.game_key = json['game_key']
        self.game_id = json['game_id']
        self.name = json['name']
        self.code = json['code']
        self.type = json['type']
        self.url = json['url']
        self.season = json['season']
        self.is_registration_over = json['is_registration_over']
        self.is_game_over = json['is_game_over']
        self.is_offseason = json['is_offseason']


class GameWeek:
    def __init__(self, json):
        self.week = json['week']
        self.display_name = json['display_name']
        self.start = json['start']
        self.end = json['end']


class PositionType:
    def __init__(self, json):
        self.type = json['type']
        self.display_name = json['display_name']


class RosterPosition:
    def __init__(self, json):
        self.position = json['position']
        self.abbreviation = json['abbreviation']
        self.display_name = json['display_name']
        self.position_type = json.get('position_type')
        self.is_bench = json.get('is_bench')
        self.is_disabled_list = json.get('is_disabled_list')


class StatCategory:
    def __init__(self, json):
        self.stat_id = json['stat_id']
        self.name = json['name']
        self.display_name = json['display_name']
        self.sort_order = json['sort_order']
        self.position_types = [d['position_type'] for d in json.get('position_types', [])]
        self.is_composite_stat = json.get('is_composite_stat')
        self.base_stats = [d['base_stat']['stat_id'] for d in json.get('base_stats', [])]
