from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    # Establishing the relationship with PlayerGame
    player_games = relationship("PlayerGame", back_populates="player")

    def add_game(self, game):
        """Add a game to the player and create a PlayerGame entry."""
        player_game = PlayerGame(player=self, game=game)
        # This automatically updates the player_games relationship
        self.player_games.append(player_game)

    def __repr__(self):
        return f"<Player(id={self.id}, username={self.username})>"


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    genre = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
    developer = Column(String)
    user_rating = Column(Float, nullable=True)

    # Establishing the relationship with PlayerGame
    player_games = relationship("PlayerGame", back_populates="game")

    def __repr__(self):
        return f"<Game(id={self.id}, title={self.title}, genre={self.genre}, release_year={self.release_year}, user_rating={self.user_rating})>"


class PlayerGame(Base):
    __tablename__ = 'player_games'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)

    # Linking back to Player and Game with relationships
    player = relationship("Player", back_populates="player_games")
    game = relationship("Game", back_populates="player_games")

    def __repr__(self):
        return f"<PlayerGame(id={self.id}, player_id={self.player_id}, game_id={self.game_id})>"
