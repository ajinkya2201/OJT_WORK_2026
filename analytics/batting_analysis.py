from database.db_connection import get_db_connection

def generate_batting_scorecard(match_id,batting_team):
    connection = get_db_connection()

    cursor = connection.cursor()

    query = """
        select 
        batter , sum(runs_batter) as total_runs,
        count(*) as balls_faced,
        sum(
            case
                when runs_batter = 4 then 1
                else 0

            end
            ) as fours,
        
        sum(
            case
                when runs_batter = 6 then 1
                else 0
            end
        ) as sixes,

        round(
            (
                sum(runs_batter) * 100.0
            ) / count(*),
            2
            ) as strike_rate

    from deliveries  where match_id = ? and batting_team = ?
    group by batter order by total_runs desc
    
    """

    cursor.execute(query,(match_id,batting_team))
    scorecard = cursor.fetchall()
    connection.close()
    return scorecard