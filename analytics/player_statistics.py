from database.db_connection import get_db_connection

def get_player_batting_stats(player_name):

    connection = get_db_connection()
    cursor = connection.cursor()



    query = """
    select batter,
            sum(runs_batter) as total_runs,
            count(*) as balls_faced,

            sum(
                case
                    when runs_batter = 4
                    then 1
                    else 0
                end
                ) as fours,
            sum(
                case
                    when runs_batter = 6
                    then 1
                    else 0
                end
                ) as sixes,

            round(
                (
                    sum(runs_batter) * 100.0
                    ) / count(*),2
                )as strike_rate

            from deliveries where batter = ?
            group by batter
            
    """


    cursor.execute(query,(player_name,))
    stats = cursor.fetchone()
    connection.close()

    return stats


def get_matches_played(player_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    query="""
    select count(distinct match_id) as matches_played
    from deliveries where batter = ?
    """

    cursor.execute(query,(player_name,))
    result = cursor.fetchone()
    connection.close()

    return result["matches_played"]

