import sqlite3
import requests
import os
from contextlib import closing
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv


'''
    Feature: 
        Added a local cache for OMDb movie data to avoid making repeated API calls for movies that have already been retrieved. 
        The cache uses a 24-hour TTL (time-to-live), configured by CACHE_TTL_HOURS = 24. 
        Cached movie data is reused for up to 24 hours, after which the application fetches fresh data from the OMDb API. 
'''
def create_cache_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS movie_cache (
            imdb_id TEXT PRIMARY KEY,
            title TEXT,
            year TEXT,
            imdb_rating REAL,
            cached_at TEXT NOT NULL
        )
    """)
    connection.commit()

def get_cached_movie(connection, imdb_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT imdb_id, title, year, imdb_rating, cached_at
        FROM movie_cache
        WHERE imdb_id = ?
    """, (imdb_id,))
    return cursor.fetchone()

def cache_movie(connection, imdb_id, title, year, imdb_rating):
    connection.execute("""
        INSERT OR REPLACE INTO movie_cache
        (imdb_id, title, year, imdb_rating, cached_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        imdb_id,
        title,
        year,
        imdb_rating,
        datetime.now(timezone.utc).isoformat()
    ))
    connection.commit()

def is_cache_valid(cached_at, cache_ttl_hours):
    if cached_at.tzinfo is None:
        cached_at = cached_at.replace(tzinfo=timezone.utc)
    return (
        datetime.now(timezone.utc) - cached_at
        < timedelta(hours=cache_ttl_hours)
    )

def clear_movie_cache(connection):
    connection.execute("""
        DELETE FROM movie_cache
    """)
    connection.commit()
###### END FEATURE #######


# added a limit parameter, in case we wanted to fetch X number of movies 
def fetch_movies_from_db(connection, limit):
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit must be a positive integer")
    
    cursor = connection.cursor()
    cursor.execute("""
        SELECT imdb_id, added_at
        FROM watchlist
        ORDER BY added_at DESC
        LIMIT ?
    """, (limit,))

    return cursor.fetchall()

def get_recent_movies_from_omdb(connection, imdb_movies, cache_ttl_hours):
    if not imdb_movies:
        return []

    omdb_api_key = os.environ["OMDB_API_KEY"]
    results = []

    for movie in imdb_movies:
        imdb_id = movie['imdb_id']
        added_at = movie['added_at']

        try:
            cached_movie = get_cached_movie(connection, imdb_id)

            if cached_movie:
                cached_at = datetime.fromisoformat(
                    cached_movie['cached_at']
                )

                cache_is_valid = is_cache_valid(
                    cached_at,
                    cache_ttl_hours
                )

                if cache_is_valid:
                    results.append({
                        'title': cached_movie['title'],
                        'year': cached_movie['year'],
                        'imdb_rating': cached_movie['imdb_rating'],
                        'watchlist_date': added_at
                    })

                    print(f"Cache data found for movie id: {imdb_id}")
                    continue

            response = requests.get(
                f"http://www.omdbapi.com/?i={imdb_id}&apikey={omdb_api_key}",
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            if data.get('Response') != 'True':
                print(
                    f"OMDb error for {imdb_id}: "
                    f"{data.get('Error')}"
                )
                continue

            rating_str = data.get('imdbRating')

            rating = (
                float(rating_str)
                if rating_str and rating_str != 'N/A'
                else None
            )

            title = data['Title']
            year = data['Year']

            cache_movie(
                connection,
                imdb_id,
                title,
                year,
                rating
            )

            results.append({
                'title': title,
                'year': year,
                'imdb_rating': rating,
                'watchlist_date': added_at
            })

        except requests.RequestException as e:
            print(f"Request failed for {imdb_id}: {e}")
            continue
        except Exception as e:
            print(f"Error grabbing movie details for {imdb_id}: {e}")
            continue

    return results

def print_final_result(result):
    for movie in result:
        display_rating = (
            f"{movie['imdb_rating']:.1f}"
            if movie['imdb_rating'] is not None
            else "N/A"
        )

        print(
            f"{movie['title']:<35} | "
            f"{movie['year']} | "
            f"{display_rating:<4} | "
            f"{movie['watchlist_date']}"
        )

        # RESULT:
        # GoodFellas                          | 1990 | 8.7  | 2024-01-17 09:00:00
        # City of God                         | 2004 | 8.6  | 2024-01-24 09:00:00
        # Saving Private Ryan                 | 1998 | 8.6  | 2024-01-23 09:00:00
        # The Silence of the Lambs            | 1991 | 8.6  | 2024-01-22 09:00:00
        # Seven Samurai                       | 1954 | 8.6  | 2024-01-21 09:00:00
        # It's a Wonderful Life               | 1946 | 8.6  | 2024-01-20 09:00:00
        # Seven                               | 1995 | 8.6  | 2024-01-19 09:00:00
        # One Flew Over the Cuckoo's Nest     | 1975 | 8.6  | 2024-01-18 09:00:00
        # Modern Times                        | 1936 | 8.5  | 2024-01-26 09:00:00
        # Once Upon a Time in the West        | 1969 | 8.5  | 2024-01-25 09:00:00


def main():
    try:
        load_dotenv()
        
        fetch_movie_limit = 10
        CACHE_TTL_HOURS = 24

        with closing(sqlite3.connect('movies.db')) as connection:
            connection.row_factory = sqlite3.Row
            # clear_movie_cache(connection)
            create_cache_table(connection)
            movies = fetch_movies_from_db(connection, fetch_movie_limit)
            omdb_result = get_recent_movies_from_omdb(
                connection,
                movies,
                CACHE_TTL_HOURS
            )
            sorted_movies = sorted(
                omdb_result,
                key=lambda m: (
                    m['imdb_rating'] is None,
                    -(m['imdb_rating'] or 0)
                )
            )
            print_final_result(sorted_movies)

    except Exception as e:
        print(f'Exception: {e}')

if __name__ == "__main__":
    main()
