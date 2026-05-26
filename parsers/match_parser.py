import json

def parser_match_info(file_path):
    with open(file_path,'r') as file:
        data = json.load(file)

    info = data["info"]

    match_details = {

        "match_type":info["match_type"],
        "venue":info["venue"],
        "city" :info["city"],
        "teams":info["teams"],
        "winner":info["outcome"]["winner"],
        "toss_winner":info["toss"]["winner"]
    }

    return match_details