from server import *
import fastapi
from data.apiobjects.apiobjects import *
from fastapi.middleware.cors import CORSMiddleware

api = fastapi.FastAPI()
server = Server()

origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.post("/api/create")
def create_tournaments(data: CreateTournament):
    name = data.name
    teams = data.teams
    games = data.games
    date = data.date

    tournament_id = server.create_tournament(name,teams,games,date)

    return {"tournamentid": tournament_id}

@api.get("/api/tournaments")
def get_tournaments():
    
    tournaments = server.get_tournaments()
    
    return {"tournaments": tournaments}

@api.get("/api/{tournament_id}/fields/{field_id}")
def get_field_games(tournament_id: str, field_id: str):
    
    games = server.get_games_from_fied(tournament_id,field_id)
    return {"games":games}

@api.get("/api/{tournament_id}/game/{game_id}")
def get_game_score(tournament_id: str, game_id: str):
    
    score = server.get_game_score(tournament_id,game_id)

    return {"score": score}

@api.put("/api/{tournament_id}/game/{game_id}")
def set_game_score(tournament_id: str, game_id: str, data: ScoreUpdate):
    score = data.score
    server.set_game_score(tournament_id,game_id,score)
    return fastapi.HTTPException(status_code=200,detail="OK")

@api.get("/{tournament_id}/groups")
def get_groups(tournament_id: str):
    return {"groups": [
            ["Fun 1","0"],
            ["Fun 2","1"],
            ["Fun 3","2"],
        ]}

@api.get("/{tournament_id}/groups/{group_id}")
def get_group_teams(tournament_id: str, group_id: str):
    return {"teams": [
        ["Fun 1",2],
        ["Fun 2",0],
        ["Fun 3",5],
    ]}

@api.get("/{tournament_id}/team/{team_id}")
def get_team_info(tournament_id: str, team_id: str):
    return {"games":[
        {"team1": "Fun 1","team2": "Fun 2","start": 1743455286,"end": 1743455777,"field": 0,"points": [0,0]},
        {"team1": "Fun 2","team2": "Fun 1","start": 1743455777,"end": 1743455888,"field": 0,"points": [0,0]},
        {"team1": "","team2": "","start": 1743455888,"end": 1743455999,"field": 0,"points": [0,0]}
    ]}