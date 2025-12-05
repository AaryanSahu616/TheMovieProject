# In TheMovieApp/views.py
from rest_framework import generics, status
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie, UserReview, Director, Genre, Tags
from .serializers import (
    MovieSerializer,
    UserReviewSerializer,
    DirectorSerializer,
    GenreSerializer,
    TagSerializer
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

# -------------------------------------------------------------------
# TEMPLATE VIEW → renders Cotton-based movies.html
# -------------------------------------------------------------------

class MovieTemplateListView(LoginRequiredMixin, ListView):
    """
    Renders the Movies page that uses Cotton components.
    """
    model = Movie
    template_name = "TheMovieApp/movies.html"
    context_object_name = "movies"

    def get_queryset(self):
        return (
            Movie.objects
            .all()
            .select_related("director")
            .prefetch_related("genre", "tags")
            .order_by("title")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Include current user's reviews for <c-movie_modal />
        if self.request.user.is_authenticated:
            user_reviews = (
                UserReview.objects
                .filter(user=self.request.user)
                .select_related("movie")
            )
            context["user_reviews_dict"] = {r.movie_id: r for r in user_reviews}
        else:
            context["user_reviews_dict"] = {}

        # NEW — Provide lists for dynamic shelves via JS (optional)
        context["api_urls"] = {
            "tags": "/movies/api/random/tags/",
            "directors": "/movies/api/random/directors/",
            "genres": "/movies/api/random/genres/",
            "movie_filter": "/movies/api/movies/filter/",
        }

        return context


# -------------------------------------------------------------------
# STANDARD DRF VIEWS (no changes required)
# -------------------------------------------------------------------

class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]


class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]


# -------------------------------------------------------------------
# RANDOM CATEGORY APIs FOR SHELF GENERATION
# -------------------------------------------------------------------

class RandomTagsAPIView(generics.ListAPIView):
    queryset = Tags.objects.all().order_by("?")[:10]
    serializer_class = TagSerializer


class RandomDirectorsAPIView(generics.ListAPIView):
    queryset = Director.objects.all().order_by("?")[:5]
    serializer_class = DirectorSerializer


class RandomGenresAPIView(generics.ListAPIView):
    queryset = Genre.objects.all().order_by("?")[:8]
    serializer_class = GenreSerializer


# -------------------------------------------------------------------
# REVIEW ADD / UPDATE API (no changes needed)
# -------------------------------------------------------------------

class AddOrUpdateReviewAPIView(generics.GenericAPIView):
    serializer_class = UserReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)

        rating = request.data.get("rating")
        review_text = request.data.get("review_text")

        # Validate rating
        try:
            rating = float(rating)
            if not 0 <= rating <= 5:
                return Response({"error": "Rating must be between 0 and 5."},
                                status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "Rating must be a number."},
                            status=status.HTTP_400_BAD_REQUEST)

        if review_text is None:
            return Response({"error": "Review text is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        existing_review = UserReview.objects.filter(
            movie=movie, user=request.user
        ).first()

        if existing_review:
            existing_review.rating = rating
            existing_review.review_text = review_text
            existing_review.save()
            return Response({"message": f"Review updated for '{movie.title}'."})

        UserReview.objects.create(
            movie=movie,
            user=request.user,
            rating=rating,
            review_text=review_text,
        )
        return Response({"message": f"Review added for '{movie.title}'."})


# -------------------------------------------------------------------
# MOVIE FILTER API FOR SHELF GENERATION
# -------------------------------------------------------------------

class MovieFilterListAPIView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = (
            Movie.objects
            .all()
            .select_related("director")
            .prefetch_related("genre", "tags")
        )

        director_id = self.request.query_params.get("director_id")
        tag_id = self.request.query_params.get("tag_id")
        genre_id = self.request.query_params.get("genre_id")

        if director_id:
            queryset = queryset.filter(director__id=director_id)
        elif tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        elif genre_id:
            queryset = queryset.filter(genre__id=genre_id)

        return queryset.order_by("?")[:12]
