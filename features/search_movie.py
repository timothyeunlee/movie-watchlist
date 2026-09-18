import requests

from features.common import redact

def search_movie_by_title(omdb_api_key, movie_title):
    try:
        response = requests.get(
            "https://www.omdbapi.com/",
            params={
                "apikey": omdb_api_key,
                "t": movie_title,
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

        if data.get("Response") != "True":
            print(
                f"Could not find movie details for movie title: "
                f"{movie_title}, {data.get('Error')}"
            )
            return

        return data

    except requests.RequestException as e:
        print(f"Request failed: {redact(e, omdb_api_key)}")

    except Exception as e:
        print(f"Error grabbing movie details: {redact(e, omdb_api_key)}")

def print_search_movie_by_title_result(data):
    if not data:
        return

    print(
        f"Title: {data.get('Title', 'N/A')} | "
        f"Year Released: {data.get('Year', 'N/A')} | "
        f"Rated: {data.get('Rated', 'N/A')} | "
        f"Runtime: {data.get('Runtime', 'N/A')} | "
        f"Genre: {data.get('Genre', 'N/A')} | "
        f"Director: {data.get('Director', 'N/A')}"
    )