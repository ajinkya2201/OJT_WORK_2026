from database.db_connection import get_db_connection


def insert_wickets(match_id, wickets):

    connection = get_db_connection()

    cursor = connection.cursor()

    query = """
    insert into wickets(
    match_id,innings,over_number,ball_number,player_out,dismissal_type,bowler

    )
    values(?,?,?,?,?,?,?)
    """

    for wicket in wickets:
        cursor.execute(query,(
            match_id,
            wicket["innings"],
            wicket["over"],
            wicket["ball"],
            wicket["player_out"],
            wicket["dismissal_type"],
            wicket["bowler"],
            
        ))

    connection.commit()
    connection.close()


