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
from analytics.leaderboard import get_batting_leaderboard,get_bowling_leaderboard
from analytics.player_statistics import get_player_batting_stats,get_matches_played
from analytics.ml_dataset import (generate_player_dataset,export_player_dataset_csv)

from ml.visulization import (generate_top_runs_chart , generate_top_wickets_chart,
                             generate_strike_rate_chart,generate_runs_vs_sr_chart)






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

    if is_new_match:

        insert_players(players)

        insert_deliveries(match_id, deliveries)

        insert_wickets(match_id, wickets)

    

    summary = generate_match_summary(match_id)

    print("Match ID:", match_id)
    print("Deliveries:", len(deliveries))
    print("Wickets:", len(wickets))

    
    team1_batting = generate_batting_scorecard(match_id,summary["team1"])
    team2_batting = generate_batting_scorecard(match_id,summary["team2"])

 

    team1_bowling = generate_bowling_scorecard(match_id,summary["team1"])
    team2_bowling = generate_bowling_scorecard(match_id,summary["team2"])



    return render_template(
        "scorecard.html",
        summary = summary,
        team1_batting = team1_batting,
        team2_batting = team2_batting,
        team1_bowling = team1_bowling,
        team2_bowling = team2_bowling
    )




@app.route("/analytics")
def analytics():
    batting_leaderboard = get_batting_leaderboard()
    bowling_leaderboard = get_bowling_leaderboard()

    dataset = generate_player_dataset()
    export_player_dataset_csv()
    generate_top_runs_chart()
    generate_top_wickets_chart()
    generate_strike_rate_chart()
    generate_runs_vs_sr_chart()
    

    return render_template("analytics.html",batting_leaderboard = batting_leaderboard,
                           bowling_leaderboard = bowling_leaderboard)



@app.route("/player/<player_name>")
def player_profile(player_name):

    batting_stats = get_player_batting_stats(player_name)

    matches_played = get_matches_played(player_name)

    return render_template(
        "player_profile.html",
        batting_stats=batting_stats,
        matches_played=matches_played
    )




if __name__ == "__main__":
    app.run(debug=True)

