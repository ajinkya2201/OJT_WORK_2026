import json

def parse_wickets(file_path):
    with open(file_path,"r") as file:
        data = json.load(file)

    
    innings_data = data["innings"]
    all_wickets = []
    innings_number = 1

    for innings in innings_data:
        overs = innings["overs"]

        for over_data in overs:
            over_number = over_data["over"]

            deliveries = over_data["deliveries"]
            ball_number = 1

            for delivery in deliveries:
                if "wickets" in delivery:
                    wickets = delivery["wickets"]

                    for wicket in wickets:
                        wicket_info = {
                            "innings":innings_number,
                            "over": over_number,
                            "ball": ball_number,
                            "player_out": wicket["player_out"],
                            "dismissal_type": wicket["kind"],
                            "bowler": delivery["bowler"]
                        }
                        all_wickets.append(wicket_info)
                ball_number += 1
        innings_number +=1

    return all_wickets