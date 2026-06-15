from database.db_connection import get_db_connection


def generate_player_match_dataset():

    connection = get_db_connection()

    cursor = connection.cursor()

    query = """

    SELECT

        batter AS player,

        match_id,

        SUM(runs_batter) AS runs,

        COUNT(*) AS balls,

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

    GROUP BY
        match_id,
        batter

    ORDER BY
        match_id,
        runs DESC

    """

    cursor.execute(query)

    dataset = cursor.fetchall()

    connection.close()

    return dataset

import csv


def export_player_match_dataset():

    dataset = generate_player_match_dataset()

    with open(
        "player_match_dataset.csv",
        "w",
        newline=""
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "player",
            "match_id",
            "runs",
            "balls",
            "fours",
            "sixes"
        ])

        for row in dataset:

            writer.writerow([
                row["player"],
                row["match_id"],
                row["runs"],
                row["balls"],
                row["fours"],
                row["sixes"]
            ])

    print("Player Match Dataset CSV Created")