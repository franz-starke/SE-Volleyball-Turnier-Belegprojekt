import os
from sqlalchemy import create_engine, NullPool, func
from sqlalchemy.orm import sessionmaker
import data.utils as utils
from contextlib import contextmanager
from typing import Union, List, Dict
from database.models import Base, Config, Group, Team, Field, Game


class Database:
    def __init__(self):
        self.engines = {}
        self.sessions = {}

    def get_engine(self, tournament_id):
        """Get or create a SQLAlchemy engine for a tournament database."""
        if tournament_id not in self.engines:
            db_path = os.path.join(utils.DATABASE_PATH, f"{tournament_id}.db")
            if not os.path.exists(db_path) and tournament_id != "":
                return None

            engine = create_engine(f'sqlite:///{db_path}', poolclass=NullPool)
            self.engines[tournament_id] = engine

        return self.engines[tournament_id]

    @contextmanager
    def session_scope(self, tournament_id):
        """Provide a transactional scope around a series of operations."""
        engine = self.get_engine(tournament_id)
        if engine is None:
            yield None
            return

        if tournament_id not in self.sessions:
            self.sessions[tournament_id] = sessionmaker(bind=engine)

        session = self.sessions[tournament_id]()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            utils.LOGGER.error(
                f"Database error for tournament: {tournament_id}")
            raise
        finally:
            session.close()

    def create_tournament(
            self,
            tournament_id: str,
            name: str,
            date: str,
            field_count: int,
            team_count: int,
            group_count: int,
            fields: Dict[str, str],
            teams: Dict[str, List[Union[str, int]]],
            groups: Dict[str, str],
            games: Dict[str, List[Union[str, int]]]) -> Union[bool, None]:
        """
        Initializes the database for a new tournament and inserts the provided data.

        Args:
            tournament_id (str): Unique identifier for the tournament.
            name (str): Tournament name.
            date (str): Tournament date.
            field_count (int): Number of fields.
            team_count (int): Number of teams.
            group_count (int): Number of groups.
            fields (dict): Field ID to name mapping.
            teams (dict): Team ID to [name, group_id] mapping.
            groups (dict): Group ID to name mapping.
            games (dict): Game ID to [field_id, team1, team2, ref, time, score1, score2].

        Returns:
            bool: True if setup is successful.
        """
        try:
            # Create database file path
            db_path = os.path.join(utils.DATABASE_PATH, f"{tournament_id}.db")

            # Create directory if it doesn't exist
            os.makedirs(utils.DATABASE_PATH, exist_ok=True)

            # Create a new SQLite database and engine
            engine = create_engine(f'sqlite:///{db_path}')
            self.engines[tournament_id] = engine

            # Create all tables defined in the Base metadata
            Base.metadata.create_all(engine)

            # Create a session
            Session = sessionmaker(bind=engine)
            self.sessions[tournament_id] = Session
            session = Session()

            try:
                # Add config
                config = Config(
                    id=tournament_id,
                    name=name,
                    date=date,
                    field_count=field_count,
                    team_count=team_count,
                    group_count=group_count
                )
                session.add(config)

                # Add groups
                for group_id, group_name in groups.items():
                    group = Group(id=group_id, name=group_name)
                    session.add(group)

                # Add fields
                for field_id, field_name in fields.items():
                    field = Field(id=field_id, name=field_name)
                    session.add(field)

                # Add teams
                for team_id, (team_name, group_id) in teams.items():
                    team = Team(id=team_id, name=team_name, group_id=group_id)
                    session.add(team)

                # Add games
                for game_id, game_data in games.items():
                    game = Game(
                        id=game_id,
                        field_id=game_data[0],
                        team1=game_data[1],
                        team2=game_data[2],
                        ref=game_data[3],
                        time=game_data[4],
                        score1=game_data[5],
                        score2=game_data[6]
                    )
                    session.add(game)

                session.commit()
                utils.LOGGER.info(
                    f"Successfully created database for tournament: {tournament_id}")
                return True

            except Exception as e:
                session.rollback()
                utils.LOGGER.error(
                    f"Failed to create tournament {tournament_id}: {str(e)}")

                # Try to delete the database file if it was created but initialization failed
                try:
                    os.remove(db_path)
                except:
                    pass

                return None
            finally:
                session.close()

        except Exception as e:
            utils.LOGGER.error(
                f"Failed to create database for tournament {tournament_id}: {str(e)}")
            return None

    def get_config(self, tournament_id: str) -> Union[List, bool, None]:
        """Returns the config of a tournament."""
        with self.session_scope(tournament_id) as session:
            if session is None:
                return None

            try:
                config = session.query(Config).filter_by(
                    id=tournament_id).first()

                if config:
                    return [(config.id, config.name, config.date,
                            config.field_count, config.team_count, config.group_count)]
                return None
            except Exception:
                utils.LOGGER.error(
                    f"Failed to get config for tournament: {tournament_id}")
                return None

    def get_games_from_field(self, tournament_id: str, field_id: str) -> Union[List, bool, None]:
        """Returns games for a specific field."""
        with self.session_scope(tournament_id) as session:
            if session is None:
                return None

            try:
                games = session.query(Game).filter_by(field_id=field_id).all()
                if games:
                    return [(game.id, game.field_id, game.team1, game.team2,
                            game.ref, game.time, game.score1, game.score2) for game in games]
                return None
            except Exception:
                utils.LOGGER.error(
                    f"Failed to get games for field {field_id} in tournament: {tournament_id}")
                return None

    def get_game_score(self, tournament_id: str, game_id: str) -> Union[List, bool, None]:
        """Returns the score for a specific game."""
        with self.session_scope(tournament_id) as session:
            if session is None:
                return None

            try:
                game = session.query(Game).filter_by(id=game_id).first()
                if game:
                    return [(game.score1, game.score2)]
                return None
            except Exception:
                utils.LOGGER.error(
                    f"Failed to get score for game {game_id} in tournament: {tournament_id}")
                return None

    def set_game_score(self, tournament_id: str, game_id: str, score: list[int]) -> bool:
        """Updates the score of a game and returns whether it was successful."""
        with self.session_scope(tournament_id) as session:
            if session is None:
                return False

            try:
                game = session.query(Game).filter_by(id=game_id).first()
                if game:
                    game.score1 = score[0]
                    game.score2 = score[1]
                    return True
                return False
            except Exception:
                utils.LOGGER.error(
                    f"Failed to set score for game {game_id} in tournament: {tournament_id}")
                return False

    def get_teams(self, tournament_id: str) -> Union[List, bool, None]:
        """Returns number of teams per group."""
        with self.session_scope(tournament_id) as session:
            if session is None:
                return None

            try:
                result = session.query(Team.group_id, func.count(Team.id).label('team_count')) \
                    .group_by(Team.group_id).all()
                if result:
                    return [(group_id, count) for group_id, count in result]
                return None
            except Exception:
                utils.LOGGER.error(
                    f"Failed to get teams for tournament: {tournament_id}")
                return None

    def get_fields(self, tournament_id: str) -> Union[List, bool, None]:
        """Returns all unique field IDs."""
        with self.session_scope(tournament_id) as session:
            if session is None:
                return None

            try:
                result = session.query(Game.field_id).distinct().all()
                if result:
                    return [(field_id,) for (field_id,) in result]
                return None
            except Exception:
                utils.LOGGER.error(
                    f"Failed to get fields for tournament: {tournament_id}")
                return None
