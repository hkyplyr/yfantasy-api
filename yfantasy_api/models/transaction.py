from yfantasy_api.models.common import Player


class Transaction:
    def __init__(self, json):
        self.transaction_key = json['transaction_key']
        self.transaction_id = json['transaction_id']
        self.type = json['type']
        self.status = json['status']
        self.timestamp = json['timestamp']
        self.faab_bid = json.get('faab_bid')
    
    def __repr__(self):
        return str(self.__dict__) # pragma: no cover


class Add(Transaction):
    def __init__(self, json):
        super().__init__(json[0])
        self.added_player = Player(json[1]['players']['0']['player'])
        self.__parse_transaction_data(json[1]['players']['0']['player'][1]['transaction_data'][0])

    def __parse_transaction_data(self, json):
        self.source_type = json['source_type']
        self.destination_type = json['destination_type']
        self.destination_team_key = json['destination_team_key']
        self.destination_team_name = json['destination_team_name']


class Drop(Transaction):
    def __init__(self, json):
        super().__init__(json[0])
        self.dropped_player = Player(json[1]['players']['0']['player'])
        self.__parse_transaction_data(json[1]['players']['0']['player'][1]['transaction_data'])

    def __parse_transaction_data(self, json):
        self.source_type = json['source_type']
        self.source_team_key = json['source_team_key']
        self.source_team_name = json['source_team_name']
        self.destination_type = json['destination_type']


class AddDrop(Transaction):
    def __init__(self, json):
        super().__init__(json[0])
        self.added_player = Player(json[1]['players']['0']['player'])
        self.dropped_player = Player(json[1]['players']['1']['player'])
        self.__parse_transaction_data(json[1]['players']['0']['player'][1]['transaction_data'][0])

    def __parse_transaction_data(self, json):
        self.source_type = json['source_type']
        self.destination_type = json['destination_type']
        self.destination_team_key = json['destination_team_key']
        self.destination_team_name = json['destination_team_name']


class Pick:
    def __init__(self, json):
        self.source_team_key = json['source_team_key']
        self.source_team_name = json['source_team_name']
        self.destination_team_key = json['destination_team_key']
        self.destination_team_name = json['destination_team_name']
        self.original_team_key = json['original_team_key']
        self.original_team_name = json['original_team_name']
        self.round = json['round']


class Trade(Transaction):
    def __init__(self, json):
        info = json[0]
        super().__init__(info)
        self.trader_team_key = info['trader_team_key']
        self.trader_team_name = info['trader_team_name']
        self.tradee_team_key = info['tradee_team_key']
        self.tradee_team_name = info['tradee_team_name']
        self.traded_picks = [Pick(d['pick']) for d in info.get('picks', [])]
        json = json[1]['players']
        print(json)
        if type(json) == list:
            self.traded_players = []
        else:
            self.traded_players = [Player(json[str(d)]['player']) for d in range(json['count'])]
