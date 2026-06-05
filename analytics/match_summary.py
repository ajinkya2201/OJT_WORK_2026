from database.db_connection import get_db_connection

def generate_match_summary(match_id):
    connection = get_db_connection()

    cursor = connection.cursor()

    summary={}

    winner_query ="""
    select winner from matches where match_id = ?
    """

    highest_score_query = """
    select batter, sum(runs_batter) as total_runs from deliveries where match_id = ?
    group by batter order by total_runs desc limit 1
    """

    highest_wicket_query = """
    select bowler, count(*) as wickets from wickets where match_id = ?
    group by bowler order by wickets desc limit 1
    """

    team_score_query = """
    select batting_team, sum(total_runs) as team_score from deliveries where match_id = ?
    group by batting_team
    """

    team_wickets_query = """
    select d.batting_team,count(w.wicket_id) as wickets_lost from deliveries d
    left join wickets w on
    d.match_id = w.match_id and
    d.innings = w.innings and
    d.over_number = w.over_number and
    d.ball_number = w.ball_number
    where d.match_id = ?
    group by d.batting_team
    """

    boundary_quey = """
    select 
        sum (
                case
                    when runs_batter = 4
                    then 1
                    else 0
                end) as total_fours,
            sum (
                case
                    when runs_batter = 6
                    then 1
                    else 0
                end 
                ) as total_sixes
                from deliveries where match_id = ?

    """

    cursor.execute(winner_query,(match_id,))
    winner_result = cursor.fetchone()

    cursor.execute(highest_score_query,(match_id,)) 
    highest_score = cursor.fetchone()   

    cursor.execute(highest_wicket_query,(match_id,))
    highest_wicket_taker = cursor.fetchone()

    cursor.execute(team_score_query,(match_id,))
    team_scores = cursor.fetchall()

    cursor.execute(team_wickets_query,(match_id,))
    team_wickets = cursor.fetchall()

    cursor.execute(boundary_quey,(match_id,))
    boundary_result = cursor.fetchone()




    
    

    summary["winner"] = winner_result["winner"]
    summary["highest_runs"] = highest_score["total_runs"]
    summary["highest_scorer"] = highest_score["batter"]
    summary["highest_wicket_taker"] = highest_wicket_taker["bowler"]
    summary["highest_wickets"] = highest_wicket_taker["wickets"]

    if len(team_scores)>= 2:
        summary["team1"] = team_scores[0]["batting_team"]
        summary["team1_score"] =  team_scores[0]["team_score"]
        summary["team2"] = team_scores[1]["batting_team"]
        summary["team2_score"] =  team_scores[1]["team_score"]

    if len(team_wickets) >= 2:
        summary["team1_wickets"] = team_wickets[0]["wickets_lost"]
        summary["team2_wickets"] = team_wickets[1]["wickets_lost"]

    summary["team1_full_score"] = (f"{summary['team1_score']}/{summary['team1_wickets']}")
    summary["team2_full_score"] = (f"{summary['team2_score']}/{summary['team2_wickets']}")

    summary["total_fours"] = boundary_result["total_fours"]
    summary["total_sixes"] = boundary_result["total_sixes"]


    
    

    connection.close()
    return summary