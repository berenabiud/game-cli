import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base,Player,Game,PlayerGame

DATABASE_URL="sqlite:///game.db"
engine=create_engine(DATABASE_URL)
Session=sessionmaker(bind=engine)
session=Session()

def init_db():
    Base.metadata.create_all(engine)
    print("batabase initiallized")

def add_game(session, title, genre, release_year, developer, user_rating=None):
    game = Game(
        title=title, 
        genre=genre, 
        release_year=release_year, 
        developer=developer, 
        user_rating=user_rating
    )
    session.add(game)
    session.commit()
    return game

def list_games(session):
    games = session.query(Game).all()
    return games

def search_games(session, title=None, genre=None):
    query = session.query(Game)
    if title:
        query = query.filter(Game.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(Game.genre.ilike(f"%{genre}%"))
    return query.all()

def delete_game(session, game_id=None, title=None):
    if game_id:
        game = session.query(Game).filter_by(id=game_id).first()
    elif title:
        game = session.query(Game).filter_by(title=title).first()
    else:
        return None

    if game:
        session.delete(game)
        session.commit()
        return True
    return False

def add_player(session, username):
    player = Player(username=username)
    session.add(player)
    session.commit()
    return player

def list_players(session):
    players = session.query(Player).all()
    return players

def update_player_username(session, player_id, new_username):
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        player.username = new_username
        session.commit()
        return player
    return None

def delete_player(session, player_id):
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        session.delete(player)
        session.commit()
        return True
    return False

def view_games_by_player(session, player_id):
    player_games = session.query(PlayerGame).filter_by(player_id=player_id).all()
    return [pg.game for pg in player_games]

def list_game_ratings(session):
    games = session.query(Game).all()
    return [(game.title, game.user_rating) for game in games]
def add_game_to_player(session, player_id, game_id):
    # Fetch the player and game from the database
    player = session.query(Player).filter_by(id=player_id).first()
    game = session.query(Game).filter_by(id=game_id).first()

    # Check if both player and game exist
    if player and game:
        # Add the game to the player using the add_game method
        player.add_game(game)
        session.commit()  # Save changes to the database
        print(f"Game '{game.title}' added to player '{player.username}'!")
    else:
        print("Player or Game not found!")

def main_menu():
   
    while True:
        print("\nGame Library Options:")
        print("1. Add Game")
        print("2. List Games")
        print("3. Search Game")
        print("4. Delete Game")
        print("5. Add Player")
        print("6. List Players")
        print("7. Update Player Username")
        print("8. Delete Player")
        print("9. View Games by Player")
        print("10. List Game Ratings")
        print("11. Add Game to Player")
        print("0. Exit")

        choice = input("Choose an option: ")
        
        if choice == "1":
            title = input("Title: ")
            genre = input("Genre: ")
            release_year = int(input("Release Year: "))
            developer = input("Developer: ")
            rating = input("Rating (optional, press Enter to skip): ")
            user_rating = float(rating) if rating else None
            add_game(session, title, genre, release_year, developer, user_rating)
            print("Game added successfully!")

        elif choice == "2":
            games = list_games(session)
            for game in games:
                print(game)

        elif choice == "3":
            title = input("Search by Title (optional): ")
            genre = input("Search by Genre (optional): ")
            results = search_games(session, title, genre)
            for game in results:
                print(game)

        elif choice == "4":
            game_id = input("Game ID to delete (optional): ")
            title = input("Game Title to delete (optional): ")
            success = delete_game(session, game_id=game_id or None, title=title or None)
            if success:
                print("Game deleted successfully!")
            else:
                print("Game not found.")

        elif choice == "5":
            username = input("Username: ")
            add_player(session, username)
            print("Player added successfully!")

        elif choice == "6":
            players = list_players(session)
            for player in players:
                print(player)

        elif choice == "7":
            player_id = int(input("Player ID: "))
            new_username = input("New Username: ")
            updated_player = update_player_username(session, player_id, new_username)
            if updated_player:
                print("Player username updated successfully!")
            else:
                print("Player not found.")

        elif choice == "8":
            player_id = int(input("Player ID to delete: "))
            success = delete_player(session, player_id)
            if success:
                print("Player deleted successfully!")
            else:
                print("Player not found.")

        elif choice == "9":
            player_id = int(input("Player ID: "))
            games = view_games_by_player(session, player_id)
            if games:
                print(f"Games played by Player {player_id}:")
                for game in games:
                    print(game)
            else:
                print("No games found for this player or player does not exist.")

        elif choice == "10":
            games = list_game_ratings(session)
            print("Games and Ratings:")
            for title, user_rating in games:
                print(f"{title} - Rating: {user_rating if user_rating else 'No rating'}")
        elif choice == "11":  # Add the logic for adding a game to a player
            player_id = int(input("Player ID: "))
            game_id = int(input("Game ID: "))
            add_game_to_player(session, player_id, game_id)

        elif choice == "0":
            print("Exiting the Game Library. Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a valid option.")
if __name__ == "__main__":
    init_db()  # Call the function to initialize the database
    main_menu()     # Call the main function for the menu
