from classes.dataAPI import Games, Simulations
from typing import List, Dict
from fastapi import APIRouter, Response
from db.dbConn import connect

router = APIRouter()


@router.get("/api/games", response_model=Games)
# function for GET response
def read_games() -> Games:
    
    connection_params = connect()
    cur = connection_params["cursor"]
    
    get_games = Games()
    all_data = get_games.select_games(cur)
    gamesList = {"GamesList": get_games.parse_games_data(all_data)}
    
    cur.close()
    
    return gamesList


@router.get("/api/simulations", response_model=Simulations)
# function for GET response
def read_simulations(game_id: int = None) -> Simulations:
    
    connection_params = connect()
    cur = connection_params["cursor"]
    
    get_simulations = Simulations()
    all_data = get_simulations.select_simulations_results(game_id, cur)
    percentage_home_win = get_simulations.calculate_percentage_win_home_team(game_id, cur)
    simulationsList = get_simulations.parse_simulations_data(all_data, percentage_home_win)
    
    cur.close()
    
    return simulationsList

