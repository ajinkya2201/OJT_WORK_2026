from database.db_connection import get_db_connection

def insert_deliveries(match_id,deliveries):
    connection = get_db_connection()

    cursor = connection.cursor()

    query = """
    insert into deliveries(
    match_id,innings,batting_team,over_number,ball_number,
    batter,bowler,non_striker,runs_batter,
    extras,total_runs
    )values(?,?,?,?,?,?,?,?,?,?,?)
    """

    for delivery in deliveries:
        cursor.execute(query,(
            match_id,
            delivery["innings"],
            delivery["batting_team"],
            delivery["over"],
            delivery["ball"],
            delivery["batter"],
            delivery["bowler"],
            delivery["non_striker"],
            delivery["runs_batter"],
            delivery["extras"],
            delivery["total_runs"]

        ))

    connection.commit()
    connection.close()