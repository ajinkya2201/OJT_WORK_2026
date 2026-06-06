from database.db_connection import get_db_connection

def get_batting_leaderboard():

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    select batter , sum(runs_batter) as total_runs from deliveries
    group by batter order by total_runs desc
    """

    cursor.execute(query)
    leaderboard = cursor.fetchall()
    connection.close()

    return leaderboard


def get_bowling_leaderboard():

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    select bowler,count(*) as total_wickets from wickets 
    group by bowler order by total_wickets desc 
    """

    cursor.execute(query)
    leaderboard = cursor.fetchall()
    connection.close()

    return leaderboard


