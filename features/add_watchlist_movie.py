import sqlite3
from contextlib import closing
from datetime import datetime, timezone

from features.search_movie import search_movie_by_title

def add_to_watchlist(omdb_api_key, movie_title):
    try:
        movie = search_movie_by_title(omdb_api_key, movie_title)

        if not movie:
            print(f"Could not find movie: {movie_title}")
            return

        movie_id = movie["imdbID"]

        with closing(sqlite3.connect("movies.db")) as connection:
            connection.row_factory = sqlite3.Row

            existing_movie = connection.execute(
                "SELECT * FROM watchlist WHERE imdb_id = ?",
                (movie_id,)
            ).fetchone()

            if existing_movie:
                print(f"{movie_title} is already in your watchlist.")
                return

            # format time to match seeded version
            formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            connection.execute(
                """
                INSERT INTO watchlist (imdb_id, added_at)
                VALUES (?, ?)
                """,
                (movie_id, formatted_time)
            )

            connection.commit()

            print(f"Added {movie['Title']} to your watchlist.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")


def delete_from_watchlist(omdb_api_key, movie_title):
    try:
        movie = search_movie_by_title(omdb_api_key, movie_title)

        if not movie:
            print(f"Could not find movie: {movie_title}")
            return

        movie_id = movie["imdbID"]

        with closing(sqlite3.connect("movies.db")) as connection:
            cursor = connection.execute(
                "DELETE FROM watchlist WHERE imdb_id = ?",
                (movie_id,)
            )

            connection.commit()

            if cursor.rowcount == 0:
                print(f"{movie['Title']} is not in your watchlist.")
            else:
                print(f"Removed {movie['Title']} from your watchlist.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    except Exception as e:
        print(f"Error removing movie from watchlist: {e}")