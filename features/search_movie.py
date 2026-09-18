import requests

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
        print(f"Request failed: {e}")

    except Exception as e:
        print(f"Error grabbing movie details: {e}")

def print_search_movie_by_title_result(data):
    print(
        f"Title: {data['Title']} | "
        f"Year Released: {data['Year']} | "
        f"Rated: {data['Rated']} | "
        f"Runtime: {data['Runtime']} | "
        f"Genre: {data['Genre']} | "
        f"Director: {data['Director']}"
    )
