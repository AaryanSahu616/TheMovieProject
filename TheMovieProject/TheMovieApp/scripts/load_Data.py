import os
import json
import datetime
import random

from django.conf import settings
from TheMovieApp.models import Director, Genre, Tags, Movie, UserReview
from AccountsApp.models import User

# Path to your JSON file
DATA_PATH = os.path.join(settings.BASE_DIR, "MoviesApp", "data", "movies.json")


def run():
    print("📥 Importing movie data from JSON...")

    # Load JSON
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- 1. Cleanup ---
    UserReview.objects.all().delete()
    Movie.objects.all().delete()
    Director.objects.all().delete()
    Genre.objects.all().delete()
    Tags.objects.all().delete()
    print("🧹 Cleanup complete.")

    # --- 2. Create Lookup Tables (Directors, Genres, Tags) ---
    directors_map = {}
    genres_map = {}
    tags_map = {}

    # Directors
    for d in data.get("directors", []):
        obj, _ = Director.objects.get_or_create(
            name=d["name"],
            defaults={"birth_date": datetime.date.fromisoformat(d["birth_date"])}
        )
        directors_map[d["name"]] = obj

    # Tags
    for t in data.get("tags", []):
        obj, _ = Tags.objects.get_or_create(name=t)
        tags_map[t] = obj

    print(f"✅ Directors and Tags created.")

    # --- 3. Create Movies ---
    movie_objs = []
    m2m_data = []  # to store genres + tags for each movie

    for m in data.get("movies", []):
        director_name = m.get("director")
        director_obj = directors_map.get(director_name)
        if not director_obj:
            print(f"⚠️ Director '{director_name}' not found for movie '{m.get('title')}'. Skipping.")
            continue

        # Convert release_date string to date object
        try:
            release_date = datetime.date.fromisoformat(m.get("release_date"))
        except Exception:
            # fallback: random date in release_year
            release_year = m.get("release_year", 2000)
            release_date = datetime.date(release_year, random.randint(1, 12), random.randint(1, 28))

        movie = Movie(
            title=m.get("title"),
            poster=m.get("poster") or "",
            release_date=release_date,
            director=director_obj,
            synopsis=f"A film by {director_name} in {m.get('genre')}"
        )
        movie_objs.append(movie)
        m2m_data.append({
            "title": m.get("title"),
            "genres": m.get("genre"),
            "tags": m.get("tags", [])
        })

    Movie.objects.bulk_create(movie_objs)
    print(f"🎞️ Created {Movie.objects.count()} Movies.")

    # --- 4. Create Genres dynamically from movies ---
    for item in m2m_data:
        genres_list = [g.strip() for g in str(item.get("genres", "")).split(",") if g.strip()]
        for g in genres_list:
            if g not in genres_map:
                obj, _ = Genre.objects.get_or_create(name=g)
                genres_map[g] = obj

    # --- 5. Assign Many-to-Many relationships ---
    movie_lookup = {m.title: m for m in Movie.objects.all()}

    for item in m2m_data:
        movie = movie_lookup.get(item["title"])
        if not movie:
            continue

        # Genres
        genres_list = [g.strip() for g in str(item.get("genres", "")).split(",") if g.strip()]
        genre_objs = [genres_map[g] for g in genres_list if g in genres_map]
        movie.genre.add(*genre_objs)

        # Tags
        tag_objs = [tags_map[t] for t in item.get("tags", []) if t in tags_map]
        movie.tags.add(*tag_objs)

    print("🔗 Many-to-Many relationships established.")

    # --- 6. Create sample users ---
    user1, _ = User.objects.get_or_create(username="test_user1", defaults={"email": "user1@example.com"})
    user2, _ = User.objects.get_or_create(username="movie_fan", defaults={"email": "fan@example.com"})

    # --- 7. Create sample reviews ---
    review_movies = Movie.objects.all()[:5]  # first 5 movies
    reviews_to_create = []

    for movie in review_movies:
        reviews_to_create.append(UserReview(
            movie=movie,
            user=user1,
            review_text=f"A fantastic movie! Loved the direction by {movie.director.name}.",
            rating=random.randint(4, 5)
        ))
        reviews_to_create.append(UserReview(
            movie=movie,
            user=user2,
            review_text="Enjoyable and well-executed. Worth watching!",
            rating=random.randint(3, 4)
        ))

    UserReview.objects.bulk_create(reviews_to_create)
    print(f"⭐ Created {UserReview.objects.count()} User Reviews.")

    print(f"✅ Data import complete! Total Movies: {Movie.objects.count()}")
