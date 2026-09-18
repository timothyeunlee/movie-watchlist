from datetime import datetime, timedelta, timezone


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