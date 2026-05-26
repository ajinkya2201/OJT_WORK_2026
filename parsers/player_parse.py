import json

def parser_players(file_path):
    with open(file_path,'r') as file:
        data = json.load(file)

    players_data = data["info"]["players"]

    player_list = []
    for team_name,players in players_data.items():
        for player in players:
            player_info = {
                "player_name":player,
                "team":team_name
            }

            player_list.append(player_info)

    return player_list