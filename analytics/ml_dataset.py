from database.db_connection import get_db_connection

from database.db_connection import get_db_connection


def generate_player_dataset():

    connection = get_db_connection()

    cursor = connection.cursor()

    query = """

    SELECT

        batter AS player,

        COUNT(DISTINCT match_id) AS matches_played,

        SUM(runs_batter) AS total_runs,

        COUNT(*) AS balls_faced,

        ROUND(
            SUM(runs_batter) * 100.0 / COUNT(*),
            2
        ) AS strike_rate,

        SUM(
            CASE
                WHEN runs_batter = 4
                THEN 1
                ELSE 0
            END
        ) AS fours,

        SUM(
            CASE
                WHEN runs_batter = 6
                THEN 1
                ELSE 0
            END
        ) AS sixes

    FROM deliveries

    GROUP BY batter

    ORDER BY total_runs DESC

    """

    cursor.execute(query)
    dataset = cursor.fetchall()
    connection.close()

    return dataset

import csv

def export_player_dataset_csv():
    dataset = generate_player_dataset()


    with open("player_dataset.csv","w",newline="")as csv_file:
        writer = csv.writer(csv_file)


        writer.writerow([
            "player",
            "matches_played",
            "total_runs",
            "balls_faced",
            "strike_rate",
            "fours",
            "sixes"
        ])

        for row in dataset:

            writer.writerow([
                row["player"],
                row["matches_played"],
                row["total_runs"],
                row["balls_faced"],
                row["strike_rate"],
                row["fours"],
                row["sixes"]
            ])

    print("CSV Created Successfully")

