-- MATCH 
create table if not exists matches(
    match_id integer primary key autoincrement,
    match_type text,
    venue text,
    city text,
    team1 text,
    team2 text,
    winner text,
    toss_winner text,
    unique(match_type,
            venue,
            team1,
            team2)
);

-- PLAYERS
create table if not exists players(
    player_id integer primary key autoincrement,
    player_name text,
    team_name text
);

--DELIVERIES

create table if not exists deliveries(
    delivery_id integer primary key autoincrement,
    match_id  integer,
    innings integer,
    batting_team text,
    over_number integer,
    ball_number integer,
    batter text,
    bowler text,
    non_striker text,
    runs_batter integer,
    extras integer,
    total_runs integer
);

--  WICKETS
create table if not exists wickets (
    wicket_id integer primary key autoincrement,
    match_id integer,
    innings integer,
    over_number integer,
    ball_number integer,
    player_out text,
    dismissal_type text ,
    bowler text
);
