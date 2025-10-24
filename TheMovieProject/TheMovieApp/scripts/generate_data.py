import os
import json
import random
import datetime
import requests
from django.conf import settings

# OMDb Config
OMDB_API_KEY = "8b9eee2e"
OMDB_BASE_URL = "https://www.omdbapi.com/"

# Output JSON storage
OUTPUT_PATH = os.path.join(settings.BASE_DIR, "MoviesApp", "data", "movies.json")


# ------------------------------
# Fetch poster via OMDb
# ------------------------------
def get_poster_url(title, year=None):
    try:
        params = {"t": title, "apikey": OMDB_API_KEY}
        if year:
            params["y"] = year

        resp = requests.get(OMDB_BASE_URL, params=params, timeout=5)
        data = resp.json()

        poster = data.get("Poster")
        if poster and poster != "N/A":
            return poster
    except:
        pass
    return None


# ------------------------------
# STATIC DATA
# ------------------------------
DIRECTORS_DATA = [
    {"name": "Christopher Nolan", "birth_date": "1970-07-30"},
    {"name": "Greta Gerwig", "birth_date": "1983-08-04"},
    {"name": "Quentin Tarantino", "birth_date": "1963-03-27"},
    {"name": "Denis Villeneuve", "birth_date": "1967-10-03"},
    {"name": "Hayao Miyazaki", "birth_date": "1941-01-05"},
    {"name": "Jane Campion", "birth_date": "1954-04-30"},
    {"name": "Bong Joon-ho", "birth_date": "1969-09-14"},
    {"name": "Steven Spielberg", "birth_date": "1946-12-18"},
    {"name": "Sofia Coppola", "birth_date": "1971-05-14"},
    {"name": "Alfred Hitchcock", "birth_date": "1899-08-13"},
    {"name": "Wes Anderson", "birth_date": "1969-05-01"},
    {"name": "James Cameron", "birth_date": "1954-08-16"},
    {"name": "David Fincher", "birth_date": "1962-08-28"},
    {"name": "Ridley Scott", "birth_date": "1937-11-30"},
    {"name": "Baz Luhrmann", "birth_date": "1962-09-17"},
    {"name": "Roman Polanski", "birth_date": "1933-08-18"}, # New
    {"name": "Jean-Pierre Jeunet", "birth_date": "1953-09-03"}, # New
    {"name": "Isao Takahata", "birth_date": "1935-10-29"}, # New
]

GENRES_DATA = [
    "Sci-Fi", "Drama", "Action", "Adventure", "Comedy", "Thriller", 
    "Fantasy", "Romance", "Horror", "Documentary", "Mystery", "Animation"
]

TAGS_DATA = [
    "Mind-Bending", "Time Travel", "Strong Female Lead", "Award Winner", "Must Watch",
    "Cyberpunk", "Dystopian", "Epic Scope", "Family Friendly", "Cult Classic",
    "Suspenseful", "Historical", "Philosophical", "Visually Stunning", "Dark Humor"
]

