from analytics.player_match_dataset import generate_player_match_dataset


def create_future_prediction_dataset():

    dataset = generate_player_match_dataset()

    player_matches = {}

    for row in dataset:

        player = row["player"]

        if player not in player_matches:
            player_matches[player] = []

        player_matches[player].append(
            {
                "match_id": row["match_id"],
                "runs": row["runs"]
            }
        )

    training_data = []

    for player in player_matches:

        matches = sorted(
            player_matches[player],
            key=lambda x: x["match_id"]
        )

        for i in range(len(matches) - 1):

            training_data.append(
                {
                    "player": player,
                    "previous_runs": matches[i]["runs"],
                    "next_runs": matches[i + 1]["runs"]
                }
            )

    return training_data


import csv


def export_future_prediction_dataset():

    data = create_future_prediction_dataset()

    with open(
        "future_prediction_dataset.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "player",
                "previous_runs",
                "next_runs"
            ]
        )

        for row in data:

            writer.writerow(
                [
                    row["player"],
                    row["previous_runs"],
                    row["next_runs"]
                ]
            )

    print(
        "Future Prediction Dataset Created"
    )


def create_future_prediction_dataset_v2():

    dataset = generate_player_match_dataset()

    player_matches = {}

    for row in dataset:

        player = row["player"]

        if player not in player_matches:
            player_matches[player] = []

        player_matches[player].append(
            {
                "match_id": row["match_id"],
                "runs": row["runs"],
                "balls": row["balls"],
                "fours": row["fours"],
                "sixes": row["sixes"]
            }
        )

    training_data = []

    for player in player_matches:

        matches = sorted(
            player_matches[player],
            key=lambda x: x["match_id"]
        )

        for i in range(len(matches) - 1):

            training_data.append(
                {
                    "player": player,

                    "previous_runs":
                        matches[i]["runs"],

                    "previous_balls":
                        matches[i]["balls"],

                    "previous_fours":
                        matches[i]["fours"],

                    "previous_sixes":
                        matches[i]["sixes"],

                    "next_runs":
                        matches[i + 1]["runs"]
                }
            )

    return training_data

import csv

def export_future_prediction_dataset_v2():

    data = create_future_prediction_dataset_v2()

    with open(
        "future_prediction_dataset_v2.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "player",
                "previous_runs",
                "previous_balls",
                "previous_fours",
                "previous_sixes",
                "next_runs"
            ]
        )

        for row in data:

            writer.writerow(
                [
                    row["player"],
                    row["previous_runs"],
                    row["previous_balls"],
                    row["previous_fours"],
                    row["previous_sixes"],
                    row["next_runs"]
                ]
            )

    print("Future Prediction Dataset V2 Created")