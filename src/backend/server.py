import os
import string
import sqlite3
import secrets
import datetime
from database import *

class Server:
    def __init__(self):
        self.database = Database()

    def create_tournament(self,
                          name:str,
                          teams:dict,
                          games:dict,
                          date:int):
        """
        Documentation here
        """

        uuid = self.generate_unique_string()
        team_count = 0
        group_count = 0

        try:
            open(os.path.join(DATABASE_PATH,f"{uuid}.db"),"w+")
        except Exception as e:
            print(e)

        field_count = len(games)
        fields = {}
        for field in games:
            fields[f"{field}"] = f"Feld {field}"

        group_count = len(teams)
        group_data = {"1":"Fun"}
        if group_count != 1:
            group_data["2"] = "Schwitzer"
        
        team_count = sum(teams.values())
        team_data = {}
        for i in range(team_count):
            team_id = f"{i+1}"
            if group_count != 1 and i < teams["1"]:
                team_data[team_id] = [f"Fun {team_id}",1]
            else:
                team_data[team_id] = [f"Schwitzer {int(team_id)-teams["1"]}",2]

        playing_games = {}
        for field in games:
            for game in games[str(field)]:
                playing_games[game] = [field,games[field][game][0],games[field][game][1],games[field][game][2],0,0]
            
        self.database.create_tournament(uuid,name,field_count,team_count,group_count,fields,team_data,group_data,playing_games,datetime.datetime.fromtimestamp(date))

        return uuid

    def get_tournaments(self):
        """
        Documentation here
        """

        return_data = []
        files = os.listdir(DATABASE_PATH)
        for file in files.copy():
            if file.endswith(".db") and len(file) == 11:
                uuid = file.replace(".db","")
                data = self.database.get_config(uuid)[0]
                return_data.append({"id":data[0],"name":data[1],"date":data[5]})

        return return_data
    
    def get_games_from_fied(self,tournament_id:str,field_id):
        """
        Documentation here
        """

        return_data = []
        data = self.database.get_games_from_field(tournament_id,field_id)
        for game in data:
            return_data.append({"id":game[0],"score":[game[5],game[6]]})

        return return_data
    
    def get_game_score(self,tournament_id:str,game_id):
        """
        Documentation here
        """

        data = self.database.get_game_score(tournament_id,game_id)[0]

        return [data[5],data[6]]
    
    def set_game_score(self,tournament_id:str,game_id,score):
        """
        Documentation here
        """

        data = self.database.set_game_score(tournament_id,game_id,score)
        return True

    def generate_unique_string(self):
        length = 8
        characters = string.ascii_letters + string.digits
        max_iterations = len(characters)**8
        iteration = 0
        used_uuids = []
        files = os.listdir(DATABASE_PATH)
        
        for file in files.copy():
            if file.endswith(".db") and len(file) == 11:
                used_uuids.append(file.replace(".db",""))
        
        while True:
            if iteration >= max_iterations:
                return
            
            new_uuid = ""
            for i in range(length):
                new_uuid += secrets.choice(characters)

            if new_uuid not in used_uuids:
                return new_uuid


    def get_tournament_details(self, tournament_id: str):
        teams = self.database.get_teams(tournament_id)
        date = self.database.get_date(tournament_id)
        games = self.database.get_games(tournament_id)
        name = self.database.get_tournament_name(tournament_id)
        return {
        "name": name,
        "teams": teams,
        "games": games,
        "date": date
    }