MOVIES_DATA = [
    # --- REAL CLASSICS & MODERN ICONS (1–20) - Your Original List ---
    {"title": "Inception", "release_year": 2010, "director": "Christopher Nolan", "genre": "Sci-Fi"},
    {"title": "Pulp Fiction", "release_year": 1994, "director": "Quentin Tarantino", "genre": "Crime"},
    {"title": "The Grand Budapest Hotel", "release_year": 2014, "director": "Wes Anderson", "genre": "Comedy"},
    {"title": "Jurassic Park", "release_year": 1993, "director": "Steven Spielberg", "genre": "Adventure"},
    {"title": "Titanic", "release_year": 1997, "director": "James Cameron", "genre": "Romance"},
    {"title": "Interstellar", "release_year": 2014, "director": "Christopher Nolan", "genre": "Sci-Fi"},
    {"title": "Schindler's List", "release_year": 1993, "director": "Steven Spielberg", "genre": "Drama"},
    {"title": "Django Unchained", "release_year": 2012, "director": "Quentin Tarantino", "genre": "Western"},
    {"title": "Avatar", "release_year": 2009, "director": "James Cameron", "genre": "Adventure"},
    {"title": "Psycho", "release_year": 1960, "director": "Alfred Hitchcock", "genre": "Thriller"},
    {"title": "The Dark Knight", "release_year": 2008, "director": "Christopher Nolan", "genre": "Action"},
    {"title": "Kill Bill: Vol. 1", "release_year": 2003, "director": "Quentin Tarantino", "genre": "Action"},
    {"title": "The Royal Tenenbaums", "release_year": 2001, "director": "Wes Anderson", "genre": "Drama"},
    {"title": "Saving Private Ryan", "release_year": 1998, "director": "Steven Spielberg", "genre": "War"},
    {"title": "Aliens", "release_year": 1986, "director": "James Cameron", "genre": "Sci-Fi"},
    {"title": "Rear Window", "release_year": 1954, "director": "Alfred Hitchcock", "genre": "Mystery"},
    {"title": "E.T. the Extra-Terrestrial", "release_year": 1982, "director": "Steven Spielberg", "genre": "Family"},
    {"title": "The Hateful Eight", "release_year": 2015, "director": "Quentin Tarantino", "genre": "Western"},
    {"title": "Tenet", "release_year": 2020, "director": "Christopher Nolan", "genre": "Sci-Fi"},
    {"title": "True Lies", "release_year": 1994, "director": "James Cameron", "genre": "Action"},
    
    # --- NEW REAL MOVIES (21–50) ---
    {"title": "Oppenheimer", "release_year": 2023, "director": "Christopher Nolan", "genre": "Drama"},
    {"title": "Dunkirk", "release_year": 2017, "director": "Christopher Nolan", "genre": "War"},
    {"title": "Reservoir Dogs", "release_year": 1992, "director": "Quentin Tarantino", "genre": "Crime"},
    {"title": "Once Upon a Time in Hollywood", "release_year": 2019, "director": "Quentin Tarantino", "genre": "Drama"},
    {"title": "Moonrise Kingdom", "release_year": 2012, "director": "Wes Anderson", "genre": "Adventure"},
    {"title": "Isle of Dogs", "release_year": 2018, "director": "Wes Anderson", "genre": "Animation"},
    {"title": "Raiders of the Lost Ark", "release_year": 1981, "director": "Steven Spielberg", "genre": "Adventure"},
    {"title": "Jaws", "release_year": 1975, "director": "Steven Spielberg", "genre": "Thriller"},
    {"title": "Terminator 2: Judgment Day", "release_year": 1991, "director": "James Cameron", "genre": "Sci-Fi"},
    {"title": "The Terminator", "release_year": 1984, "director": "James Cameron", "genre": "Sci-Fi"},
    {"title": "Vertigo", "release_year": 1958, "director": "Alfred Hitchcock", "genre": "Mystery"},
    {"title": "North by Northwest", "release_year": 1959, "director": "Alfred Hitchcock", "genre": "Thriller"},
    {"title": "Arrival", "release_year": 2016, "director": "Denis Villeneuve", "genre": "Sci-Fi"},
    {"title": "Prisoners", "release_year": 2013, "director": "Denis Villeneuve", "genre": "Thriller"},
    {"title": "Spirited Away", "release_year": 2001, "director": "Hayao Miyazaki", "genre": "Animation"},
    {"title": "Princess Mononoke", "release_year": 1997, "director": "Hayao Miyazaki", "genre": "Fantasy"},
    {"title": "The Power of the Dog", "release_year": 2021, "director": "Jane Campion", "genre": "Drama"},
    {"title": "Pianist, The", "release_year": 2002, "director": "Roman Polanski", "genre": "Drama"}, # Note: Added director data for Polanski, check full script below
    {"title": "Parasite", "release_year": 2019, "director": "Bong Joon-ho", "genre": "Thriller"},
    {"title": "Memories of Murder", "release_year": 2003, "director": "Bong Joon-ho", "genre": "Mystery"},
    {"title": "Lost in Translation", "release_year": 2003, "director": "Sofia Coppola", "genre": "Romance"},
    {"title": "The Virgin Suicides", "release_year": 1999, "director": "Sofia Coppola", "genre": "Drama"},
    {"title": "Se7en", "release_year": 1995, "director": "David Fincher", "genre": "Mystery"},
    {"title": "Fight Club", "release_year": 1999, "director": "David Fincher", "genre": "Drama"},
    {"title": "Gladiator", "release_year": 2000, "director": "Ridley Scott", "genre": "Action"},
    {"title": "Blade Runner", "release_year": 1982, "director": "Ridley Scott", "genre": "Sci-Fi"},
    {"title": "The Great Gatsby", "release_year": 2013, "director": "Baz Luhrmann", "genre": "Romance"},
    {"title": "Moulin Rouge!", "release_year": 2001, "director": "Baz Luhrmann", "genre": "Romance"},
    {"title": "Amélie", "release_year": 2001, "director": "Jean-Pierre Jeunet", "genre": "Comedy"}, # Note: Added director data for Jeunet, check full script below
    {"title": "Grave of the Fireflies", "release_year": 1988, "director": "Isao Takahata", "genre": "Animation"}, # Note: Added director data for Takahata, check full script below
]


# (You will paste your existing static lists here unchanged)


# ------------------------------
# MAIN
# ------------------------------
def run():
    print("📦 Generating JSON metadata...")

    result = {
        "directors": DIRECTORS_DATA,
        "genres": GENRES_DATA,
        "tags": TAGS_DATA,
        "movies": []
    }

    for m in MOVIES_DATA:
        poster = get_poster_url(m["title"], m["release_year"])

        movie_entry = {
            "title": m["title"],
            "release_year": m["release_year"],
            "director": m["director"],
            "genre": m["genre"],
            "poster": poster,
            "release_date": str(datetime.date(m["release_year"], random.randint(1,12), random.randint(1,28))),
            "tags": random.sample(TAGS_DATA, random.randint(1, 3))
        }

        result["movies"].append(movie_entry)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)

    print(f"✅ JSON saved to: {OUTPUT_PATH}")
