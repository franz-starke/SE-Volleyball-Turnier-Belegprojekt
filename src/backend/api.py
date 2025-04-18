from server import *
import fastapi
from data.apiobjects.apiobjects import *
from fastapi.middleware.cors import CORSMiddleware
from database import create_tournament_db
import uuid

api = fastapi.FastAPI()
server = Server()

@api.post("/create")
def create_tournaments(data: CreateTournament):
    tournament_id = str(uuid.uuid4())
    create_tournament_db(tournament_id)
    return {"turnamentid": "0"}

@api.get("/tournaments")
def get_tournaments():
    return {"tournaments": [
        ["Nikolaus Tournier 2024",1743455286,"0"],
        ["Weihnachts Tournier 2024",1743455354,"1"]
    ]}

@api.get("/{tournament_id}/fields/{field_id}")
def get_field_games(tournament_id: str, field_id: str):
    return {"games": [
        ["0",1743455286,1743455777,["0","Fun 1"],["1","Fun 2"],"Fun 3",[0,0]],
        ["1",1743455888,1743455999,["1","Fun 2"],["0","Fun 1"],"Fun 3",[10,10]],
    ]}

@api.get("/{tournament_id}/game/{game_id}")
def get_game_points(tournament_id: str, game_id: str):
    return {"points": [0,0]}

@api.put("/{tournament_id}/game/{game_id}")
def update_game_points(tournament_id: str, game_id: str, points: PointUpdate):
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