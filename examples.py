from yfantasy_api import YahooFantasyApi

league_id = 17457  # This should be the id of the league you are querying
game_id = "nhl"  # This should be the id of the game you are querying
team_id = 1  # This should be the id of the team you are querying

api = YahooFantasyApi(league_id, game_id)


def example_usage_one():
    team = api.team(team_id).roster().stats(date="2021-03-31").get()
    for player in team.players:
        print(player.full_name, player.points)


def example_usage_two():
    league = api.league().draft_results().players().get()

    for draft_result in league.draft_results:
        print(
            f"{draft_result.round} - {draft_result.pick} - {draft_result.player.full_name}"
        )


if __name__ == "__main__":
    example_usage_one()
    example_usage_two()
