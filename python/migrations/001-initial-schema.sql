CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(255) NOT NULL
);

CREATE SEQUENCE teams_team_id_seq START WITH 0 MINVALUE 0;

CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL
);

CREATE SEQUENCE venues_venue_id_seq START WITH 0 MINVALUE 0;

CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY,
    home_team_id INTEGER,
    away_team_id INTEGER,
    game_date DATE,
    venue_id INTEGER,
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
); 

CREATE SEQUENCE games_game_id_seq START WITH 0 MINVALUE 0;

CREATE TABLE IF NOT EXISTS simulations (
    simulation_id INTEGER PRIMARY KEY,
    game_id INTEGER,
    home_team_score INTEGER,
    away_team_score INTEGER,
    simulation_run INTEGER,
    FOREIGN KEY (game_id) REFERENCES games(game_id)
); 

CREATE SEQUENCE simulations_simulation_id_seq START WITH 0 MINVALUE 0;