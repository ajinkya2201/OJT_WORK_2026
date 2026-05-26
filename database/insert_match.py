from database.db_connection import get_db_connection
import sqlite3

def insert_match(match_data):
    connection = get_db_connection()

    cursor = connection.cursor()
    query = """

    insert into matches(
    match_type,venue,city,team1,team2,winner,toss_winner
    )
    values(?,?,?,?,?,?,?)
    """
    try:

        cursor.execute(query,(
            match_data["match_type"],
            match_data["venue"],
            match_data["city"],
            match_data["teams"][0],
            match_data["teams"][1],
            match_data["winner"],
            match_data["toss_winner"],
        ))

        connection.commit()
        match_id = cursor.lastrowid
        is_new_match = True

    except sqlite3.IntegrityError:
        existing_match_query = """
        select match_id from matches where
        match_type = ?
        and venue = ?
        and team1 = ?
        and team2 = ?
        """

        cursor.execute(existing_match_query,(
            match_data["match_type"],
            match_data["venue"],
            match_data["teams"][0],
            match_data["teams"][1]
        ))

        existing_match = cursor.fetchone()
        match_id = existing_match["match_id"]
        is_new_match = False

    connection.close()
    return match_id,is_new_match

