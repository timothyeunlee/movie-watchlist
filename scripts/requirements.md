# Movie Watchlist Exercise
 
You have been given a small Python project containing:
 
* a pre-seeded SQLite database
* a `watchlist` table containing IMDb IDs and timestamps
* the `requests` library
* an `OMDB_API_KEY` environment variable
* a minimal Python entry point
 
The project README contains instructions for running the application and rebuilding the database.
 
## Task
 
Our application stores movies that have been added to a watchlist.
 
Each watchlist entry contains:
 
* an IMDb ID
* the date and time it was added
 
Using the existing SQLite database and the [OMDb API](https://www.omdbapi.com/), update the program so that it retrieves the **10 most recently added movies** and outputs the following information for each movie:
 
* title
* year
* IMDb rating
* date added to the watchlist
 
Order the final results from **highest to lowest IMDb rating**.
 
If information for one movie cannot be retrieved from OMDb, that should not prevent the other movies from being returned.
 
## Example output
 
The exact formatting is up to you. Something like this is sufficient:
 
```text
The Shawshank Redemption | 1994 | 9.3 | 2026-07-10 14:32:00
The Godfather             | 1972 | 9.2 | 2026-07-08 10:15:00
...
```
 
You do not need to build a user interface or HTTP server.
 
You may organize the Python code however you think is appropriate.
 
## During the exercise
 
You are welcome to:
 
* inspect the existing database and project files
* consult the OMDb API documentation
* run the program as often as you want
* ask questions about ambiguous requirements
* use normal language/library documentation
 
We are interested in your reasoning and approach as much as the final implementation. Feel free to talk through decisions, tradeoffs, or assumptions as you work.
 
You do not need to optimize for hypothetical scale unless it becomes relevant during the exercise.