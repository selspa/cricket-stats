import csv

# function to select the list of team
def select_teams(cur):
    
    sql = """SELECT * FROM teams;"""
    cur.execute(sql)
    teams = cur.fetchall()
    rows = cur.rowcount
    
    return teams, rows
    

# function to get the list of teams from simulations.cvs and insert them into teams table
def insert_teams(simulations_csv, cur, conn):
    
    insert_teams = """INSERT INTO teams (team_id, team_name) VALUES (%s, %s);"""
    inserted_rows = 0
    
    with open(simulations_csv, newline='', encoding='utf-8') as csvfile:
        
        simulations_reader = csv.DictReader(csvfile)

        for row in simulations_reader:
        # check if the select query returned records from teams tables
            
            teams, rows = select_teams(cur)
            
            teams_ids = [team["team_id"] for team in teams]
            teams_names = [team["team_name"] for team in teams]
            
            # check if the select query to return teams data returned something
            if rows != 0:
                # check if the team isn't already in the table
                if row["team_id"] not in teams_ids and row["team"] not in teams_names:
                    team_id = row["team_id"]
                    team_name = row["team"]
                    try:
                        cur.execute(insert_teams, (team_id, team_name), prepare=True)
                        conn.commit()
                        if cur.rowcount != 0:
                            inserted_rows += 1
                    except: 
                        print("An error occurred. Failed to insert team_id = "+str(team_id)+" and team_name = "+str(team_name))
                        conn.rollback()
            else:
                team_id = row["team_id"]
                team_name = row["team"]
                cur.execute(insert_teams, (team_id, team_name), prepare=True)
                conn.commit()
                if cur.rowcount != 0:
                    inserted_rows += 1
        
    if inserted_rows != 0:
        return True
    else: 
        return False


# function to insert data from venues.csv into venues table 
def insert_venues(venues_csv, cur, conn):
    
    insert_venues = """INSERT INTO venues (venue_id, venue_name) VALUES (%s, %s);"""
    inserted_rows = 0
    
    with open(venues_csv, newline='', encoding='utf-8') as csvfile:
        
        venues_reader = csv.DictReader(csvfile)
    
        for row in venues_reader:
            
            sql = """SELECT * FROM venues;"""
            cur.execute(sql)
            venues = cur.fetchall()
            venues_ids = [venue["venue_id"] for venue in venues]
            venues_names = [venue["venue_name"] for venue in venues]
    
            # check if the venue isn't already in the table
            if row["venue_id"] not in venues_ids and row["venue_name"] not in venues_names:
                venue_id = row["venue_id"]
                venue_name = row["venue_name"]
                try:
                    cur.execute(insert_venues, (venue_id, venue_name), prepare=True)
                    conn.commit()
                    if cur.rowcount != 0:
                        inserted_rows += 1
                except: 
                    print("An error occurred. Failed to insert team_id = "+str(venue_id)+" and team_name = "+str(venue_name))
                    conn.rollback()
    
    if inserted_rows != 0:
        return True
    else: 
        return False
    

# function to insert data from games.csv into table games
def insert_games(games_csv, cur, conn):
    
    teams, rows = select_teams(cur)
    
    insert_games = """INSERT INTO games (home_team_id, away_team_id, game_date, venue_id)
                        VALUES (%s, %s, %s, %s);"""
    select_games = """SELECT * FROM games 
                        WHERE home_team_id = %s AND away_team_id = %s AND game_date = %s AND venue_id = %s;"""
    
    inserted_rows = 0
    
    with open(games_csv, newline='', encoding='utf-8') as csvfile:
        
        games_reader = csv.DictReader(csvfile)
    
        for row in games_reader:
            # check if the name of the team is the same and get the team_id 
            for team in teams:
                if row["home_team"] == team["team_name"]:
                    home_team_id = team["team_id"]
                elif row["away_team"] == team["team_name"]:
                    away_team_id = team["team_id"]
            game_date = row["date"]
            venue_id = row["venue_id"]  
            
            try:
                # check if the game already exists
                cur.execute(select_games, (home_team_id, away_team_id, game_date, venue_id), prepare=True)
                if cur.rowcount == 0:
                    cur.execute(insert_games, (home_team_id, away_team_id, game_date, venue_id), prepare=True)
                    conn.commit()
                    if cur.rowcount != 0:
                        inserted_rows += 1
                # else:
                #     print("Game already exists, skipping insertion.")
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback() 
                    
    
    if inserted_rows != 0:
        return True
    else: 
        return False


# function to insert data from simulations.csv into simulations table
def insert_simulations(simulations_csv, cur, conn):
    
    sql = """SELECT * FROM games"""
    cur.execute(sql)
    games = cur.fetchall()
    
    insert_simulations = """INSERT INTO simulations (game_id, home_team_score, away_team_score, simulation_run) 
                            VALUES (%s, %s, %s, %s);"""
    select_simulations = """SELECT * FROM simulations 
                                WHERE game_id = %s AND home_team_score = %s AND away_team_score = %s AND simulation_run = %s"""
    inserted_rows = 0
    
    with open(simulations_csv, newline='', encoding='utf-8') as csvfile:
        
        simulations = {}
        simulations_reader = csv.DictReader(csvfile) 
        
        # create a dictionary with data from simulations.csv    
        for row in simulations_reader:
            key = (int(row['team_id']), int(row['simulation_run']))
            simulations[key] = int(row['results'])
        
                    
    for game in games:
        for simulation_run in range(1, 101):  # Assuming 100 simulation runs
            home_key = (game['home_team_id'], simulation_run)
            away_key = (game['away_team_id'], simulation_run)

            # check if both home and away simulations exist for this run
            if home_key in simulations and away_key in simulations:
                try:
                    # check if the simulation already exists in the database
                    cur.execute(select_simulations, (game['game_id'], simulations[home_key], simulations[away_key], simulation_run), prepare=True)
                    if cur.rowcount == 0:
                        # insert the simulation run into the database
                        cur.execute(insert_simulations, (game['game_id'], simulations[home_key], simulations[away_key], simulation_run), prepare=True)
                        conn.commit()
                        inserted_rows += 1
                        # print("Inserted row "+str(inserted_rows))
                        # print("Game id: "+str(game['game_id'])+" - Home team score: "+str(simulations[home_key])+" - Away team score: "+str(simulations[away_key])+" - Simulation run: "+str(simulation_run)+"\n")
                    # else:
                    #     print("Simulation already exists, skipping insertion.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    conn.rollback()
        
        
    if inserted_rows != 0:
        return True
    else: 
        return False
    
    