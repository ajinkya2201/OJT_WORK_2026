from database.db_connection import get_db_connection


def insert_players(players):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    insert into players(player_name,team_name)
    values(?,?)
    """

    for player in players:
        cursor.execute(query,(
            player["player_name"],
            player["team"]
        ))

    connection.commit()
    connection.close()
