from fastapi import FastAPI
from routers import routers
from yoyoApply import db_migrations
from db.dbConn import connect 
from functions.importCSVFuntions import insert_teams, insert_venues, insert_games, insert_simulations
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Disable CORS as it won't allow React to access to the API
app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def init_database():
    db_migrations()
    connection_params = connect()
    cur = connection_params["cursor"]
    conn = connection_params["connection"]
    insert_teams("csv/simulations.csv", cur, conn)
    insert_venues("csv/venues.csv", cur, conn)
    insert_games("csv/games.csv", cur, conn)
    insert_simulations("csv/simulations.csv", cur, conn)
    

# function to check if FastAPI is working
@app.get("/")
async def read_main():
    return {"msg": "The server is running"}



app.include_router(routers.router)