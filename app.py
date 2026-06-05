from flask import Flask,render_template,request
from utils.validators import allowed_file
from werkzeug.utils import secure_filename
import os

from parsers.match_parser import parser_match_info
from parsers.player_parse import parser_players
from parsers.delivery_parser import parse_deliveries
from parsers.wicket_parser import parse_wickets

from database.insert_match import insert_match
from database.insert_players import insert_players
from database.insert_deliveries import insert_deliveries
from database.insert_wickets import insert_wickets

from analytics.batting_analysis import generate_batting_scorecard
from analytics.bowling_analysis import generate_bowling_scorecard
from analytics.match_summary import generate_match_summary







app = Flask(__name__)

UPLOAD_FOLDER = "uploads/json_files"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("upload.html")


@app.route("/upload",methods=["POST"])
def upload_file():
    if "json_file" not in request.files:
        return "No file part found"

    uploaded_file = request.files["json_file"]

    if uploaded_file.filename=="":
        return "No file selected"
    
    if not allowed_file(uploaded_file.filename):
        return "only json files are allowed"
    
    filename = secure_filename(uploaded_file.filename)

    file_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)

    uploaded_file.save(file_path)


    match_data=parser_match_info(file_path)
    match_id,is_new_match = insert_match(match_data)

    players = parser_players(file_path)
    deliveries = parse_deliveries(file_path)
    wickets = parse_wickets(file_path)


    scorecard = generate_batting_scorecard(match_id)
    bowling_scorecard = generate_bowling_scorecard(match_id)

    summary = generate_match_summary(match_id)
    # print(summary)

    


    return render_template(
        "scorecard.html",
        summary = summary,
        batting_scorecard = scorecard,
        bowling_scorecard = bowling_scorecard
    )


    output = " <h2> Bowling Scorecard</h2>"

    for bowler in bowling_scorecard:
        output += f"""
        Bowler: {bowler['bowler']} |
        Overs: {bowler['overs']} |
        Runs: {bowler['runs_conceded']} |
        Wickets: {bowler['wickets']} |
        Economy: {bowler['economy']}
        <br>
        """

    return output



    output = ""
    for player in scorecard:
        output += f"""
        Batter: {player['batter']} |
        Runs: {player['total_runs']} |
        Balls: {player['balls_faced']} |
        4s: {player['fours']} |
        6s: {player['sixes']} | 
        SR: {player['strike_rate']}       

        <br>
        """
    return output
        



    if is_new_match:
        insert_players(players)
        insert_deliveries(match_id,deliveries)
        insert_wickets(match_id,wickets)
        return "New Match Data Inserted Successfully"
    else:

        return "Match Already Exists with Match Id: {match_id}"
    

    
    



    return "Match,Players and Deliveries Inserted Successfuly"

    return f"Match  and Players inserted Successfully "

    wicket_output =""
    for wicket in wickets:
        wicket_output += f"""
        Innings: {wicket['innings']} |
    
        Over: {wicket['over']}.{wicket['ball']} |    
        Player Out: {wicket['player_out']} |   
        Dismissal: {wicket['dismissal_type']} |       
        Bowler: {wicket['bowler']} 
        <br>
        """
    return wicket_output



    delivery_output = ""

    for delivery in deliveries[:20]:

        delivery_output += f"""
        Innings: {delivery['innings']} |
        Over: {delivery['over']}.{delivery['ball']} |
        Batter: {delivery['batter']} | 
        Bowler: {delivery['bowler']} | 
        Runs: {delivery['total_runs']}
        
        <br>
        """
    return delivery_output


    player_output =""
    for player in players:
        player_output +=f"""
        Player: {player['player_name']}
        | Team: {player['team']}<br>
        """
    return player_output
    

    return f"""
    Match Type : {match_data['match_type']}<br>
    Venue : {match_data['venue']}<br>
    City : {match_data['city']}<br>
    Teams : {match_data['teams']}<br>
    Winner: {match_data['winner']} <br>
    Toss Winner: {match_data['toss_winner']}

    """


    
    




if __name__ == "__main__":
    app.run(debug=True)

