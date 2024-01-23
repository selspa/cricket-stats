ALTER TABLE teams ALTER COLUMN team_id SET DEFAULT nextval('teams_team_id_seq'); 

ALTER TABLE venues ALTER COLUMN venue_id SET DEFAULT nextval('venues_venue_id_seq'); 

ALTER TABLE games ALTER COLUMN game_id SET DEFAULT nextval('games_game_id_seq'); 

ALTER TABLE simulations ALTER COLUMN simulation_id SET DEFAULT nextval('simulations_simulation_id_seq');