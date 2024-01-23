from typing import List, Dict
from dataclasses import dataclass, field
from fastapi import HTTPException



@dataclass
class Games():
    
    GamesList: list = field(default_factory=list)
    
    def __init__(self):
        
        self.gamesList = []

    # method to return the data about games
    def select_games(self, cur):
        
        sql_games = """SELECT g.game_id, ht.team_name as home_team, at.team_name as away_team, g.game_date, g.venue_id, v.venue_name
                        FROM games g
                        JOIN teams ht ON ht.team_id = g.home_team_id
                        JOIN teams at ON at.team_id = g.away_team_id
                        JOIN venues v ON v.venue_id = g.venue_id
                        ORDER BY g.game_id;"""
                        
        if cur != 'error':
            
            cur.execute(sql_games)

            all_data = cur.fetchall()

        return all_data
    
    # method to build JSON from a set of data selected from db
    def parse_games_data(self, all_data):
        
        if all_data != []:
                
            for data in all_data:
                
                game = {
                        "game_id": data["game_id"],
                        "home_team": data["home_team"],
                        "away_team": data["away_team"],
                        "game_date": data["game_date"],
                        "venue_name": data["venue_name"] 
                        }
                
                self.gamesList.append(game)
                
        else:
            self.gamesList = [{"error": "Game not found"}]
            raise HTTPException(status_code=404, detail="Game not found")
        
        return self.gamesList


@dataclass
class Simulations():
    
    HomeTeamWinPercentage: str
    SimulationsList: list = field(default_factory=list)
    
    def __init__(self):
        
        self.simulationsList = []
        self.homeWinPercentage = ""

    # method to select data about simulations
    def select_simulations_results(self, game_id, cur):
        
        sql_simulations = """SELECT s.game_id, ht.team_name as home_team, at.team_name as away_team, s.home_team_score, s.away_team_score, s.simulation_run  
                            FROM simulations s 
                            JOIN games g ON g.game_id = s.game_id 
                            JOIN teams ht ON ht.team_id = g.home_team_id
                            JOIN teams at ON at.team_id = g.away_team_id 
                            WHERE s.game_id = %s"""
                            
        if cur != 'error':
            
            cur.execute(sql_simulations, (game_id,), prepare=True)

            all_data = cur.fetchall()

        return all_data               
    
    # method to build JSON from a set of data selected from db
    def parse_simulations_data(self, all_data, win_percentage):
        
        if all_data != []:
                
            for data in all_data:
                
                simulation = {
                                "game_id": data["game_id"],
                                "home_team": data["home_team"],
                                "away_team": data["away_team"],
                                "home_team_score": data["home_team_score"],
                                "away_team_score": data["away_team_score"],
                                "simulation_run": data["simulation_run"] 
                                }
                
                self.simulationsList.append(simulation)
            result = {
                        "HomeTeamWinPercentage": win_percentage,
                        "SimulationsList": self.simulationsList
                        }
                
        else:
            self.simulationsList = [{"error": "Simulation not found"}]
            raise HTTPException(status_code=404, detail="Simulation not found")
        
        return result     
    
    
    # method to calculate percentage of wins for home team
    def calculate_percentage_win_home_team(self, game_id, cur):
        
        sql = """WITH game_simulations as 
                (
                    SELECT s.game_id, ht.team_name as home_team, at.team_name as away_team, s.home_team_score, s.away_team_score, s.simulation_run  
                    FROM simulations s 
                    JOIN games g ON g.game_id = s.game_id 
                    JOIN teams ht ON ht.team_id = g.home_team_id
                    JOIN teams at ON at.team_id = g.away_team_id 
                    WHERE s.game_id = %s 
                ) 
                
                SELECT count(home_team) FROM game_simulations WHERE home_team_score > away_team_score;"""
                
        if cur != 'error':
            
            cur.execute(sql, (game_id,), prepare=True)

            result = cur.fetchone()
            self.homeWinPercentage = str(result["count"])+"%"

        return self.homeWinPercentage        
                        