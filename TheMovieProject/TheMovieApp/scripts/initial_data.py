# MoviesApp/scripts/initial_data.py

from django.db import IntegrityError
# NOTE: Update 'YourAppName' to your actual app name (e.g., 'movies')
from TheMovieApp.models import Director, Genre, Tags, Movie, UserReview 
from AccountsApp.models import User
import datetime
import random
import requests
import os
from itertools import cycle
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings

# --- Configuration Data for 50 Movies ---
OMDB_API_KEY = "8b9eee2e"  # <-- replace with your OMDb API key
OMDB_BASE_URL = "https://www.omdbapi.com/"
# OMDB_BASE_URL = "http://www.omdbapi.com/?i=tt3896198&apikey=8b9eee2e"

def get_poster_url(title, year=None):
    """Fetch movie poster from OMDb API and optionally download it locally."""
    try:
        params = {"t": title, "apikey": OMDB_API_KEY}
        if year:
            params["y"] = year
        response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
        data = response.json()
        poster = data.get("Poster")

        if poster and poster != "N/A":
            # Download and save locally
            poster_response = requests.get(poster, timeout=5)
            if poster_response.status_code == 200:
                file_name = f"{title.replace(' ', '_')}.jpg"
                file_path = os.path.join(settings.MEDIA_ROOT, "posters", file_name)

                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(poster_response.content)

                # Return relative path for Django's ImageField
                return f"posters/{file_name}"
            # return poster_response.url
    except Exception as e:
        print(f"Poster fetch failed for {title}: {e}")

    return "posters/no-poster.png"  # default fallback in your media folder


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
# --- Main Run Function ---
def run():
    print("🎬 --- Starting bulk data population (50 Movies) ---")

    # --- 1. Cleanup ---
    UserReview.objects.all().delete()
    Movie.objects.all().delete()
    Director.objects.all().delete()
    Genre.objects.all().delete()
    Tags.objects.all().delete()
    print("🧹 Cleanup complete.")

    # --- 2. Create Lookup Tables (Director, Genre, Tags) ---
    directors_map = {}
    genres_map = {}
    tags_map = {}

    # Directors
    for d_data in DIRECTORS_DATA:
        director, _ = Director.objects.get_or_create(
            name=d_data["name"],
            defaults={"birth_date": datetime.date.fromisoformat(d_data["birth_date"])}
        )
        directors_map[d_data["name"]] = director

    # Genres
    for g_name in GENRES_DATA:
        genre, _ = Genre.objects.get_or_create(name=g_name)
        genres_map[g_name] = genre

    # Tags
    for t_name in TAGS_DATA:
        tag, _ = Tags.objects.get_or_create(name=t_name)
        tags_map[t_name] = tag

    print(f"📚 Created {Director.objects.count()} Directors, {Genre.objects.count()} Genres, {Tags.objects.count()} Tags.")

    # --- 3. Create Movie Data (Bulk Creation) ---
    movies_to_create = []
    m2m_data = []

    for m_data in MOVIES_DATA:
        director_obj = directors_map.get(m_data["director"])
        if not director_obj:
            print(f"⚠️ Skipping {m_data['title']} — director not found.")
            continue

        # Fetch poster URL from OMDb
        poster_url = get_poster_url(m_data["title"], m_data["release_year"])

        # Generate a pseudo-random date in that year
        release_date = datetime.date(m_data["release_year"], random.randint(1, 12), random.randint(1, 28))

        # Create movie object
        movie = Movie(
            title=m_data["title"],
            synopsis=f"A thought-provoking {', '.join(m_data.get('genres', []))} film directed by {m_data['director']}.",
            poster=poster_url,
            release_date=release_date,
            director=director_obj,
        )
        movies_to_create.append(movie)

        # M2M data (assign 1–2 genres + 1–3 random tags)
        m2m_data.append({
            "title": m_data["title"],
            "genres": m_data.get("genres", []),
            "tags": random.sample(list(tags_map.keys()), random.randint(1, 3)),
        })

    Movie.objects.bulk_create(movies_to_create)
    print(f"🎞️ Created {Movie.objects.count()} Movies.")

    # --- 4. Add Many-to-Many Relationships ---
    movie_lookup = {movie.title: movie for movie in Movie.objects.all()}

    for item in m2m_data:
        movie = movie_lookup.get(item["title"])
        if not movie:
            continue

        # Link genres
        genre_objs = [genres_map[g] for g in item["genres"] if g in genres_map]
        movie.genre.add(*genre_objs)

        # Link tags
        tag_objs = [tags_map[t] for t in item["tags"] if t in tags_map]
        movie.tags.add(*tag_objs)

    print("🔗 Many-to-Many relationships established.")

    # --- 5. Create Users ---
    try:
        user1, _ = User.objects.get_or_create(username="test_user1", defaults={"email": "user1@example.com"})
        user2, _ = User.objects.get_or_create(username="movie_fan", defaults={"email": "fan@example.com"})
    except IntegrityError:
        print("⚠️ WARNING: Could not create test users. Ensure they exist.")
        user1 = User.objects.filter(username="test_user1").first()
        user2 = User.objects.filter(username="movie_fan").first()

    # --- 6. Create User Reviews ---
    review_movies = Movie.objects.all()[:5]
    if user1 and user2 and review_movies.exists():
        reviews_to_create = []
        for movie in review_movies:
            reviews_to_create.append(
                UserReview(
                    movie=movie,
                    user=user1,
                    review_text=f"A fantastic movie! Loved the direction by {movie.director.name}.",
                    rating=random.randint(4, 5)
                )
            )
            reviews_to_create.append(
                UserReview(
                    movie=movie,
                    user=user2,
                    review_text="Enjoyable and well-executed. Worth watching!",
                    rating=random.randint(3, 4)
                )
            )
        UserReview.objects.bulk_create(reviews_to_create)
        print(f"⭐ Created {UserReview.objects.count()} User Reviews.")
    else:
        print("⚠️ Skipping UserReview creation (missing users or movies).")

    print(f"✅ --- Data population complete. Total Movies: {Movie.objects.count()} ---")

