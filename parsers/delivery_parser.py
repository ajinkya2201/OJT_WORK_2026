import json

def parse_deliveries(file_path):
    with open(file_path,"r")as file:
        data = json.load(file)

    innings_data = data["innings"]
    all_deliveries = []

    innings_number = 1
    for innings in innings_data:
        batting_team = innings["team"]

        overs = innings["overs"]
        for over_data in overs:
            over_number = over_data["over"]
            deliveries = over_data["deliveries"]
            ball_number = 1

            for delivery in deliveries:
                delivery_info = {
                    "innings": innings_number,
                    "batting_team": batting_team,
                    "over": over_number,
                    "ball": ball_number,
                    "batter": delivery["batter"],
                    "bowler": delivery["bowler"],
                    "non_striker": delivery["non_striker"],
                    "runs_batter": delivery["runs"]["batter"],
                    "extras": delivery["runs"]["extras"],
                    "total_runs": delivery["runs"]["total"]
                }

                all_deliveries.append(delivery_info)
                ball_number += 1
    innings_number += 1
    return all_deliveries