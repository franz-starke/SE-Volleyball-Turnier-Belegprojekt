from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Config(Base):
    __tablename__ = 'config'
    id = Column(String, primary_key=True)
    name = Column(String)
    date = Column(String)
    field_count = Column(Integer)
    team_count = Column(Integer)
    group_count = Column(Integer)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(String, primary_key=True)
    name = Column(String)


class Team(Base):
    __tablename__ = 'teams'
    id = Column(String, primary_key=True)
    name = Column(String)
    group_id = Column(String, ForeignKey('groups.id'))


class Field(Base):
    __tablename__ = 'fields'
    id = Column(String, primary_key=True)
    name = Column(String)


class Game(Base):
    __tablename__ = 'games'
    id = Column(String, primary_key=True)
    field_id = Column(String, ForeignKey('fields.id'))
    team1 = Column(String, ForeignKey('teams.id'))
    team2 = Column(String, ForeignKey('teams.id'))
    ref = Column(String, ForeignKey('teams.id'))
    time = Column(String)
    score1 = Column(Integer)
    score2 = Column(Integer)
