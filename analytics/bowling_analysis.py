from database.db_connection import get_db_connection

def generate_bowling_scorecard(match_id):
    connection = get_db_connection()

    cursor = connection.cursor()

    query = """
    select d.bowler,
    count(d.delivery_id) as balls_bowled,
    round(
        count(d.delivery_id) / 6.0,
        1
    ) as overs,
    sum(d.total_runs) as runs_conceded,
    count(w.wicket_id) as wickets,
    round((
            SUM(d.total_runs) * 1.0
        )/
        (
                COUNT(d.delivery_id) / 6.0
            ),
            2
        ) AS economy
    
    FROM deliveries d
    
    LEFT JOIN wickets w
    
    ON
    
        d.match_id = w.match_id
    
        AND d.bowler = w.bowler
    
        AND d.over_number = w.over_number
    
        AND d.ball_number = w.ball_number
    
    WHERE d.match_id = ?
    
    GROUP BY d.bowler
    
    ORDER BY wickets DESC
    """
    

    cursor.execute(query,(match_id,))
    scorecard = cursor.fetchall()

    connection.close()

    return scorecard
    
    