from sqlalchemy import Column,Integer,String,Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    genre = Column(String,nullable=False)
    release_year = Column(Integer,nullable=False)
    developer = Column(String)
    user_rating = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Game(id={self.id}, title={self.title}, genre={self.genre}, release_year={self.release_year}, developer={self.developer})>"

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Player(id={self.id}, username={self.username})>"

class PlayerGame(Base):
    __tablename__ = 'player_games'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)

    # Relationship to Players and Games
    player = relationship("Player", backref="player_games")
    game = relationship("Game", backref="player_games")

    def __repr__(self):
        return f"<PlayerGame(id={self.id}, player_id={self.player_id}, game_id={self.game_id})>"
